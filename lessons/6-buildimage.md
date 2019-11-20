## Building Container Images Using Dockerfiles

### The Big Picture - Step 3

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson will go over how build a container/OCI/docker image. These three names are used interchangeably when referring to images. 

---

### BuildConfigs - Introduction

There are numerous build tools that are used to build container images, such as Docker, Buildah, and Podman. You can install these tools on your system or use a virtual machine (such as [localdev]()). 

Openshift, however, provides a way to build container images within the cluster itself. This way, builds can be automated and never dependent on system tools. This is done through an Openshift-specific object called a `BuildConfig`. You can review the documentation for `BuildConfigs` [here](https://docs.openshift.com/container-platform/4.2/builds/understanding-image-builds.html). 

`BuildConfigs` allow you to define the necessary parameters to build your container image. This way, you can have a repeatable process and always build your container image the same way. 

### BuildConfigs - Sample

In this section, we will review a very basic `BuildConfig` to build an image which we will later overwrite. 

1. 



---  

Continue to [Container Registries](./5-quay.md).

Return to [Table of Contents](../README.md#agenda)