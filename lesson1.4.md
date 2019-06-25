# Lesson 1, App Container Images

### Building Container Images with Localdev

1. Build the container image for the Springboot app. 

If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

The springboot sample app has a build script at [`image/build.sh`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/image/build.sh) to make building a container image easier. The build script sets up the environment variables necessary to use Ford's web proxy server as required. It then builds the container image using a tool call Buildah.

> Note that Red Hat, Ford's CaaS vendor, is promoting the use of the Buildah tool over Docker, so the build scripts in these samples use Buildah. If you're familiar with Docker, you will find Buildah behaves almost identically. This [blog](https://www.projectatomic.io/blog/2017/11/getting-started-with-buildah/) and this [Red Hat doc](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8-beta/html/building_running_and_managing_containers/building-container-images-with-buildah_building-running-and-managing-containers) have some basic Buildah examples.

The springboot sample app also has a Dockerfile at [`image/Dockerfile`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/image/Dockerfile) that defines the container image to be built when the build script is executed. As an app team deploying an app to Ford's CaaS environment, you will be responsible for developing and maintaining your app's Dockerfile.


Now, if you're ready to build the container image, run the `image/build.sh` script for the sample app you plan to deploy. For example:
```bash
[vagrant@m1 ~]$ /home/vagrant/containers/springboot/image/build.sh
Setting proxy env vars.....
STEP 1: FROM registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift
Getting image source signatures
Copying blob sha256:76608b6b9d54251299c5d3be69fdf53e05f97a3735bbcd5889c30ebb78608428
 72.31 MiB / ? [---------------------------------------------=------------] 29s
Copying blob sha256:3c81a5d20855a6cef8b997d709410e047e2839b5ad113f4c34d25e9fae9e3beb
 1.24 KiB / ? [--------------=---------------------------------------------] 0s
Copying blob sha256:f4e561752acba40ba739e700e3b3277b8fe23eee951a5d2dfde7e7e762a3d156
 101.99 MiB / ? [----=----------------------------------------------------] 21s
Copying config sha256:b4b953ca8f5b9319b769842c7409a46b3e04136fe2d2165b88766b5a895e8b75
 7.53 KiB / 7.53 KiB [======================================================] 0s
Writing manifest to image destination
Storing signatures
STEP 2: VOLUME /tmp
-> 9da79f7a3ab568b4f3bca66a280d76e4ca09815e06ec170caafb744e382216b3
STEP 3: FROM 9da79f7a3ab568b4f3bca66a280d76e4ca09815e06ec170caafb744e382216b3
...
STEP 11: COMMIT registry.ford.com/devenablement/springboot-hello-world:0.0.1
```

2. If the build was successful, the script used the `image/Dockerfile` as input to build the app's container image, and saved that image locally. To confirm that the image is there, list the images with Buildah like this:
```bash
[vagrant@m1 ~]$ sudo buildah images
IMAGE NAME                                                        IMAGE TAG  IMAGE ID      CREATED AT          SIZE
registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift  latest     b4b953ca8f5  Apr 18, 2019 15:11  498 MB
registry.ford.com/devenablement/springboot-hello-world            0.0.1      54bf7824222  May 29, 2019 12:15  528 MB

```

One image is a cached copy of the `openjdk18-openshift` image that was the base image for your app container image. It was downloaded from Red Hat's image registry by the Buildah tool. The other image `registry.ford.com/devenablement/springboot-hello-world` is your app container image that was output by the Buildah tool.

3. Also, note that both the Buildah and Podman tools share this same image location. To demonstrate this, if you use Podman to list container images, you should see the same list.
```bash
[vagrant@m1 ~]$ sudo podman images
REPOSITORY                                                         TAG      IMAGE ID       CREATED         SIZE
registry.ford.com/devenablement/springboot-hello-world             0.0.1    54bf78242223   2 minutes ago   528 MB
registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift   latest   b4b953ca8f5b   5 weeks ago     498 MB
```

4. Before running this image in CaaS, you can test it by running it locally with a tool like Podman or Docker. This example uses Podman.

The commands below use Podman to run the app container image in detached mode and publish the container's port 8080 to the host's port 8080. The command saves the container_id as a variable so you can destroy the container later. Then curl is used to test the python web app. If successful, the app responds with a 200 OK http code. Note that the app is not yet exposed beyond the VM, so you cannot access it in a web browser from your workstation yet.

```bash
[vagrant@m1 ~]$ container_id=$(sudo podman run -p 8080:8080 -d springboot-hello-world:0.0.1)

[vagrant@m1 ~]$ curl --head 127.0.0.1:8080/api/v1/hello
HTTP/1.1 200
X-Request-Info: timestamp=1559133133; execution=1;
X-Application-Info: name=${spring.application.name}; version=unspecified;
...
Content-Length: 44
Date: Wed, 29 May 2019 12:32:13 GMT

# Stop and destroy the container.
[vagrant@m1 ~]$ sudo podman container stop ${container_id}
```

---  

Continue to [Lesson 1.5](./lesson1.5.md).