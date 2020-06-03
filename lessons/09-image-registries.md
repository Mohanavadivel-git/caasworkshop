# Container Image Registries

This lesson focuses on understanding container image registries. At Ford, we use a tool called Quay to provide an on-premise registry to store images. If you are familiar with Docker Hub on the public internet, Quay is similar. The production instance of Quay is at https://registry.ford.com/.

---

## Quay

Quay is Ford's container image registry. All the images you build should be stored in Quay. The format in Quay follows an Organization → Repository style. For your organization, you may have one or more repositories.

Any single repository corresponds to a single application's container image. You may keep your version history within Quay as well to allow for rollbacks.

To be able to push container images to Quay you will need to provide authentication. Quay has a version of generic accounts called "robots" that can be maintained by the owner of a repository.

<!-- You can see [this page]() on the dev guide for how to create and use robot's in Quay. -->

### Workshop Secret

A robot account was created for the workshop repository. This robot has read and write access to the workshop repository. This will allow you to create and push container images to this repository and deploy. You will notice the `BuildConfig` object reference a secret called `devenablement-workshop-pull-secret`. This is the robot account for the workshop repository in Quay, which gives us access to write images to this repository.

## RedHat

You may also find that you need to authenticate against RedHat's container catalog to use their images. In this class, you will notice the `FROM` statement of the `Dockerfile` is from RedHat's registry, not Quay. To be able to authenticate against RedHat's registry in your namespace, you need a RedHat developer and service account (which is free to sign up for). Go to [here](./RedhatSvrAcct.md) for details on how to do it.

For the purpose of the workshop, this credential has already been created and we will be able to use it to utilize RedHat's container catalog, which you can view [here](https://registry.redhat.io).

### Requesting Quay Access

App teams that need access to Quay can request it using these [instructions](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#quay-on-boarding.)

---

Continue to [Deployments](./10-deployment.md).

Return to [Table of Contents](../README.md#agenda)
