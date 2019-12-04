# The Big Picture

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This image represents a high level overview of developing applications for CaaS. The workshop will go over all of these topics in some fashion. 

## Application Code

You application code (generally) will not change. You might make some tweaks to you application preferences, but generally, you will still need to produce an application artifact (a .jar, .zip, etc) from your application code.  

## Dockerfile

A `Dockerfile` is a list of commands that are used to assemble a container image. It is here you will specify all the necessary tools that are needed to run your application. For example, to run a basic python application, your Dockerfile would provide the instructions to download python and pip (a package isntaller for python). We look more at `Dockerfiles` in a later lesson. 

## Building Container Image

Since a `Dockerfile` is simply a set of instructions for building your container image, you still need to build the image itself. There are numerous ways to do this that will be discussed in a later lesson. 

## Storing Container Image

Once you build a container image, you need to store it somewhere. Similarly to storing code in GitHub, container images are stored in a repository. CaaS provides a container image registry called Quay where you can have repositories of images. Every image you want to deploy to CaaS must be first stored in Quay. 

## Deploying Container Image

Once your container image is stored in Quay, you can then deploy it to CaaS. There are numerous ways to do this, as well as a strategy to automatically handle it. We will look at those methods in a later lesson. 

## Testing 

There are different methods of testing that can be employed before, during, and after the deployment of your container image. Your unit and code level tests should still occur as normal, prior to building your container image. Kubernetes (and by extension, CaaS) allows you to have health tests during the deployment of your application. Finally, you can run smoke tests on live versions of your application. You can have multiple environments in CaaS to do your testing (e.g DEV, QA, PROD). 

## Monitoring

Some monitoring is provided out of the box with CaaS where you can view the memory and cpu consumption of your containers. Future monitoring systems will be put in place that offer more in-depth monitoring capabilities. 

---

Continue to [overview](./3-application.md).

Return to [Table of Contents](../README.md#agenda)