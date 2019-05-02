# Lesson 1, App Container Images

### Building Container Images with Localdev

The big picture...

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on building a container image for your app. The activities in this lesson correspond to boxes 1, 2, and 3 in the above diagram. If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

#### Exercise

The CaaS team maintains a repository of sample apps that will run on CaaS. You will clone this repo locally, and then go through the process of building a container image with one of the sample apps.

1. Open a terminal as Administrator on your workstation. Git Bash for Windows is recommended.
2. Clone the [samples repo](https://github.ford.com/JPOTTE46/samples) to your workstation.
```
# Change directory to your project workspace if you have a preferred one.
cd ~/workspace

# Clone the samples git repo.
git clone git@github.ford.com:JPOTTE46/samples.git
```
3. Configure synchronized folders between your workstation and the localdev VM so that you can access the samples repo from within the localdev VM. To set up a synchronized folder, customize then execute the commands below to configure an `ADDITIONAL_SYNCED_FOLDERS` environment variable. The value of this variable should be the full path to the samples repo that you cloned in the previous step, followed by the characters `=>`, followed by `/home/vagrant/containers`. For example, if you cloned the samples repository to `/c/Users/CDSID/workspace/samples`, then you would set up the env var with one of the commands below.
```
# On Git Bash for Windows
export ADDITIONAL_SYNCED_FOLDERS='/c/Users/CDSID/workspace/samples=>/home/vagrant/containers'

# On MacOS
export ADDITIONAL_SYNCED_FOLDERS='/Users/CDSID/workspace/samples=>/home/vagrant/containers'

# On Windows Powershell
$env:ADDITIONAL_SYNCED_FOLDERS = 'C:/Users/CDSID/workspace/samples=>/home/vagrant/containers'
```
The commands above will result in the samples repo (which is localed on your host workstation's filesystem) being mounted to `/home/vagrant/containers` in the VM's filesystem. To confirm that this stepped work, start the VM, log into the VM with ssh, and confirm that the folder was synchronized correctly.

```
# Change directory into your localdev directory.
cd ~/workspace/localdev

# Start the localdev VM. If it is already running, skip this step.
vagrant up

# SSH into the VM
vagrant ssh

# From your SSH session in the VM, list the contents of the samples repo.
[vagrant@m1 ~]$ ls /home/vagrant/containers   <------------- LIST THE CONTENTS OF THE SAMPLES REPO

best-practices.md  DTaaS  http-echo  jenkins  leap  perl  python  README.md  simple_nodejsapp  springboot  toolbox
```
You should see multiple files in `/home/vagrant/containers`. If you do not, let the instructor know you need help.

<!--
If the VM was already running before you set the ADDITIONAL_SYNCED_FOLDERS env var, then restart it so it will pick up the settings.

If you already started the localdev VM before creating the env var for synced folders, you may find `/home/vagrant/containers` is empty. In that case, exit out of ssh and reload the VM with `vagrant reload` so the synced folders will take effect. If that still does not work, then do a `vagrant destroy`, `vagrant update`, `vagrant prune`, and `vagrant up` which will rebuild the VM from scratch.
-->


   
4. Build the container image for a sample app (let's use the python app). If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

The python sample app has a build script at `image/build.sh` to make building a container image easier. Feel free to review the build script in a text editor or in the terminal with `cat /home/vagrant/containers/python/image/build.sh`. The build script sets up the environment variables necessary to use Ford's web proxy server as required. It then builds the container image using a tool call Buildah.

> Note that Red Hat, Ford's CaaS vendor, is promoting the use of the Buildah tool over Docker, so the build scripts in these samples use Buildah. If you're familiar with Docker, you will find Buildah behaves almost identically. This [blog](https://www.projectatomic.io/blog/2017/11/getting-started-with-buildah/) and this [Red Hat doc](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8-beta/html/building_running_and_managing_containers/building-container-images-with-buildah_building-running-and-managing-containers) have some basic Buildah examples.

The python sample app also has a Dockerfile at `image/Dockerfile` that defines the container image to be built when the build script is executed. Feel free to review the Dockerfile in a text editor or in the terminal with `cat /home/vagrant/containers/python/image/Dockerfile`. As an app team deploying an app to Ford's CaaS environment, you will be responsible for developing and maintaining your app's Dockerfile.

Now, if you're ready to build the container image, run the `image/build.sh` script for the sample app you plan to deploy. For example:

```
[vagrant@m1 ~]$ /home/vagrant/containers/python/image/build.sh
Setting proxy env vars.....
STEP 1: FROM registry.access.redhat.com/rhscl/python-27-rhel7
Getting image source signatures
Copying blob sha256:cf9df0949547455093eff8889609c44291b52007ebb5f539ca58baa297b66e55
 72.31 MiB / 72.31 MiB [===================================================] 28s
STEP 2: ARG LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64
--> eb3afd7ce6fd80aa4e987a369bb293dec344637f3d9e2a9b03c14061a69f8456
STEP 3: FROM eb3afd7ce6fd80aa4e987a369bb293dec344637f3d9e2a9b03c14061a69f8456
...
STEP 17: COMMIT registry.ford.com/devenablement/python:0.0.1
```

If the build was successful, the script used the `image/Dockerfile` as input to build the app's container image, and saved that image locally. To confirm that the image is there, list the images with Buildah like this:
 
```
[vagrant@m1 ~]$ sudo buildah images
IMAGE NAME                                         IMAGE TAG   IMAGE ID        CREATED AT             SIZE
registry.access.redhat.com/rhscl/python-27-rhel7   latest      2a9a9538beb2    Jan 24, 2019 12:30     666 MB
registry.ford.com/devenablement/python             0.0.1       3c98d9af86f6    Feb 21, 2019 20:13     671 MB
```

One image is a cached copy of the `python-27-rhel7` image that was the base image for your app container image. It was downloaded from Red Hat's image registry by the Buildah tool. The other image `registry.ford.com/devenablement/python` is your app container image that was output by the Buildah tool.

Also, note that both the Buildah and Podman tools share this same image location. To demonstrate this, if you use Podman to list container images, you should see the same list.

```
[vagrant@m1 ~]$ sudo podman images
REPOSITORY                                         TAG      IMAGE ID       CREATED          SIZE
registry.ford.com/devenablement/python             0.0.1    3c98d9af86f6   11 minutes ago   671 MB
registry.access.redhat.com/rhscl/python-27-rhel7   latest   2a9a9538beb2   4 weeks ago      666 MB
```

5. Before running this image in CaaS, you can test it by running it locally with a tool like Podman or Docker. This example uses Podman.

The commands below use Podman to run the app container image in detached mode and publish the container's port 8080 to the host's port 8080. The command saves the container_id as a variable so you can destroy the container later. Then curl is used to test the python web app. If successful, the app responds with a 200 OK http code. Note that the app is not yet exposed beyond the VM, so you cannot access it in a web browser from your workstation yet.

```
[vagrant@m1 ~]$ container_id=$(sudo podman run -p 8080:8080 -d registry.ford.com/devenablement/python:0.0.1)

[vagrant@m1 ~]$ curl --head 127.0.0.1:8080
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 118
Server: Werkzeug/0.14.1 Python/2.7.13
Date: Thu, 21 Feb 2019 20:43:27 GMT

# Stop and destroy the container.
[vagrant@m1 ~]$ sudo podman container stop ${container_id}
```

---  

Continue to [Lesson 1.3](./lesson1.3.md).
