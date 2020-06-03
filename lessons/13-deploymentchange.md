# Deployment Changes

## Exercise - Change the Code

In this exercise, we will change a small part of the code and then re-build the image.

1. Re-open `build-config-2.yaml`.

2. Change line 11. Replace your CDSID at the end of the line with CDSID-v2. Example: `registry.ford.com/devenablement/workshop:malyass` → `registry.ford.com/devenablement/workshop:malyass-v2`.

3. Line 28 reads `NAME=World`. Change `World` to be your CDSID.

4. Apply the changes to your build config with the following command:

```bash
$ oc apply -f ./manifests/build-config-2.yaml
buildconfig.build.openshift.io/app-build-<CDSID> configured
```

5. Start your build by running the following command:

```bash
$ oc start-build app-build-<CDSID> --from-dir=./ --wait=true
Uploading directory "." as binary input for the build ...
......
Uploading finished
build.build.openshift.io/app-build-<CDSID>-3 started
```

## Exercise - Apply Image Change

1. When you build is successful, re-open `deployment.yaml`.

2. Change line 58 to reference your new image with the same tag you applied to the `BuildConfig`. (i.e `<CDSID>` to `<CDSID>-v2`)

3. Apply the changes to your deployment with the following command:

```bash
$ oc apply -f ./manifests/deployment.yaml
deployment.apps/malyass-deployment configured
```

4. Due to a configuration change, your deployment will begin creating a new pod with your new image. You can view the `Deployments` section in the console. You can also go to your route and repeatedly refresh. You will be able to see how your application changes are deployed without any downtime.

---

Continue to [continuous delivery](./14-contdeploy.md).

Return to [Table of Contents](../README.md#agenda)
