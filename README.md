# Deploying Apps to Ford's CaaS Platform

:imagesdir: images

image:OpenShift_Logo.svg[alt="OpenShift Logo", align="left",width=420]

This is a hands-on, training workshop to get application development teams started in Ford's Container as a Service platform.

This workshop will provide instructions to build application container images, then deploying these images to the CaaS platfom. Workshop participants will experience deploying a sample application to a local CaaS environment on their own workstation. In doing so, participants will learn how they can take the applications they build and deploy to Ford's CaaS platform.

# Agenda

#### Day 1
- Localdev
  - Installing dependencies: vagrant, virtual box, git
  - Installing localdev repo and starting the vm
  - Testing the installation in a browser and with cli
- Building an App Container Image
  - Docker 101, Dockerfile
  - Using other tools, buildah, podman, docker
- Image Registries
  - Ford's Quay Registry

#### Day 2
- Running App Container in Openshift
  - Manifest Objects
- Managing App Container Resources
  - Avoid defaults
  - CPU Cores and resource limits

#### Day 3
- Monitoring Apps
  - https://grafana-openshift-monitoring.app.caas.ford.com/?orgId=1
- Storage
  - Persistent storage options
- Vanity URLs and TLS
  - Requesting a Vanity URL
  - TLS termination options
- Jenkins Usage
