## Overivew

## The Big Picture

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This image represents a high level overview of developing applications for CaaS. The workshop will go over all of these topics in some fashion. 

## CaaS Objects Overview 

There are various ways to build and deploy container images. This workshop focuses on a specific, best-practice way of building and deploying container images through use of automation. First, we will discuss the necessary Openshift objects to build and deploy container images at a high level. 

![CaaS Workflow](../images/overview.png)

- Source Code
    - Your source code/build artifacts can be sent to CaaS in various ways. You can achieve this through GitHub or through your local machine. Your choice will require different configurations to be set up.
- [BuildConfig](https://docs.openshift.com/container-platform/4.2/builds/understanding-image-builds.html)
    - Takes as input a combination of source code, application artifacts (.jar, .zip, etc), and Dockerfiles.
    - Outputs a container image to a container image registry
- [Quay](https://registry.ford.com/)
    - Ford's container image registry
    - Can store history of container images
    - Customizable credentials used to write and read images from the registry
- [ImageStreams](https://docs.openshift.com/container-platform/4.2/openshift_images/image-streams-manage.html)
    - Listener for an image in a container image registry  
    - Updated whenever the image is updated
- [DeploymentConfig](https://docs.openshift.com/container-platform/4.2/applications/deployments/what-deployments-are.html)
    - Handles actual deployment of application 
    - Can be triggered based on image updates (i.e. when the `ImageStream` is updated)
    - Handles bringing up new instances and scaling down old instances of the application 

---

Continue to [Openshift console](./3-console.md).

Return to [Table of Contents](../README.md#agenda)
