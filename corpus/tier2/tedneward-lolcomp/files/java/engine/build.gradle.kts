plugins {
    // Apply the java-library plugin for API and implementation separation.
    `java-library`
    'antlr'
}

repositories {
    // Use Maven Central for resolving dependencies.
    mavenCentral()
}

dependencies {
    // Local dependencies (aka our ANTLR-generated code)
    implementation fileTree(dir: 'lib', include: '*.jar')

    antlr "org.antlr:antlr4:4.10.1"
    
    // Use JUnit Jupiter for testing.
    testImplementation("org.junit.jupiter:junit-jupiter:5.8.2")

    // This dependency is exported to consumers, that is to say found on their compile classpath.
    api("org.apache.commons:commons-math3:3.6.1")

    // This dependency is used internally, and not exposed to consumers on their own compile classpath.
    implementation("com.google.guava:guava:31.0.1-jre")
}

tasks.named<Test>("test") {
    // Use JUnit Platform for unit tests.
    useJUnitPlatform()
}
