package com.lolcode;

import java.util.ArrayList;
import java.util.List;

public class BaseCompilerSettings implements CompilerSettings {
    private boolean disableWarnings = false;
    private String outputClassPath = "";
    private String outputDir = "./";
    private boolean createJar = false;
    private List<String> inputFiles = new ArrayList<>();
    private String jarMainClass;
    private String outJarFile;
    private String runtimeJar = "runtime.jar";
    private boolean deleteClassFiles = false;

    private String pathToUnitName(String path) {
        int pos = path.lastIndexOf('/');
        if (pos == -1)
            pos = 0;
        return path.substring(pos).replace(".lol", "").replace(".", "_");
    }

    @Override
    public void verify() throws ConfigurationException {
        if (inputFiles.size() == 0)
            throw new ConfigurationException("No input files specified");
        if (createJar && (inputFiles.size() > 1) && (jarMainClass == null))
            throw new ConfigurationException("Unable to set main class for jar file when compiling multiple files.\nSet main class with \'-e\' switch");
        if (!runtimeJar.endsWith(".jar"))
            throw new ConfigurationException("Runtime library must be jar file");
        if (createJar && (outJarFile == null))
            outJarFile = pathToUnitName(inputFiles.get(0)) + ".jar";
    }

    @Override
    public boolean isDisableWarnings() {
        return disableWarnings;
    }

    @Override
    public void setDisableWarnings(boolean disableWarnings) {
        this.disableWarnings = disableWarnings;
    }

    @Override
    public String getOutputClassPath() {
        return outputClassPath;
    }

    @Override
    public void setOutputClassPath(String outputClassPath) {
        if (outputClassPath.equals("."))
            return;
        this.outputClassPath = outputClassPath.replace('.', '/');
        if (!this.outputClassPath.endsWith("/")) {
            this.outputClassPath += '/';
        }
    }

    @Override
    public boolean isDeleteClassFiles() {
        return deleteClassFiles;
    }

    @Override
    public void setDeleteClassFiles(boolean deleteClassFiles) {
        this.deleteClassFiles = deleteClassFiles;
    }

    @Override
    public String getRuntimeJar() {
        return runtimeJar;
    }

    @Override
    public void setRuntimeJar(String runtimeJar) {
        this.runtimeJar = runtimeJar;
    }

    @Override
    public String getOutputDir() {
        return outputDir;
    }

    @Override
    public void setOutputDir(String outputDir) {
        this.outputDir = outputDir;
        if (!this.outputDir.endsWith("/")) {
            this.outputDir += "/";
        }
    }

    @Override
    public boolean isCreateJar() {
        return createJar;
    }

    @Override
    public void setCreateJar(boolean createJar) {
        this.createJar = createJar;
    }

    @Override
    public List<String> getInputFiles() {
        return inputFiles;
    }

    @Override
    public void setInputFiles(List<String> inputFiles) {
        this.inputFiles = inputFiles;
    }

    @Override
    public void addInputFile(String filename) {
        inputFiles.add(filename);
    }

    @Override
    public void setJarMainClass(String className) {
        jarMainClass = className;
    }

    @Override
    public String getJarMainClass() {
        return jarMainClass;
    }

    @Override
    public void setOutputJarFile(String name) {
        outJarFile = name;
    }

    @Override
    public String getOutputJarFile() {
        return outJarFile;
    }
}
