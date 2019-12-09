## Building a Container Image Using BuildConfigs

In this lesson we will deploy a test `BuildConfig` and the `BuildConfig` for the sample application. 

---

**Note**: You need the [Openshift CLI](../workstation-setup.md#oc-cli)

## Exercise - Test BuildConfig

1. Navigate to the directory you cloned the samples repository. Open the `workshop` directory. 

2. Open `build-config-1.yaml` in a text editor (Visual Studio Code, Notepad++, etc). 

3. Replace the parts that say `<CDSID>` with your CDSID (lines 4 and 11).

4. In your terminal window, ensure you are still at the root of the `caas-workshop` directory. 

5. Navigate to the `application` directory. This is the directory we will be working out of for all of the examples. 

```bash
$ cd ./application
$ ls
Dockerfile  manifests/  README.md  src/
```

6. Create the `BuildConfig` object using the following command: 

```bash
$ oc create -f ./manifests/build-config-1.yaml
buildconfig.build.openshift.io/test-build-<CDSID> created
```

7. Start the build. You can do this via the console or from the terminal.

Console: 

- Go to [builds](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/builds) section. 
- Click on your build. 
- On the far right, click "start build"

Terminal: 

- Replace `<CDSID>` with your CDSID

```bash
$ oc start-build test-build-<CDSID> --wait=true
build.build.openshift.io/test-build-<CDSID>-1 started
```

8. When the build is completed, we can view the image [in Quay](https://registry.ford.com/repository/devenablement/workshop?tab=tags). 


## Exercise - Sample Application BuildConfig

1. Open `build-config-2.yaml` in a text editor (Visual Studio Code, Notepad++, etc). 

2. Replace the parts that say `<CDSID>` with your CDSID (lines 4 and 11).

3. Create the `BuildConfig` object in the same fashion: 

```bash
$ oc create -f ./manifests/build-config-2.yaml
buildconfig.build.openshift.io/example-dvncaas created
```

4. Start the build in the same way either through the console or the command line. 

```bash
$ oc start-build app-build-<CDSID> --wait=true
build.build.openshift.io/app-build-<CDSID>-1 started
```

5. Notice that this build failed. That's because our `Dockerfile` is expecting our `src` directory. What we can do is pass along our `src` directory to the `BuildConfig` object, and we can do this from the command line. 

```bash
$ oc start-build app-build-<CDSID> --from-dir=./ --wait=true
Uploading directory "." as binary input for the build ...
......
Uploading finished
build.build.openshift.io/app-build-<CDSID>-2 started
```

6. When the build is completed, we can view the image [in Quay](https://registry.ford.com/repository/devenablement/workshop?tab=tags). Notice the image is now larger than our first image because it contains our application code and the larger, python base image. 

---

Continue to [container image registry](./9-quay.md).

Return to [Table of Contents](../README.md#agenda)