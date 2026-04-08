package com.lolcode;

import java.util.List;

public interface CompilerSettings {

    void verify() throws ConfigurationException;

    boolean isDisableWarnings();

    void setDisableWarnings(boolean disableWarnings);

    String getOutputClassPath();

    void setOutputClassPath(String outputClassPath);

    boolean isDeleteClassFiles();

    void setDeleteClassFiles(boolean deleteClassFiles);

    String getRuntimeJar();

    void setRuntimeJar(String runtimeJar);

    String getOutputDir();

    void setOutputDir(String outputDir);

    boolean isCreateJar();

    void setCreateJar(boolean createJar);

    List<String> getInputFiles();

    void setInputFiles(List<String> inputFiles);

    void addInputFile(String filename);

    void setJarMainClass(String className);

    String getJarMainClass();

    void setOutputJarFile(String name);

    String getOutputJarFile();
}
