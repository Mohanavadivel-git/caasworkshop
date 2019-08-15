## Advanced Topics

There are a number of topics that will not be covered as part of the training that you will encounter on your journey to CaaS. Our team is available to help if you get stuck or face issues along the way. 

### BuildConfigs

You can build a container image in Openshift and automate the process of building your images. This is defined with a [build config](https://docs.openshift.com/container-platform/3.11/dev_guide/builds/index.html) object. You provide your source code or Dockerfile and the location to push the image (Quay). You can also set up triggers so that the builds begin automatically whenever you make a change to your code or to your Dockerfile. 

### ImageStreams 

In a similar fashion, you can abstract the referencing of your container images. Rather than having to deploy a new image every time it is created, the image stream and its tags provide a way to automate the process. Your deployments can listen for notifications on the image stream and when the image stream detects a new image version in your repository, it will trigger your deployment to deploy your new image. 

### Jenkins

You can also utilize Jenkins for the build and deployment of your containers. The Dev Enablement team will soon release a CI/CD pattern for Jenkins. 

---

You have reached the end of the workshop! :clap:

Return to [Table of Contents](../README.md#agenda)