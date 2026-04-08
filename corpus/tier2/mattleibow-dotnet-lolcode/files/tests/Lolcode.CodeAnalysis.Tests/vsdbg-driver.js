#!/usr/bin/env node
// vsdbg-driver.js — DAP protocol driver for vsdbg with vsda handshake support.
// Used by VsdbgDebuggerTests.cs to drive vsdbg from C# xUnit tests.
//
// Usage: node vsdbg-driver.js <vsdbgPath> <vsdaPath>
// Reads JSON commands from stdin (one per line), writes JSON results to stdout.
//
// Commands:
//   { "cmd": "launch", "program": "...", "cwd": "...", "stopAtEntry": true }
//   { "cmd": "setBreakpoints", "source": "...", "lines": [4, 5] }
//   { "cmd": "continue", "threadId": 123 }
//   { "cmd": "next", "threadId": 123 }
//   { "cmd": "stepIn", "threadId": 123 }
//   { "cmd": "stackTrace", "threadId": 123 }
//   { "cmd": "scopes", "frameId": 456 }
//   { "cmd": "variables", "ref": 789 }
//   { "cmd": "threads" }
//   { "cmd": "disconnect" }

"use strict";

const { spawn } = require("child_process");
const path = require("path");
const readline = require("readline");

const vsdbgPath = process.argv[2];
const vsdaPath = process.argv[3];

if (!vsdbgPath || !vsdaPath) {
    output({ error: "Usage: node vsdbg-driver.js <vsdbgPath> <vsdaPath>" });
    process.exit(1);
}

let vsda;
try {
    vsda = require(vsdaPath);
} catch (e) {
    output({ error: "Failed to load vsda: " + e.message });
    process.exit(1);
}

const signer = new vsda.signer();

// Start vsdbg
const proc = spawn(vsdbgPath, ["--interpreter=vscode"], {
    stdio: ["pipe", "pipe", "pipe"],
});

proc.on("error", (e) => {
    output({ error: "vsdbg spawn error: " + e.message });
    process.exit(1);
});

proc.on("exit", (code) => {
    output({ event: "vsdbg_exit", code });
});

// DAP message handling
let dapSeq = 0;
let dapBuffer = "";
const pendingRequests = new Map(); // seq -> { resolve, reject, timer }
const eventQueue = []; // collected events
let initialized = false;

function dapSend(type, command, args, requestSeq) {
    dapSeq++;
    const msg = { seq: dapSeq, type };
    if (type === "request") {
        msg.command = command;
        if (args !== undefined) msg.arguments = args;
    } else if (type === "response") {
        msg.command = command;
        msg.request_seq = requestSeq;
        msg.success = true;
        msg.body = args || {};
    }
    const json = JSON.stringify(msg);
    const data = "Content-Length: " + Buffer.byteLength(json) + "\r\n\r\n" + json;
    proc.stdin.write(data);
    return dapSeq;
}

function dapRequest(command, args, timeoutMs) {
    timeoutMs = timeoutMs || 15000;
    return new Promise((resolve, reject) => {
        const seq = dapSend("request", command, args);
        const timer = setTimeout(() => {
            pendingRequests.delete(seq);
            reject(new Error("Timeout waiting for " + command + " response"));
        }, timeoutMs);
        pendingRequests.set(seq, { resolve, reject, timer });
    });
}

function waitForEvent(eventName, timeoutMs) {
    timeoutMs = timeoutMs || 30000;
    // Check already-received events
    for (let i = 0; i < eventQueue.length; i++) {
        if (eventQueue[i].event === eventName) {
            return Promise.resolve(eventQueue.splice(i, 1)[0]);
        }
    }
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
            reject(new Error("Timeout waiting for event: " + eventName));
        }, timeoutMs);
        const check = setInterval(() => {
            for (let i = 0; i < eventQueue.length; i++) {
                if (eventQueue[i].event === eventName) {
                    clearInterval(check);
                    clearTimeout(timer);
                    resolve(eventQueue.splice(i, 1)[0]);
                    return;
                }
            }
        }, 50);
    });
}

// Parse DAP messages from vsdbg stdout
proc.stdout.on("data", (chunk) => {
    dapBuffer += chunk.toString();
    while (true) {
        const idx = dapBuffer.indexOf("\r\n\r\n");
        if (idx < 0) break;
        const header = dapBuffer.substring(0, idx);
        const m = header.match(/Content-Length:\s*(\d+)/);
        if (!m) break;
        const len = parseInt(m[1]);
        const bodyStart = idx + 4;
        if (dapBuffer.length < bodyStart + len) break;
        const body = dapBuffer.substring(bodyStart, bodyStart + len);
        dapBuffer = dapBuffer.substring(bodyStart + len);
        handleDapMessage(JSON.parse(body));
    }
});

function handleDapMessage(msg) {
    // Log all messages to stderr for diagnostics
    if (msg.type !== "event" || msg.event !== "output" || (msg.body && msg.body.category !== "telemetry")) {
        process.stderr.write("DAP: " + msg.type + " " + (msg.command || msg.event || "") +
            (msg.success === false ? " FAILED: " + (msg.message || "") : "") + "\n");
    }

    if (msg.type === "request" && msg.command === "handshake") {
        // Sign the challenge with vsda
        const signature = signer.sign(msg.arguments.value);
        dapSend("response", "handshake", { signature }, msg.seq);
        return;
    }

    if (msg.type === "response") {
        const entry = pendingRequests.get(msg.request_seq);
        if (entry) {
            pendingRequests.delete(msg.request_seq);
            clearTimeout(entry.timer);
            entry.resolve(msg);
        }
    } else if (msg.type === "event") {
        eventQueue.push(msg);
    }
}

function output(obj) {
    process.stdout.write(JSON.stringify(obj) + "\n");
}

// Initialize the debug adapter
async function initializeAdapter() {
    const resp = await dapRequest("initialize", {
        clientID: "lolcode-test",
        adapterID: "coreclr",
        pathFormat: "path",
        linesStartAt1: true,
        columnsStartAt1: true,
        supportsRunInTerminalRequest: true,
        supportsHandshakeRequest: true,
    });
    if (!resp.success) {
        throw new Error("initialize failed: " + (resp.message || JSON.stringify(resp)));
    }
    initialized = true;
}

// Process commands from stdin
const rl = readline.createInterface({ input: process.stdin, terminal: false });

rl.on("line", async (line) => {
    let cmd;
    try {
        cmd = JSON.parse(line.trim());
    } catch (e) {
        output({ error: "Invalid JSON: " + e.message });
        return;
    }

    try {
        if (!initialized && cmd.cmd !== "disconnect") {
            await initializeAdapter();
        }

        switch (cmd.cmd) {
            case "launch": {
                const resp = await dapRequest("launch", {
                    type: "coreclr",
                    request: "launch",
                    program: cmd.program,
                    args: cmd.args || [],
                    cwd: cmd.cwd || path.dirname(cmd.program),
                    stopAtEntry: cmd.stopAtEntry !== false,
                    justMyCode: false,
                }, 30000);
                if (!resp.success) {
                    output({ error: "launch failed: " + (resp.message || "") });
                    break;
                }
                const confResp = await dapRequest("configurationDone", {}, 30000);
                if (!confResp.success) {
                    output({ error: "configurationDone failed: " + (confResp.message || "") });
                    break;
                }
                // Wait for the stopped event (entry or breakpoint)
                const stopped = await waitForEvent("stopped", 30000);
                output({
                    result: "launched",
                    threadId: stopped.body.threadId,
                    reason: stopped.body.reason,
                });
                break;
            }

            case "setBreakpoints": {
                const resp = await dapRequest("setBreakpoints", {
                    source: { path: cmd.source },
                    breakpoints: cmd.lines.map((l) => ({ line: l })),
                    sourceModified: false,
                });
                const bps = (resp.body && resp.body.breakpoints) || [];
                output({
                    result: "breakpoints",
                    breakpoints: bps.map((bp) => ({
                        verified: bp.verified,
                        line: bp.line,
                        id: bp.id,
                    })),
                });
                break;
            }

            case "continue": {
                await dapRequest("continue", { threadId: cmd.threadId });
                const stopped = await waitForEvent("stopped", 30000);
                output({
                    result: "stopped",
                    reason: stopped.body.reason,
                    threadId: stopped.body.threadId,
                    hitBreakpointIds: stopped.body.hitBreakpointIds || [],
                });
                break;
            }

            case "next": {
                await dapRequest("next", { threadId: cmd.threadId });
                const stopped = await waitForEvent("stopped", 30000);
                output({
                    result: "stopped",
                    reason: stopped.body.reason,
                    threadId: stopped.body.threadId,
                });
                break;
            }

            case "stepIn": {
                await dapRequest("stepIn", { threadId: cmd.threadId });
                const stopped = await waitForEvent("stopped", 30000);
                output({
                    result: "stopped",
                    reason: stopped.body.reason,
                    threadId: stopped.body.threadId,
                });
                break;
            }

            case "stackTrace": {
                const resp = await dapRequest("stackTrace", {
                    threadId: cmd.threadId,
                    startFrame: 0,
                    levels: cmd.levels || 20,
                });
                const frames = (resp.body && resp.body.stackFrames) || [];
                output({
                    result: "stackTrace",
                    frames: frames.map((f) => ({
                        id: f.id,
                        name: f.name,
                        line: f.line,
                        column: f.column,
                        source: f.source ? f.source.path || f.source.name : null,
                    })),
                });
                break;
            }

            case "scopes": {
                const resp = await dapRequest("scopes", { frameId: cmd.frameId });
                const scopes = (resp.body && resp.body.scopes) || [];
                output({
                    result: "scopes",
                    scopes: scopes.map((s) => ({
                        name: s.name,
                        ref: s.variablesReference,
                        expensive: s.expensive,
                    })),
                });
                break;
            }

            case "variables": {
                const resp = await dapRequest("variables", {
                    variablesReference: cmd.ref,
                });
                const vars = (resp.body && resp.body.variables) || [];
                output({
                    result: "variables",
                    variables: vars.map((v) => ({
                        name: v.name,
                        value: v.value,
                        type: v.type,
                        ref: v.variablesReference,
                    })),
                });
                break;
            }

            case "threads": {
                const resp = await dapRequest("threads", {});
                const threads = (resp.body && resp.body.threads) || [];
                output({
                    result: "threads",
                    threads: threads.map((t) => ({ id: t.id, name: t.name })),
                });
                break;
            }

            case "disconnect": {
                try {
                    await dapRequest("disconnect", {
                        terminateDebuggee: true,
                    }, 5000);
                } catch (_) { /* ignore timeout on disconnect */ }
                output({ result: "disconnected" });
                setTimeout(() => process.exit(0), 500);
                break;
            }

            default:
                output({ error: "Unknown command: " + cmd.cmd });
        }
    } catch (e) {
        output({ error: e.message });
    }
});

rl.on("close", () => {
    try { proc.kill(); } catch (_) { }
    process.exit(0);
});
