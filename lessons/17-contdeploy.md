# Continuous Deployment

As you can see from the sample deployment, to reflect code updates the image changes need to be constantly updated in the deployment and then applied.
The Dev Enablement team recommends using Jenkins to handle your continuous delivery.
We have a sample pipeline for applications using AccuRev and Ant and we can provide advice for teams looking to build pipelines for other tool sets.
What we will cover next are underlying OpenShift commands used with the Jenkins deployment approach that we have propagated to teams.

There are OpenShift-specific objects (`ImageStreams` and `DeploymentConfigs`) that can be used to provide continuous deployment.
But there are some limitations to them so we have opted to not promote their use.

An `ImageStream` object acts as a pointer to Quay. It polls Quay and receives updates whenever a specific tag in Quay is updated.
You will notice that our image tag in the `Deployment` is hard-coded (line 58). `ImageStreams` allow us to abstract this information and automatically
re-deploy our application when a new image is posted to Quay.

The main limitation of `ImageStreams` is the amount of time you are required to wait before new images are polled from Quay. It can take up to
15 minutes for a new image to be detected and deployed, and unfortunetly this time period is only configurable at cluster level.

The second limitation is the fact that `ImageStreams` and `DeploymentConfigs` are OpenShift specific objects. The more of these you adopt the
less portable your pipeline becomes. We are already using `BuildConfigs` which are OpenShift specific, but since we have a way to implement continuous deployment
using those and `Deployments` or `StatefulSets` alone (the approach shown below works with both) we don't currently see a need for adopting
use of these other objects.

## Example

Let's make a code change and see how we can get our updates deployed to the platform in a repeatable way that would be similar to an approach
used when adopting a CI/CD pipeline. To do this we will use a template. Templates can be used to let you parameterize the contents of a
Kubernetes object's YAML file. You can specify the values of your parameters in a parameter file and they will be merged into the
resulting YAML when you **process** the template. In this exercise we will be parameterizing our build config with template `build-config-template.yaml`.

### Change Code

1. Open `build-config.env` with a text editor and change `<CDSID>` to your CDSID. 

2. Change `<QUAY_IMAGE_TAG>` to your CDSID-v3. In CI/CD systems you usually have an automated version number generated each time there is a build.
When implementing CI/CD you would want to feed that version number into your build config to tag your new image in Quay with it.  

3. Process the template and apply the resulting changes to your build config. We will be using the same build config as before: app-build-CDSID

```bash
$ oc process -f ./manifests/build-config-template.yaml --param-file=./manifests/build-config.env | oc apply -f -
```

### Build New Image

4. Let's start a new build that will use our updated build config, which will result in a new container image stored in Quay

```bash
$ oc start-build app-build-<CDSID> --from-dir=./ --wait=true
Uploading directory "." as binary input for the build ...
.
Uploading finished
build.build.openshift.io/app-build-<CDSID>-4 started

```

You can go to [quay](https://registry.ford.com/repository/devenablement/workshop?tab=tags) and see your new image.

### Update Deployment to Use New Image

5. In order for us to use our new image we have to update our Deployment to reference it.

```bash
$ oc set image deployment/<CDSID>-deployment <CDSID>-deployment=registry.ford.com/devenablement/workshop:<CDSID>-v3
```

### Watch Updates

6. Go to the [pods](https://console-openshift-console.apps.pd01.edc.caas.ford.com/k8s/ns/devenablement-workshop-dev/pods) section in OpenShift. You will see the platform:

- Bring up a new pod running the code in your latest image
- Ensuring it passes its probes
- Terminate the old pod

7. When these steps are complete, you can go to your route (https://MY-CDSID.apps.pd01.edc.caas.ford.com) and see the latest version of your app which should just say Hello CDSID
with your CDSID having been set in the build config via the parameter in `build-config.env`. 

---

Continue to [Continuous Integration](./18-contint.md).

Return to [Table of Contents](../README.md#agenda)
