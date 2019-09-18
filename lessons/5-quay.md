## Container Image Registries

### The Big Picture - Step 3

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on understanding container image registries. At Ford, we use a tool called Quay to provide an on-premise registry to store images. If you are familiar with Docker Hub on the public internet, Quay is similar. The production instance of Quay is at https://registry.ford.com/.

---

### Exercise 

### Push Container Image to Quay

If you are following this guide as part of the workshop, we will push the image we created to the DevEnablement organization in Quay. If you are following this workshop on your own, go to the [next section](./5-quay.md#exercise---post-workshop).

Recall in the `build.sh` script, we defined the IMAGE_NAME to be `springboot-hello-world` and the VERSION to be `0.0.1`. Normally, you would change these values in `build.sh` to match the repository you will push to in Quay. For the purposes of the workshop, however, we will push the image to the `workshop` repository in the `devenablement` organization, and you will use a version number assigned to you.

[Click here](https://gist.github.ford.com/JPOTTE46/388b8eb535811c9e98ccae7aeb0e3d22) to copy the command to login with the Quay credentials provided to you for the workshop. 

```bash
# Pushing the container to Quay
# The command below is just an example - copy the actual command from the link above
[vagrant@m1 ~]$ sudo podman login -u="USERNAME" -p="PASSWORD" registry.ford.com

# Push your image to Quay using your version number
[vagrant@m1 ~]$ sudo podman push \
                    springboot-hello-world:0.0.1 \
                    registry.ford.com/devenablement/workshop:YOUR_VERSION_NUMBER
```

#### Update Manifest

In the `samples/springboot/manifest/deployment-1.yaml` file, there is a reference to the image at line 59. 

```yaml
containers:
      - name: springboot-hello-world
        # image will be pulled from localdev Docker Registry if present
        image: registry.ford.com/devenablement/workshop:0.0.1 # <---------- Update version here
        imagePullPolicy: IfNotPresent
```

Openshift will attempt to access the image located at the location provided, which in this case, is `registry.ford.com/devenablement/workshop:0.0.1`. If this image is not available locally, it will attempt to access the image via the URL provided. 

For Openshift to get the correct image, you must update the `deployment-1.yaml` file to reference the correct image tag. 

### Exercise - Post-Workshop

When you go to develop at the end of the workshops, you will not have access to the DevEnablement Quay organization and the workshop repository. If you or your team do not have an organization in Quay, you can still push your container images to a registry. Instead of the registry on Quay, you will push your container to your local container image registry, which localdev provides. 

```bash
# Pushing the container to local registry
sudo podman push \
    springboot-hello-world:0.0.1 \
    docker-daemon:registry.ford.com/devenablement/workshop:0.0.1

Getting image source signatures
Copying blob sha256:050c734bd2868bcd3b69ab0ca033aa3bc95a00a4a1e5317e732394e1c36ef59e
 203.90 MB / 203.90 MB [====================================================] 2s
 ...
Writing manifest to image destination
Storing signatures
```

Looking at the command, you can see we are pushing the image to the local docker daemon. You can see we have kept the name `registry.ford.com/devenablement/workshop:0.0.1`, so no changes are needed to the `deployment-1.yaml` file other than needing the version number here to match the version number in your `deployment-1.yaml` file. 

If you wish, you can change this name. For example, in place of `registry.ford.com/devenablement/workshop:0.0.1`, you could put `springboot-hello-world:0.0.1` or `my-app:1.0.0`. You would then need to change the `deployment-1.yaml` file (on line 59) to read `springboot-hello-world:0.0.1` or `my-app:1.0.0` instead of `registry.ford.com/devenablement/workshop:0.0.1`. 

---

### Requesting Quay Access

App teams that need access to Quay can request it using these [instructions](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#quay-on-boarding.)

---  

Continue to [Openshift console and CLI](./6-console.md).

Return to [Table of Contents](../README.md#agenda)
