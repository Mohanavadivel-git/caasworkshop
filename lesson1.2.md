# Lesson 1, App Container Images

### Building Container Images with Localdev

The big picture...

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on building a container image for your app. The activities in this lesson correspond to boxes 1, 2, and 3 in the above diagram. If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

#### Exercise

The CaaS team maintains a repository of sample apps that will run on CaaS. You will clone this repo locally, and then go through the process of building a container image with one of the sample apps.

1. Open a terminal **as Administrator** on your workstation. Git Bash for Windows is recommended.
2. Clone the [samples repo](https://github.ford.com/JPOTTE46/samples) to your workstation.
```bash
# Change directory to your project workspace if you have a preferred one.
cd ~/workspace

# Clone the samples git repo.
git clone git@github.ford.com:JPOTTE46/samples.git

# Or clone the repo using https if your workstation is not configured to use ssh.
git clone https://github.ford.com/JPOTTE46/samples.git
```

3. After clonging the repo you will notice it contains a number of sample applications. For the workshop, we will use the Springboot application. To do so, we need to build the application using gradle. 

```bash
$ cd <LOCATION_OF_CLONED_REPO>
$ ls
best-practices.md  DTaaS  http-echo  leap  mailx  perl  python  README.md  simple_nodejsapp  springboot  toolbox
$ cd springboot
$ ./gradlew clean build
```

Continue to the next steps only when the build is successful. 

4. Configure synchronized folders between your workstation and the localdev VM so that you can access the samples repo from within the localdev VM. To set up a synchronized folder, customize then execute the commands below to configure an `ADDITIONAL_SYNCED_FOLDERS` environment variable. The value of this variable should be the full path to the samples repo that you cloned in the previous step, followed by the characters `=>`, followed by `/home/vagrant/containers`. So, on the left side the of `=>` is the location where you saved the samples repo. Let's export this as an environment variable. 

```bash
# Git Bash for Windows
export ADDITIONAL_SYNCED_FOLDERS='/c/YOUR_PATH_TO_REPO/samples=>/home/vagrant/containers'
# Terminal for MacOS
export ADDITIONAL_SYNCED_FOLDERS='/YOUR_PATH_TO_REPO/samples=>/home/vagrant/containers'
# Windows Powershell
$env:ADDITIONAL_SYNCED_FOLDERS = 'C:/YOUR_PATH_TO_REPO/samples=>/home/vagrant/containers'
```
The commands above will result in the samples repo (which is located on your host workstation's filesystem) being mounted to `/home/vagrant/containers` in the VM's filesystem. To confirm that this stepped work, start the VM, log into the VM with ssh, and confirm that the folder was synchronized correctly.

5. Issue the vagrant up command after navigating to the localdev directory. 
```bash
# Change directory into your localdev directory.
cd ~/workspace/localdev

# Start the localdev VM. If it is already running, skip this step.
vagrant up
```

> Note: You should receive a message to verify your host IP. If you do not, you will likely run into issues throughout the workshop  

6. After the VM is built, SSH into the VM and confirm the samples repo was mounted. 
```bash
# SSH into the VM
vagrant ssh

# From your SSH session in the VM, list the contents of the samples repo.
[vagrant@m1 ~]$ ls /home/vagrant/containers   #<------------- LIST THE CONTENTS OF THE SAMPLES REPO

best-practices.md  DTaaS  http-echo  jenkins  leap  perl  python  README.md  simple_nodejsapp  springboot  toolbox
```
You should see multiple files in `/home/vagrant/containers`. If you do not, let the instructor know you need help. If you are completing this outside of the workshop, check your file locations, ensure you're passing in the correct file location, and check the spelling.  

**>>>>>>> THIS IS A GREAT TIME FOR A BREAK <<<<<<<**

<!--
If the VM was already running before you set the ADDITIONAL_SYNCED_FOLDERS env var, then restart it so it will pick up the settings.

If you already started the localdev VM before creating the env var for synced folders, you may find `/home/vagrant/containers` is empty. In that case, exit out of ssh and reload the VM with `vagrant reload` so the synced folders will take effect. If that still does not work, then do a `vagrant destroy`, `vagrant update`, `vagrant prune`, and `vagrant up` which will rebuild the VM from scratch.
-->

7. Build the container image for the Springboot app. If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

The springboot sample app has a build script at [`image/build.sh`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/image/build.sh) to make building a container image easier. Feel free to review the build script by clicking the above link, in a text editor, or in the terminal with `cat /home/vagrant/containers/springboot/image/build.sh`. The build script sets up the environment variables necessary to use Ford's web proxy server as required. It then builds the container image using a tool call Buildah.

> Note that Red Hat, Ford's CaaS vendor, is promoting the use of the Buildah tool over Docker, so the build scripts in these samples use Buildah. If you're familiar with Docker, you will find Buildah behaves almost identically. This [blog](https://www.projectatomic.io/blog/2017/11/getting-started-with-buildah/) and this [Red Hat doc](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8-beta/html/building_running_and_managing_containers/building-container-images-with-buildah_building-running-and-managing-containers) have some basic Buildah examples.

The springboot sample app also has a Dockerfile at [`image/Dockerfile`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/image/Dockerfile) that defines the container image to be built when the build script is executed. Feel free to review the Dockerfile clicking the link above, in a text editor, or in the terminal with `cat /home/vagrant/containers/springboot/image/Dockerfile`. As an app team deploying an app to Ford's CaaS environment, you will be responsible for developing and maintaining your app's Dockerfile.

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
--> 9da79f7a3ab568b4f3bca66a280d76e4ca09815e06ec170caafb744e382216b3
STEP 3: FROM 9da79f7a3ab568b4f3bca66a280d76e4ca09815e06ec170caafb744e382216b3
...
STEP 11: COMMIT registry.ford.com/devenablement/springboot-hello-world:0.0.1
```

8. If the build was successful, the script used the `image/Dockerfile` as input to build the app's container image, and saved that image locally. To confirm that the image is there, list the images with Buildah like this:
```bash
[vagrant@m1 ~]$ sudo buildah images
IMAGE NAME                                                        IMAGE TAG  IMAGE ID      CREATED AT          SIZE
registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift  latest     b4b953ca8f5  Apr 18, 2019 15:11  498 MB
registry.ford.com/devenablement/springboot-hello-world            0.0.1      54bf7824222  May 29, 2019 12:15  528 MB

```

One image is a cached copy of the `openjdk18-openshift` image that was the base image for your app container image. It was downloaded from Red Hat's image registry by the Buildah tool. The other image `registry.ford.com/devenablement/springboot-hello-world` is your app container image that was output by the Buildah tool.

9. Also, note that both the Buildah and Podman tools share this same image location. To demonstrate this, if you use Podman to list container images, you should see the same list.
```bash
[vagrant@m1 ~]$ sudo podman images
REPOSITORY                                                         TAG      IMAGE ID       CREATED         SIZE
registry.ford.com/devenablement/springboot-hello-world             0.0.1    54bf78242223   2 minutes ago   528 MB
registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift   latest   b4b953ca8f5b   5 weeks ago     498 MB
```

10. Before running this image in CaaS, you can test it by running it locally with a tool like Podman or Docker. This example uses Podman.

The commands below use Podman to run the app container image in detached mode and publish the container's port 8080 to the host's port 8080. The command saves the container_id as a variable so you can destroy the container later. Then curl is used to test the python web app. If successful, the app responds with a 200 OK http code. Note that the app is not yet exposed beyond the VM, so you cannot access it in a web browser from your workstation yet.

```bash
[vagrant@m1 ~]$ container_id=$(sudo podman run -p 8080:8080 -d registry.ford.com/devenablement/springboot-hello-world:0.0.1)

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

Continue to [Lesson 1.3](./lesson1.3.md).
