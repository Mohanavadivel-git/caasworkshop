## Deploying Apps to Ford's CaaS Platform

This is a hands-on, training workshop to get application development teams started in Ford's Container as a Service platform.

![OpenShift Logo](images/OpenShift_Logo.svg)

This workshop will provide instructions to build application container images, then deploying these images to the CaaS platform. Workshop participants will experience deploying a sample application to the CaaS environment from their workstation. 

## Setup

- Install the required software on your laptop **prior** to the class. See the [workstation setup guide](workstation-setup.md). 
- Login to https://api.caas.ford.com/ with your CDSID and password. You should be able to log in and see the `devenablement-workshop-dev` namespace. **DO NOT** deploy/create objects until the workshop.

## Agenda

1. [Introduction](./lessons/1-introduction.md)
1. [Application Code and Mounting Directories](./lessons/2-development.md)
1. [Intro to Dockerfiles](./lessons/3-application.md)
1. [Building Images in Localdev](./lessons/4-dockerfiles.md)
1. [Container Image Registry](./lessons/5-console.md)
1. [Openshift Console and CLI](./lessons/6-buildtools.md)
1. [Intro to Openshift Objects](./lessons/7-buildintro.md)
1. [Intro to Openshift Manifests](./lessons/8-buildconfig.md)
1. [Deploying to Openshift](./lessons/9-quay.md)
1. [Intro to Volumes](./lessons/10-deployment.md)
1. [Volumes Exercise](./lessons/11-imagestreams.md)
1. [Saving Logs](./lessons/12-deploymentconfig.md)


## Schedule

The workshop is offered once per month. The duration is two 4-hour sessions offered typically on two consecutive days. It is currently offered for no charge.

To attend, sign up [here](https://it2.spt.ford.com/sites/dev/Lists/RegisterForEvent/newform.aspx).

## Begin Workshop

Begin with an [Overview of CaaS at Ford](https://it2.spt.ford.com/sites/dev/Documents/CaaS-At-Ford_Workshop.pptx) then [Lesson 1](./lessons/1-introduction.md).
