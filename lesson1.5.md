## Day 1 - Lesson 1

## Container Image Registries

The big picture...

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on understanding container image registries. At Ford, we use a tool called Quay to provide an on-premise registry to store images. If you are familiar with Docker Hub on the public internet, Quay is similar.

Quay is secured and since you likely do not have an account, there is no hands-on exercise.

Jump over to the samples repository README again and review the section on [pushing an image to a container registry](https://github.ford.com/JPOTTE46/samples#optional-pushing-an-image-to-container-registry).

#### Requesting Quay Access

App teams that need access to Quay can request it using these [instructions](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#quay-on-boarding.)

The production instance of Quay is at https://registry.ford.com/.

<!--
#### Shutting Down LocalDev

At the end of the day, you should stop your localdev instance with the following commands from the terminal.

```bash
# Exit out of the VM
[vagrant@m1 ~]$ exit
logout
Connection to 127.0.0.1 closed.

# Stop the VM. This takes about a minute.
vagrant halt
```
-->
---  

Continue to [Lesson 2](./lesson2.1.md).

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop/tree/workshop-reformat#agenda)