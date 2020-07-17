# Container Build Tools

There are numerous ways of building a container image. We will provide an overview of some of the ways you can do that on your machine.

## Docker

For those with administrative rights on their machine, you can download Docker from the public internet. This will give you the ability to build, run, and store Docker images on your machine. You will get the Docker CLI, which comes with commands such as `docker build` and `docker push` to build your container image and save your image to Quay.

## BuildConfigs

The OpenShift product provides a way to build container images within the cluster itself with an object called `BuildConfigs`. This way, we avoid installing any other command line tools or virtual machines. This makes it a quick and clean process that is less prone to machine errors.

The disadvantage is that you now can no longer test and view your container images locally. Generally, the building of your container image will be done in your team's DEV environment to compensate for this disadvantage.

This workshop uses `BuildConfigs` to build our container images and this is the recommended approach for all projects going forward.


## LocalDev

A [previous version](https://github.ford.com/DevEnablement/caas-workshop/tree/archived) of the workshop went over installing [localdev](https://github.ford.com/Containers/localdev) on your machine. Localdev was maintained by the CaaS engineering team and allowed you to run a local, slim version of CaaS on a local virtual machine. This allowed you to do development and testing locally without ever deploying your images to the production instance of CaaS. However, CaaS engineering is no longer supporting or updating localdev and it will not be upgraded to version 4.x of OpenShift, so there will be significant differences between localdev and production CaaS.

There were some advantages of using and developing with localdev, namely that you could test and run your container images before pushing them to the production cluster. Anytime you come across issues or "break" your application, you can destroy everything and rebuild it quickly. 

Localdev comes packaged with Docker, Buildah, and Podman. Buildah and Podman are the preferred container image build tools maintained by RedHat and have [advantages over Docker](https://developers.redhat.com/blog/2019/02/21/podman-and-buildah-for-docker-users/). Localdev provides these tools so that you do not need to install them separately.

The disadvantage of localdev is that it requires a lot of setup and a powerful machine. To properly set up localdev, you will need a 4 core CPU machine and 8 GB of RAM (i.e. a developer machine). Localdev also runs on VirtualBox, which is prone to errors and is notoriously buggy.  A [troubleshooting guide](https://github.ford.com/DevEnablement/caas-workshop/blob/archived/troubleshooting.md) is provided in the old version of the workshop. We have also found that it will not work while the VPN is on, making it impossible to push from localdev to CaaS while working from home.

At this point the DevEnablement and CaaS engineering teams recommend using BuildConfigs to build your Docker images for new projects and migrating to BuildConfigs if you are currently using the localdev workflow.

**Note**: Localdev uses VirtualBox, which conflicts with `Hyper-V` used by Docker. You can only have 1 running on your system at a time without workarounds.

---

Continue to [Building a Container Image Using BuildConfigs](./07-buildintro.md).

Return to [Table of Contents](../README.md#agenda)
