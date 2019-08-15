## Openshift Console and CLI

Next, you will be deploying the container image you built in the last lesson to CaaS localdev. Deploying to localdev is similar to how you might deploy the container image to the production instance of CaaS. To do that, we will need to access the Openshift console and/or use the `oc` CLI. 

#### Exercise

1. Your instance of localdev has started and is running a full installation of OpenShift. Test to confirm that OpenShift is running and ready by opening the web management in a browser at https://console.oc.local:8443/. Your browser will give you an error about the self-signed SSL certificate, but just tell it to proceed anyway. You will have to do that twice because of a redirect.

Once you get a log in prompt, use the following credentials:

```yaml
Username: admin
Password: sandbox
```

2. In addition to the web interface, you can communicate directly with the OpenShift API using a command line tool called `oc` from Red Hat, or the more generic Kubernetes command-line tool `kubectl`. This workshop uses `oc` and it is recommended that you use `oc` for all interactions with Openshift.

```bash
# Login to Openshift
[vagrant@m1 ~]$ oc login api.oc.local:8443
Username: admin
Password: sandbox

# Create a new project to hold the app and keep things organized.
[vagrant@m1 ~]$ oc new-project my-namespace
```

> NOTE: You can only create a project this way in localdev. Visit the [Ford Cloud Portal](https://www.cloudportal.ford.com/openshift) if you wish to get a project/namespace in the production instance of Openshift

In Openshift, `project` and `namespace` are used interchangeably. It is a logicial construct where you deploy your Openshift objects. Your application instances/replicas may span different nodes and data centers, but you can manage them all within your single namespace. 

<!---
If you get an error like, "no such host" or "couldn't resolve host", the issue is likely with the name resolution of `console.oc.local`. The localdev installation runs a local DNS service to provide name resolution for the `oc.local` domain. Sometimes, you will need to wait a bit longer for the DNS service to start, or manually flush your DNS cache with `ipconfig /flushdns` on Windows (or escape the fwd slash in Git Bash like `ipconfig //flushdns`).
-->
---  

Continue to [Openshift objects](./7-objects.md).

Return to [Table of Contents](../README.md#agenda)