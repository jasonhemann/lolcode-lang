version: 1.0.0
name: slopbucket_special
description: >
  Max‑allowed banter pack for ALNFantasia and mature sandbox contexts.
  Links phrase pools, procedural generators, and compliance policies.

contexts:
  allowed:
    - adult
    - mature
    - test_sandbox
  blocked:
    - child
    - pg13
    - public_unrated

assets:
  pools:
    - id: core_vulgar
      path: alnfantasia/dialogue/slopbucket_banter.create
      tags: [insult, vulgar, quick_hit]
    - id: roast_strings
      path: alnfantasia/dialogue/slopbucket_roasts.create
      tags: [scene, cinematic, roast]
    - id: banter_bursts
      path: alnfantasia/dialogue/slopbucket_bursts.create
      tags: [combat, reactive, short]
  generators:
    - id: max_banter_burst
      path: alnfantasia/banter/max_banter.aln
      triggers: [on_taunt, npc_banter_window]
      input: [player, npc, context]
      output: banters[random_index()]
  policies:
    - id: banter_context_guard
      path: bit.hub/policy/alnfantasia_banter.rego
      package: alnfantasia.dialogue

compliance:
  railguards:
    - deny_if: context not in contexts.allowed
    - log_all: true
    - moderation_hooks: true
