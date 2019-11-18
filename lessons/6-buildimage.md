## Building Container Images Using Dockerfiles

### The Big Picture - Step 3

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson will go over how build a container/OCI/docker image. These three names are used interchangeably when referring to images. 

---

### Build Container Image In localdev

If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

### BuildConfigs - Introduction

There are numerous build tools that are used to build container images, such as Docker, Buildah, and Podman. You can install these tools on your system or use a virtual machine (such as [localdev]()). 

Openshift, however, provides a way to build container images within the cluster itself. This way, builds can be automated and never dependent on system tools. You can review the documentation for `BuildConfigs` [here](https://docs.openshift.com/container-platform/4.2/builds/understanding-image-builds.html). 

Behind the scenes, `BuildConfigs` uses `Buildah` to build your container image. 

### BuildConfigs - Parameters



---  

Continue to [Container Registries](./5-quay.md).

Return to [Table of Contents](../README.md#agenda)