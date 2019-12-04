## Deployment Config

A `DeploymentConfig` is different than a `Deployment`. A `DeploymentConfig` spins up `Deployments`. What we will do is set up a trigger in our `DeploymentConfig` so that every time our image is updated in Quay, a new `Deployment` will be automatically spun up by the `DeploymentConfig`. 

---

### Deploy Deployment Config

1. Open the `deploymentconfig.yaml` file. Replace <CDSID> with your CDSID. 

2. Deploy the `DeploymentConfig` object. 

```bash
$ oc create -f ./manifests/image-stream.yaml
```

3. Go to the [deployments](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/deployments) section in Openshift. Notice the separate section for `DeploymentConfigs`. We can watch the logs and the pods to see how the `DeploymentConfig` spins up a `Deployment` which spins up our pods. 

### Change Image

We will now change our image in Quay so that we can watch the process of a `DeploymentConfig` automatically change and spin up new pods. 

1. Open the `build-config-2.yaml` again. 

2. In the `Dockerfile` section, add an environment variable. You can copy and paste the following line and enter this between lines 22 and 23. 

```yaml
ENV TEST=hello
```

3. Let's restart our build, which will result in a new container image deployed to Quay. 

```bash
$ oc start-build app-build-<CDSID> --from-dir=./build/libs --wait=true
Uploading directory "build\\libs" as binary input for the build ...
......
Uploading finished
build.build.openshift.io/app-build-<CDSID>-2 started
```

---  

Return to [Table of Contents](../README.md#agenda)
