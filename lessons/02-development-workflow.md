# Development Workflow

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This image represents a high level overview of developing applications for CaaS. The workshop will go over all of these topics in some fashion.

## Application Code

You might make some tweaks to you application preferences, but you will still need your source code or an application artifact to build your container image.

## Dockerfile

A `Dockerfile` is a list of commands used to assemble a container image. It is here you will specify all the necessary tools that are needed to run your application. For example, to run a basic Python application, your Dockerfile would provide the instructions to download Python and `pip` (a package installer for Python).

## Building Container Image

Since a `Dockerfile` is simply a set of instructions for building your container image, you still need to build the image itself. There are numerous ways to do this that will be discussed in a later lesson.

## Storing Container Image

Once you build a container image, you need to store it somewhere. Similarly to storing code in GitHub, container images are stored in a repository. CaaS provides a container image registry, called Quay, where you can have repositories of images. Every image you want to deploy to CaaS must be first stored in Quay.

## Deploying Container Image

Once your container image is stored in Quay, you can then deploy it to CaaS. There are numerous ways to do this, as well as strategies to help automate the process.

## Testing

There are different methods of testing that can be employed before, during, and after the deployment of your container image. Your unit and code level tests should still occur as normal, prior to building your container image. Kubernetes (and by extension, CaaS) allows you to have health tests during the deployment of your application. Finally, you can run smoke tests on live versions of your application. You can have multiple environments in CaaS to do your testing (i.e DEV and QA environments)

## Monitoring

Some monitoring is provided out of the box with CaaS where you can view the memory and cpu consumption of your containers. Future monitoring systems will be put in place that offer more in-depth monitoring capabilities.

---

Continue to [cloning sample application](./03-application.md).

Return to [Table of Contents](../README.md#agenda)
