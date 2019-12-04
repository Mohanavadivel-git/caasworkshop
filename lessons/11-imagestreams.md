## Image Streams

An `ImageStream` object acts as a pointer to Quay. It polls Quay and receives updates whenever a specific tag in Quay is updated. You will notice that our image tag in the `Deployment` is hardcoded (line 57). `ImageStreams` allow us to abstract this information and automatically re-deploy our application when a new image is posted to Quay. 

---

1. Open the `image-stream.yaml` file. Replace <CDSID> with your CDSID. 

2. Deploy the `ImageStream` object. 

```bash
$ oc create -f ./manifests/image-stream.yaml
```

3. Go to the [image streams](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/images) section in Openshift. Notice how the SHA256 tag is the same as the one in Quay for your image.

4. Anytime now that the URL provided to Quay is updated with a new image, the `ImageStream` object will get updated with the new image. We can now introduce a new object called a `DeploymentConfig`, which uses our `ImageStream` to deploy our container image. 

---  

Continue to [Openshift console and CLI](./12-deploymentconfig.md).

Return to [Table of Contents](../README.md#agenda)
