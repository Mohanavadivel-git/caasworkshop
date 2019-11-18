## Container Image Registries

### The Big Picture - Step 3

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on understanding container image registries. At Ford, we use a tool called Quay to provide an on-premise registry to store images. If you are familiar with Docker Hub on the public internet, Quay is similar. The production instance of Quay is at https://registry.ford.com/.

---

### Quay 

Quay is Ford's container image registry. All the images you build will be stored in Quay. The format in Quay follows an Organization->Repository style. For your organization, you may have one or more repositories.

Any single repository corresponds to a single application's container image. You may keep your version history within Quay as well to allow for rollbacks. 

To be able to push container images to Quay you will need to provide authentication. Quay has a version of generic accounts called "robots" that can be maintained by the owner of a repository. 

### Exercise - Understanding Robots

1. Navigate to https://registry.ford.com/ 
2. On the right side of the page, in the `Users and Organizations` section, click your CDSID. 
3. On the left side of the page, click the Robot icon. 
4. Click `Create Robot Account`
5. Choose any name (example: `test`) and descriptor for this Robot. 
6. On the next page, click `Close` without choosing a repository. 
7. After the creation of the robot, click the robot and then click `Kubernetes Secret`. 
8. Click the button that says `View <my-robot-name>.yml`.

What you are viewing here is the Kubernetes secet for your Robot. Providing this secret to Openshift will allow Openshift to access any repository that this robot has access to. Robot permissions can be set for single or multiple repositores and set as read or write. 

### Workshop Secret

You are currently set with developer mode in the namespace. Therefore, you are unable to create or manage secrets. This is to enforce some separation of duties for developers. 

Similarly to the robot account you created for yourself, a robot account was created for the workshop repository. This robot has read and write access to the workshop repository. This will allow you to create and push container images to this repository and deploy them later on. 

---

### Requesting Quay Access

App teams that need access to Quay can request it using these [instructions](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#quay-on-boarding.)

---  

Continue to [Openshift console and CLI](./6-buildimage.md).

Return to [Table of Contents](../README.md#agenda)
