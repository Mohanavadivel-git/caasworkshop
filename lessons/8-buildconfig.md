## Building a Container Image Using BuildConfigs

In this lesson we will deploy a test `BuildConfig` and the `BuildConfig` for sample application. 

---

**Note**: You need the [Openshift CLI](../workstation-setup.md#oc-cli)

## Exercise - Test BuildConfig

1. Navigate to the directory you cloned the samples repository. Open the `workshop` directory. 

2. Open `build-config-1.yaml` in a text editor (Visual Studio Code, Notepad++, etc). 

3. Replace the parts that say <CDSID> with your CDSID (lines 4 and 11).

4. In your terminal window, ensure you are still at the root of the `workshop` directory. 

5. Create the `BuildConfig` object using the following command: 

```bash
$ oc create -f ./manifests/build-config-1.yaml
buildconfig.build.openshift.io/example-dvncaas created
```

6. Start the build. You can do this via the console or from the terminal. 

Console: 

- Go to [builds](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/builds) section. 
- Click on your build. 
- On the far right, click "start build"

Terminal: 

- Replace <MY-CDSID> with your CDSID

```bash
$ oc start-build example-<MY-CDSID> --wait=true
```

## Exercise - Sample Application BuildConfig



---

Continue to [container image registry](./7-buildconfigs.md).

Return to [Table of Contents](../README.md#agenda)