package com.lolcode;

public class Main {

    public static void main(String[] args) {
        ArgParser parser = new ArgParser();
        parser.parse(args);
        Runner runner = new Runner(parser.settings);
        runner.run();
    }
}
