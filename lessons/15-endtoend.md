## End to End Test

Now that we've introduced a number of concepts and objects, let's make a code change. After we make the code change, we will start our build and see that Openshift handles everything afterwards automatically.

### Change Code

1. Open the `HelloController.java` file located in `src/main/java/com/ford/devenablement/helloworld/hello/api/`

2. In line 24, change `Hello` to your name or some other message. Copy this message when you are done. 

3. After changing our code, we need to make sure our tests pass. Open `HelloControllerIntegrationTest.java` located in `test/java/com/ford/devenablement/helloworld/hello`. Change line 52 from `Hello` to your message. 

4. Open `HelloControllerTest.java` also located in `test/java/com/ford/devenablement/helloworld/hello`. Change line 31 from `Hello` to your message. 

5. Open `HelloAcceptanceTest.java` located in `test/java/com/ford/devenablement/helloworld/acceptance/hello`. Change line 28 from `Hello` to your message.

6. We need to rebuild our application, so run the command below to use gradle to build our application again with the code changes. 

```bash
$ ./gradlew clean build
Starting a Gradle Daemon (subsequent builds will be faster)
...
BUILD SUCCESSFUL in 19s
7 actionable tasks: 7 executed
```

### Build New Image

7. Let's start a new build with our new `.jar`, which will result in a new container image deployed to Quay

```bash
$ oc start-build app-build-<CDSID> --from-dir=./build/libs --wait=true
Uploading directory "build\\libs" as binary input for the build ...
......
Uploading finished
build.build.openshift.io/app-build-<CDSID>-2 started
```

### Watch Updates

8. Go to the [image streams](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/images) section in Openshift. It make take approximately 5 minutes for the `ImageStream` to receive the updated image in Quay. 

9. Once you see that your `ImageStream` has updated, go to the [deployments](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/deployments) section in Openshift and select your `DeploymentConfig`. We can now watch the process of the `DeploymentConfig` doing the following steps:

- Bringing up your new deployment in the background
- Ensuring your deployment passes its probes
- Scale down and delete your old deployment
- Make the new deployment the actively running deployment 

10. When these steps are made, your can go to your route (<CDSID>.app.caas.ford.com/api/v1/hello) and see your new greeting. 

---

Return to [Table of Contents](../README.md#agenda)