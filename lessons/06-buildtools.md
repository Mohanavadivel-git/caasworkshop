## Container Build Tools

There are numerous ways of building a container image. We will provide an overview of some of the ways you can do that on your machine.

## Docker

For those with administrative rights on their machine, you can download Docker from the public internet. This will give you the ability to build, run, and store Docker images on your machine. You will get the Docker CLI, which comes with commands such as `docker build` and `docker push` to build your container image and save your image to Quay.

## LocalDev

A [previous version](https://github.ford.com/DevEnablement/caas-workshop/tree/archived) of the workshop went over installing [localdev](https://github.ford.com/Containers/localdev) on your machine. Localdev is maintained by the CaaS engineering team and allows you to run a local, slim version of CaaS on a local virtual machine. This allows you to do development and testing locally without ever deploying your images to the production instance of CaaS.

There are numerous advantages of using and developing with localdev, namely that you can test and run your container images before pushing them to the production cluster. Anytime you come across issues or "break" your application, you can destroy everything and rebuild it quickly. Localdev is maintained to be the same, or one version ahead of, the production instance of CaaS. In the words of the CaaS engineering team: "if it works in localdev, it will work on the production cluster."

Localdev comes packaged with Docker, Buildah, and Podman. Buildah and Podman are the more preferable container image build tools maintained by RedHat that has [advantages over Docker](https://developers.redhat.com/blog/2019/02/21/podman-and-buildah-for-docker-users/). Localdev provides these tools so that you do not need to install them separately.

The disadvantage of localdev is that it requires a lot of setup and a powerful machine. To properly set up localdev, you will need a 4 core CPU machine and 8 GB of RAM (i.e. a developer machine). Localdev also runs on VirtualBox, which is prone to errors and is notoriously buggy.

**Note**: Localdev uses VirtualBox, which conflicts with `Hyper-V` used by Docker. You can only have 1 running on your system at a time without workarounds.

## BuildConfigs

The Openshift product provides a way to build container images within the cluster itself with an object called `BuildConfigs`. This way, we avoid installing any other command line tools or virtual machines. This makes it a quicker and cleaner process that is less prone to machine errors.

The disadvantage is that you now can no longer test and view your container images locally. Generally, the building of your container image will be done in your team's DEV environment to compensate for this disadvantage.

This workshop uses `BuildConfigs` to build our container images. If you have a developer machine, you are still encouraged to download [localdev](https://github.ford.com/Containers/localdev) and can build container images that way if you want the ability to test and run images locally. A [troubleshooting guide](https://github.ford.com/DevEnablement/caas-workshop/blob/archived/troubleshooting.md) is provided in the old version of the workshop.

---

Continue to [build configs introduction](./07-buildintro.md).

Return to [Table of Contents](../README.md#agenda)
