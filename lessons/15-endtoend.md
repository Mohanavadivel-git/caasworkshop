## End to End Test

<p align="center">
  <img src="../images/overview.png" width="850" height="450">
</p>

Now that we've introduced a number of concepts and objects, let's make a code change. After we make the code change, we will start our build and see that Openshift handles everything afterwards automatically.

### Change Code

1. Let's revert our changes from earlier. Remove the `-v2` in `build-config-2.yaml` (line 11) so that our tag is back to just being our CDSID. 

2. Change the value(s) of line 26, 27, 28 to whatever message you'd like in the quoted sections for the `SUMMARY`, `DESCRIPTION`, and `NAME` environment variables. **Do not** remove the `\` at the end of lines 26 and 27. 

3. Apply the changes to your build config. 

```bash
$ oc apply -f ./manifests/build-config-2.yaml
```

### Build New Image

4. Let's start a new build with our new code, which will result in a new container image deployed to Quay

```bash
$ oc start-build app-build-<CDSID> --from-dir=./ --wait=true
Uploading directory "build\\libs" as binary input for the build ...
......
Uploading finished
build.build.openshift.io/app-build-<CDSID>-4 started
```

### Point Service to DeploymentConfig

5. In order for us to see the updated code at the URL we created, we need to change the `Service` to point to the `DeploymentConfig` rather than the `Deployment` we were using earlier.

   Open `./manifests/service.yaml` and append `-config` to line 10, so it reads:
   ```yaml
   app: <CDSID>-deployment-config
   ```

6. Apply the new `Service` configuration to the cluster.

```bash
$ oc apply -f ./manifests/service.yaml
```

### Watch Updates

7. Go to the [image streams](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/images) section in Openshift. It may take up to 15 minutes for the `ImageStream` to detect the updated image in Quay.

8. Once you see that your `ImageStream` has updated, go to the [deployments](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/deployments) section in Openshift and select your `DeploymentConfig`. We can now watch the process of the `DeploymentConfig` doing the following steps:

- Bringing up your new deployment in the background
- Ensuring your deployment passes its probes
- Scale down and delete your old deployment
- Make the new deployment the actively running deployment

9. When these steps are made, your can go to your route (MY-CDSID.app.caas.ford.com) and see your new greeting.

---

Continue to [volumes](./16-volumesintro.md).

Return to [Table of Contents](../README.md#agenda)
