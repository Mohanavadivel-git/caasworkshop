# Continuous Deployment

As you can see from the sample deployment, image changes need to be constantly updated in the deployment and then applied. You can always use a tool to handle your continuous deployment (such as Jenkins). Alternatively, you can use some Openshift specific objects to handle some forms of continuous deployment. 

**Note**: Like `BuildConfigs`, the following objects (`ImageStreams` and `DeploymentConfigs`) are Openshift specific. The other objects, such as `Deployments`, `Routes`, `Services`, etc. can be lifted and shifted to any other Kubernetes orchestration system. Keep that under consideration when using Openshift-specific objects. 

---

## ImageStreams

An `ImageStream` object acts as a pointer to Quay. It polls Quay and receives updates whenever a specific tag in Quay is updated. You will notice that our image tag in the `Deployment` is hardcoded (line 57). `ImageStreams` allow us to abstract this information and automatically re-deploy our application when a new image is posted to Quay. 

1. Open the `image-stream.yaml` file. Replace `<CDSID>` with your CDSID. 

2. Deploy the `ImageStream` object. 

```bash
$ oc create -f ./manifests/image-stream.yaml
```

3. Go to the [image streams](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/images) section in Openshift. Notice how the SHA256 tag is the same as the one in Quay for your first image.

4. Anytime now that the URL provided to Quay is updated with a new image, the `ImageStream` object will get updated with the new image. We can now introduce a new object called a `DeploymentConfig`, which uses our `ImageStream` to deploy our container image. 

## DeploymentConfigs

A `DeploymentConfig` is different than a `Deployment`. A `DeploymentConfig` spins up `Deployments`. What we will do is set up a trigger in our `DeploymentConfig` so that every time our image is updated in Quay, a new `Deployment` will be automatically spun up by the `DeploymentConfig`. 

1. Open the `deploymentconfig.yaml` file. Replace <CDSID> with your CDSID. 

2. Deploy the `DeploymentConfig` object. 

```bash
$ oc create -f ./manifests/deploymentconfig.yaml
```

3. Go to the [deployments](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/deployments) section in Openshift. Notice the separate section for `DeploymentConfigs`. We can watch the logs and the pods to see how the `DeploymentConfig` spins up a `Deployment` which spins up our pods. 

---

Continue to [DeploymentConfigs](./15-imagestreams.md).

Return to [Table of Contents](../README.md#agenda)