## Building a Container Image Using BuildConfigs

In the next lessons, we will walk through an example `BuildConfig` and then one for our application. 

---

## BuildConfig Overview

`BuildConfigs` are an Openshift specific object that allow the building of container images within the cluster. There are various ways of setting up `BuildConfig` configurations, inputs, outputs, strategies, etc. of which we will review a few. See the [Openshift DevGuide](https://docs.openshift.com/container-platform/4.1/builds/understanding-buildconfigs.html) for more information on `BuildConfigs`. 

### Inputs

There are a variety of different inputs that `BuildConfigs` accept. The simple way that we will be using is directly providing a `Dockerfile` within the `BuildConfig`.

Another way to provide an input for a `BuildConfig` is through GitHub. This does require extra steps (which will be discussed later in the workshop) to setup the authenitcation with GitHub. When set up, the `BuildConfig` can then clone your repository and will have access to your code. Most importantly, it can have access to a `Dockerfile` that you provide in the GitHub repository. 

### Strategy

There are two types of strategies that are available in CaaS: Docker and Source. 

Docker strategies are what we will use in the workshop, which is when a `Dockerfile` is provided. A source strategy, called a `Source-to-Image` (S2I) build, simply takes as input your source code.

### Outputs

The output of a `BuildConfig` is a container image. That container image will be stored in Quay. The container image can be output to other locations other than Quay, but for images deployed to Openshift, Quay is the preferred container image store. 

### Triggers

A `BuildConfig` can be triggered in various ways. The most common way to trigger a `BuildConfig` would be from a Github webhook so that a code change could trigger a new build. A `BuildConfig` can also be triggered off a change in the base image. That would require setting up an `ImageStream`, which will be covered later. 

---

Continue to [example build configs](./8-buildconfig.md).

Return to [Table of Contents](../README.md#agenda)