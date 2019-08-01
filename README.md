# Deploying Apps to Ford's CaaS Platform

This is a hands-on, training workshop to get application development teams started in Ford's Container as a Service platform.

![OpenShift Logo](images/OpenShift_Logo.svg)

This workshop will provide instructions to build application container images, then deploying these images to the CaaS platform. Workshop participants will experience deploying a sample application to a local CaaS environment on their own workstation. In doing so, participants will learn how they can take the applications they build and deploy to Ford's CaaS platform.

# Agenda

#### Day 1

- **Lesson 1** - App Container Images
    - [Introduction](./lesson1.1.md)
    - [The Big Picture and Mounting Directories](./lesson1.2.md)
    - [Writing Dockerfiles](./lesson1.3.md)
    - [Building a Container image](./lesson1.4.md)
    - [Ford's Docker Registry](./lesson1.5.md)
- **Lesson 2** - Running Apps in Openshift
    - [Acessing the Console and oc CLI](./lesson2.1.md)
    - [Manifests and Openshift Objects](./lesson2.2.md)
    - [Pushing Container Image to Registry](./lesson2.3.md)
    - [Deploying Application to Openshift](./lesson2.4.md)
    - [Best Practices](./lesson2.5.md)

#### Day 2

- **Lesson 3** - Application Monitoring
    - [Grafana and Dynatrace](./lesson3.1.md)
- **Lesson 4** - Volumes
    - [Volume and Storage Overview](./lesson4.1.md)
    - [Deploying Application w. Persistent Volume Claim](./lesson4.2.md)
- **Lesson 5** - Application Logging
    - [Elasticsearch and Kibana](./lesson5.1.md)
    - [Writing application logs to storage](./lesson5.2.md)
- **Lesson 6** - [Vanity URLs and Routes](./lesson6.1.md)

<!--
#### Lesson 1, App Container Images
- Setting up the CaaS localdev environment on your workstation.
- Building your first app container image.
- Understanding Ford's container image registry.

#### Lesson 2, Running Apps in CaaS
- Running the app container images that were built in the last lesson in Openshift.
- Managing app container resources.
- Best practices for CaaS apps.

#### Lesson 3, Advanced Topics
- Monitoring app performance.
- Persistent Volume Claims
- Logging with Kibana
- More to come in the future.

- Viewing app logs.
- Utilizing persistent storage options.
- Configuring vanity URLs and TLS security.
- Using Jenkins and other CI/CD tools.
-->

# Pre-requisites and Equipment
- Your own developer-class laptop with minimal 4 CPU cores and 8GB of RAM. An underpowered laptop that is used mostly for checking email WILL NOT WORK.
- Install the required software on your laptop prior to class. [Instructions](workstation-setup.md) will be sent out to registered attendees.
- Basic knowledge of command line and git/github. Simple stuff like cloning repos, moving files, etc...

Course content is targeted for a Windows environment using Git Bash for Windows or other Bash terminal emulator. If you have a Mac and are a wiz with it, then come on. Just be aware that the instructor will not be able to answer Mac-specific questions, so you'll be on your own to translate commands from Windows to Mac and troubleshoot your own issues if things go off the rails.

# Schedule

The workshop is offered once per month. The duration is two 4-hour sessions offered typically on two consecutive days. It is currently offered for no charge.

To attend, sign up [here](https://it2.spt.ford.com/sites/dev/Lists/RegisterForEvent/newform.aspx).

# Begin Workshop

Begin with an [Overview of CaaS at Ford](https://it2.spt.ford.com/sites/dev/Documents/CaaS-At-Ford_Workshop.pptx) then [Lesson 1](./lesson1.1.md).
