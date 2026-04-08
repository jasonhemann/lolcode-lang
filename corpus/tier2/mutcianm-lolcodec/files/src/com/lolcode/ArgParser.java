package com.lolcode;

/**
 * Created with IntelliJ IDEA.
 * User: miha
 * Date: 7/24/13
 * Time: 8:01 PM
 */
public class ArgParser {
    public CompilerSettings settings = new BaseCompilerSettings();
    private static final String help = "Usage:\n" +
            "lolcodec.jar [options] <list of input files ...>\n" +
            "OPTIONS:\n" +
            "\t-h, --help\t\t\tShow this help\n" +
            "\t-Woff, --disable-warnings\tDisable all warnings\n" +
            "\t-j, --jar <file>\t\tPack result in a jar file\n" +
            "\t-o, --output-dir <dir>\t\tSet output directory\n" +
            "\t-c, --classpath <cp>\t\tSet classpath for produced classes\n" +
            "\t-e, --main-class <class>\tSet jar main class\n" +
            "\t-r, --runtime-lib <jarfile>\tSet lolcode runtime to link output jar\n" +
            "\t-d, --delete-class-files\tDelete produced class files after packing a jar\n";

    public ArgParser() {
    }

    public int parse(String[] args) {
        if (args.length == 0) {
            System.out.print(help);
            return 1;
        }
        for (int i = 0; i < args.length; i++) {
            String str = args[i];
            switch (str) {
                case "--help":
                case "-h":
                    System.out.print(help);
                    return 1;
                case "-Woff":
                case "--disable-warnings":
                    settings.setDisableWarnings(true);
                    break;
                case "-d":
                case "--delete-class-files":
                    settings.setDeleteClassFiles(true);
                    break;
                case "-j":
                case "--jar":
                    settings.setCreateJar(true);
                    if (!args[i+1].startsWith("-")) { // optional argument
                        settings.setOutputJarFile(args[i + 1]);
                        ++i;
                    }
                    break;
                case "-o":
                case "--output-dir":
                    settings.setOutputDir(args[i + 1]);
                    ++i;
                    break;
                case "-c":
                case "--classpath":
                    settings.setOutputClassPath(args[i + 1]);
                    ++i;
                    break;
                case "-e":
                case "--main-class":
                    settings.setJarMainClass(args[i + 1]);
                    ++i;
                    break;
                case "-r":
                case "--runtime-lib":
                    settings.setRuntimeJar(args[i+1]);
                    ++i;
                    break;
                default:
                    settings.addInputFile(str);
            }
        }
        return 0;
    }
}
