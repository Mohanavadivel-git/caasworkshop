## Introduction

### Pre-Requisites

Did you set up your workstation with CaaS localdev yet? If not, complete the [instructions](../workstation-setup.md).

### What is Ford's CaaS?

CaaS is Ford's container as a service offering. It is an app hosting platform.

At Ford, we currently use RedHat's OpenShift Container Platform to provide CaaS although there are many other products in the market that could also provide a similar capability. For this reason, we will use the generic term CaaS to refer to the service offering.

To use CaaS, as an app team, you have responsibility for building your app and building an associated app container image. Then you take that app container image and upload it to the CaaS platform. From there CaaS will run your app container, and in doing so, run your app.

Both CaaS and the Pivotal Cloud Foundry (PCF) PaaS platform provide an app hosting service in a "cloudy" containerized way, so in some respects they are similar. But in many ways they are different.

Pivotal often describes PCF as an "[opinionated platform](https://content.pivotal.io/blog/cloud-foundry-brazen-opinions-and-easy-extensions)". In other words, in the pursuit of speed and simplicity, app teams get to ignore many of the technical details involved with running on a containerized, cloud platform. Pivotal has made many technical decisions on app teams' behalf and configured these decisions into the platform. You couldn't change them if you wanted to.

In contrast, the CaaS platform is highly configurable. For example, app teams have total control over their apps' resource allocation, data center location, TLS termination, and packages, libraries and other dependencies included in their container image. The trade-off is there is a pretty steep learning curve for CaaS. Be sure you have the desire to get into the weeds with cloud hosting with CaaS.

---  

Continue to [Application Code and Mounting Directories](./2-buildapp.md).

Return to [Table of Contents](../README.md#agenda)