## Deploying Apps to Ford's CaaS Platform

This is a hands-on, training workshop to get application development teams started in Ford's Container as a Service platform.

![OpenShift Logo](images/OpenShift_Logo.svg)

This workshop will provide instructions to build application container images, then deploying these images to the CaaS platform. Workshop participants will experience deploying a sample application to a local CaaS environment on their own workstation. In doing so, participants will learn how they can take the applications they build and deploy to Ford's CaaS platform.

## Agenda

1. [Introduction](./lessons/1-introduction.md)
1. [Application Code and Mounting Directories](./lessons/2-buildapp.md)
1. [Intro to Dockerfiles](./lessons/3-dockerfiles.md)
1. [Building Images in Localdev](./lessons/4-buildimage.md)
1. [Container Image Registry](./lessons/5-quay.md)
1. [Openshift Console and CLI](./lessons/6-console.md)
1. [Intro to Openshift Objects](./lessons/7-objects.md)
1. [Intro to Openshift Manifests](./lessons/8-manifest.md)
1. [Deploying to Openshift](./lessons/9-deploy.md)
1. [Intro to Volumes](./lessons/10-VolumesIntro.md)
1. [Volumes Exercise](./lessons/11-VolumesExercise.md)
1. [Saving Logs](./lessons/12-VolumeLogs.md)
1. [Kibana (Logging Aggregator)](./lessons/13-Kibana.md)
1. [Monitoring](./lessons/14-Monitoring.md)
1. [Vanity URLs](./lessons/15-VanityUrl.md)
1. [Advanced Topics](./lessons/16-AdvancedTopics.md)

## Pre-requisites and Equipment
<!-- 
- Your own developer-class laptop with minimal 4 CPU cores and 8GB of RAM. An underpowered laptop that is used mostly for checking email WILL NOT WORK.
- Install the required software on your laptop prior to class. [Instructions](workstation-setup.md) will be sent out to registered attendees.
- Basic knowledge of command line and git/github. Simple stuff like cloning repos, moving files, etc...

Course content is targeted for a Windows environment using Git Bash for Windows or other Bash terminal emulator. If you have a Mac and are a wiz with it, then come on. Just be aware that the instructor will not be able to answer Mac-specific questions, so you'll be on your own to translate commands from Windows to Mac and troubleshoot your own issues if things go off the rails.
-->

- Install the required software on your laptop **prior** to the class. See the [workstation setup guide](workstation-setup.md). 
- Login to https://api.caas.ford.com/console/catalog with your CDSID and password. You should be able to log in and see the `devenablement-workshop-dev` namespace. **DO NOT** deploy/create objects until the workshop.

## Schedule

The workshop is offered once per month. The duration is two 4-hour sessions offered typically on two consecutive days. It is currently offered for no charge.

To attend, sign up [here](https://it2.spt.ford.com/sites/dev/Lists/RegisterForEvent/newform.aspx).

## Begin Workshop

Begin with an [Overview of CaaS at Ford](https://it2.spt.ford.com/sites/dev/Documents/CaaS-At-Ford_Workshop.pptx) then [Lesson 1](./lessons/1-introduction.md).
