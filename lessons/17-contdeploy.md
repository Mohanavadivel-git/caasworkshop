# Continuous Deployment

As you can see from the sample deployment, image changes need to be constantly updated in the deployment and then applied. The Dev Enablement team recommends using Jenkins to handle your continuous delivery. We have a sample pipeline for applications using AccuRev and Ant for and we can provide advice for teams looking to build pipelines for other tool sets.

Alternatively, you can use some OpenShift specific objects to handle some forms of continuous delivery. There are some limitations to these OpenShift objects when compared to Jenkins. The biggest being limitations around configuring how frequently `ImageStreams` check for updates.

**Note**: Like `BuildConfigs`, the following objects (`ImageStreams` and `DeploymentConfigs`) are OpenShift specific. The other objects, such as `Deployments`, `Routes`, `Services`, etc. can be lifted and shifted to any other Kubernetes orchestration system. Keep that under consideration when using OpenShift-specific objects.

---

## ImageStreams

An `ImageStream` object acts as a pointer to Quay. It polls Quay and receives updates whenever a specific tag in Quay is updated. You will notice that our image tag in the `Deployment` is hard-coded (line 58). `ImageStreams` allow us to abstract this information and automatically re-deploy our application when a new image is posted to Quay.

1. Open the `image-stream.yaml` file. Replace `<CDSID>` with your CDSID.

2. Deploy the `ImageStream` object.

```bash
$ oc create -f ./manifests/image-stream.yaml
```

3. Go to the [image streams](https://console-openshift-console.apps.pd01.edc.caas.ford.com/k8s/ns/devenablement-workshop-dev/imagestreams) section in OpenShift. You should see a stream with your CDSID. If you click on it you will see the **From** section pointing to your image in the workshop repository.

4. Now whenever the URL provided to Quay is updated with a new image, the `ImageStream` object will get updated with the new image. We can now introduce a new object called a `DeploymentConfig`, which uses our `ImageStream` to deploy our container image.

## DeploymentConfigs

A `DeploymentConfig` is different than a `Deployment`. A `DeploymentConfig` spins up a `ReplicationController` which manages a certain number of pod replicas. What we will do is set up a trigger in our `DeploymentConfig` so that every time our image is updated in Quay, a new `ReplicationController` will be automatically created by the `DeploymentConfig` and will deploy our new image.

1. Open the `deploymentconfig.yaml` file. Replace <CDSID> with your CDSID.

2. Deploy the `DeploymentConfig` object.

```bash
$ oc create -f ./manifests/deploymentconfig.yaml
```

3. Go to the [deployments](https://console-openshift-console.apps.pd01.edc.caas.ford.com/k8s/ns/devenablement-workshop-dev/deploymentconfigs) section in OpenShift. We can watch the logs and the pods to see how the `DeploymentConfig` spins up a `ReplicationController` which spins up our pods.

---

Continue to [End to End Example](./18-endtoend.md).

Return to [Table of Contents](../README.md#agenda)
