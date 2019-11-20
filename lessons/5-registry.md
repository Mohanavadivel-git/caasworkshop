## Container Image Registries

### The Big Picture - Step 3

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on understanding container image registries. At Ford, we use a tool called Quay to provide an on-premise registry to store images. If you are familiar with Docker Hub on the public internet, Quay is similar. The production instance of Quay is at https://registry.ford.com/.

---

## Quay 

Quay is Ford's container image registry. All the images you build should be stored in Quay. The format in Quay follows an Organization->Repository style. For your organization, you may have one or more repositories. 

Any single repository corresponds to a single application's container image. You may keep your version history within Quay as well to allow for rollbacks. 

To be able to push container images to Quay you will need to provide authentication. Quay has a version of generic accounts called "robots" that can be maintained by the owner of a repository. 

### Exercise - Understanding Robots

1. Navigate to https://registry.ford.com/ 
2. On the right side of the page, in the `Users and Organizations` section, click your CDSID. 
3. On the left side of the page, click the Robot icon. 
4. Click `Create Robot Account`
5. Choose any name (example: `test`) and descriptor for this Robot. 
6. On the next page, click `Close` without choosing a repository. 
7. After the creation of the robot, click the robot name and then click `Kubernetes Secret`. 
8. Click the button that says `View <my-robot-name>.yml`.

Sample Kubernetes secret: 

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: workshop-test-pull-secret
data:
  .dockerconfigjson: ewogICJhdXRocyI6IHsKICAgICJyZWdpc3RyeS5mb3JkLmNvbSI6IHsKICAgICAgImF1dj5iOiAiYldGc2VXRnpjeXQwWlhOME9sbERVMFJhT0VveVEwRmFRa3hTUlVSUVExaFdURTh5TmtORFNrRk1NVFpPVjFCWVNVVlJNRlZRUjFGTk5sP3FOMDFOVFZoRU0xRlNNbHBLVlRaVFMwVT0iLAogICAgICAiZW1haWw0fE4iIgogICAgfQogIH0KfQ==
type: kubernetes.io/dockerconfigjson
```

What you are viewing here is the Kubernetes secet for your Robot. You can see the "kind" of object is a `secret`. It provides a type called `kubernetes.io/dockerconfigjson`, which is the type for a Kubernetes credential, aka, a credential for a container image repository.

Providing this secret to Openshift will allow Openshift to access any repository that this robot has access to. Robot permissions can be set for single or multiple repositores and set as read or write. 

### Exercise - Deploy Secret

Let's practice deploying this secret to our namespace. We will use bash/command line to create it. 

1. Download this `yaml` file and save it to the samples repository in `samples/springboot/manifest` with the other yaml files. 
2. Save the file as `pull-secret-test.yaml` 
3. Run the command below to create the secret. 

```bash
# Navigate to the springboot directory if you have not already 
$ cd springboot
$ oc create -f ./manifest/pull-secret-test.yaml
```

You should receive the following error: 

```bash
Error from server (Forbidden): error when creating "pulpull-secret-test.yaml": secrets is forbidden: User <YOUR-CDSID> cannot create secrets in the namespace "devenablement-workshop-dev": no RBAC policy matched
```

The reason why you receive this error is because you are set with developer permissions in the namespace. To have some forms of separtion of duties, developers cannot create or view secrets.

These exercises showed you how to create and deploy Quay credentials to a namespace so that if are an admin on a namespace, you will know how to.

### Workshop Secret

Similarly to the robot account you created for yourself, a robot account was created for the workshop repository. This robot has read and write access to the workshop repository. This will allow you to create and push container images to this repository and deploy them later on. 

## RedHat 

You may also find that you need to authenticate against RedHat's container catalog to use their images. In this class, you will notice the `FROM` statement of the `Dockerfile` is from RedHat's registry, not Quay. To be able to authenticate against RedHat's registry in your namespace, see [these instructions](). 

For the purpose of the workshop, this credential has already been created and we will be able to use it to utilize RedHat's container catalog, which you can view [here](https://registry.redhat.io). 

---

### Requesting Quay Access

App teams that need access to Quay can request it using these [instructions](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#quay-on-boarding.)

---  

Continue to [Openshift console and CLI](./6-buildimage.md).

Return to [Table of Contents](../README.md#agenda)
