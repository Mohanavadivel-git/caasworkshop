## Building A Sample Application

This lesson will focus on building a sample application from which we will build a container image. 

### Exercise

1. Open a terminal and navigate to the samples directory you cloned in the [Workstation Setup](../workstation-setup.md#samples-repository). 

```bash
$ cd <LOCATION_OF_SAMPLES_REPO>
$ ls
best-practices.md  DTaaS  http-echo  leap  mailx  perl  python  README.md  simple_nodejsapp  springboot  toolbox  workshop
```

2. For the workshop, we will use the `workshop` directory, which contains a sample Springboot application. To do so, we need to build the application using `gradlew clean build`. 

> Note: For this sample app, you will need to point your `JAVA_HOME` environment variable to your JDK8 path. If you are currently using Java 10 or 11, see the [workstation setup](../workstation-setup.md#jdk-8) for instructions for getting JDK8. 

```bash
$ cd workshop
$ ./gradlew clean build
Starting a Gradle Daemon (subsequent builds will be faster)
...
BUILD SUCCESSFUL in 19s
7 actionable tasks: 7 executed
```

3. Check the contents of the `build/libs` directory. You should see the output `.jar` called `devenablement-service-helloworld.jar`. 

```bash
$ ls build/libs
devenablement-service-helloworld.jar
```

Now that we have our application build artifact, we can begin the process of building our container image to be deployed in CaaS. 

---

Continue to [Dockerfiles](./4-dockerfiles.md).

Return to [Table of Contents](../README.md#agenda)