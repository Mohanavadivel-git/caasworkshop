## Building Container Images

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

1. Open `build-config-1.yaml` and review the file. 

- Metadata
  - Relevant metadata can be provided, with a name provided at minimum 
- Output
  - pushSecret: The name of the secret containing your Quay robot credentials
    - See [these instructions]() to create the robot credential
  - To: Location and tag of the output container
- Resources:
  - Resources to allocate for the build process
- Source:
  - Necessary input to complete the container image build
  - Can include but is not limited to: source code, Dockerfile, build artifact, etc. (this example uses an inline Dockerfile)

2. Replace the spots that say `<YOUR-CDSID>` with your CDSID. 

3. Using the terminal, let's create the `BuildConfig`. Ensure you are in the `workshop` directory. 

```bash
$ oc create -f ./manifests/build-config-1.yaml
buildconfig.build.openshift.io/example-dvncaas created
```

4. Start the build. You can do this via the console or from the terminal. 

Console: 

- Go to [builds](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/builds) section. 
- Click on your build. 
- On the far right, click "start build"

Terminal: 

- Replace <MY-CDSID> with your CDSID

```bash
$ oc start-build example-<MY-CDSID> --wait=true
```

---  
<!--oc import-image redhat-openjdk-18/openjdk18-openshift --from=registry.redhat.io/redhat-openjdk-18/openjdk18-openshift --confirm-->
Continue to [Container Registries](./5-quay.md).

Return to [Table of Contents](../README.md#agenda)