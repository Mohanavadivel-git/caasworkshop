## Building A Sample Application

### The Big Picture - Step 1

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson will go over building the sample Springboot application and mounting the samples app directory to our virtual machine. 

---

#### Exercise

1. Open a terminal as administrator and navigate to the samples directory you cloned in the [Workstation Setup](../workstation-setup.md#samples-repository). 

```bash
$ cd <LOCATION_OF_SAMPLES_REPO>
$ ls
best-practices.md  DTaaS  http-echo  leap  mailx  perl  python  README.md  simple_nodejsapp  springboot  toolbox
```

2. For the workshop, we will use the Springboot application. To do so, we need to build the application using `gradlew clean build`. 

> Note: For this sample app, you will need to point your `JAVA_HOME` environment variable to your JDK8 path. If you are currently using Java 10 or 11, see the [workstation setup](../workstation-setup.md#jdk-8) for instructions for getting JDK8. 

```bash
$ cd springboot
$ ./gradlew clean build
Starting a Gradle Daemon (subsequent builds will be faster)
...
BUILD SUCCESSFUL in 19s
7 actionable tasks: 7 executed
```

Continue to the next steps only when the build is successful. 

3. Configure synchronized folders between your workstation and the localdev VM so that you can access the samples repo from within the localdev VM. To set up a synchronized folder, customize and then execute the commands below to configure an `ADDITIONAL_SYNCED_FOLDERS` environment variable. 

The value of this variable should be the full path to the samples repo that you cloned in the previous step, followed by the characters `=>`, followed by `/home/vagrant/containers`. So, on the left side the of `=>` is the location where you saved the samples repo. Let's export this as an environment variable. 

```bash
# Git Bash for Windows
export ADDITIONAL_SYNCED_FOLDERS='/c/YOUR_PATH/samples=>/home/vagrant/containers'
# Terminal for MacOS
export ADDITIONAL_SYNCED_FOLDERS='/YOUR_PATH/samples=>/home/vagrant/containers'
# Windows Powershell
$env:ADDITIONAL_SYNCED_FOLDERS = 'C:/YOUR_PATH/samples=>/home/vagrant/containers'
```
The commands above will result in the samples repo (which is located on your host workstation's filesystem) being mounted to `/home/vagrant/containers` in the VM's filesystem. The next steps will confirm whether or not the mounting was done correctly. 

4. Issue the vagrant up command after navigating to the localdev directory. If you already brought vagrant up, execute a vagrant reload. 

```bash
# Change directory into your localdev directory.
cd <PATH_TO_LOCALDEV_DIRECTORY>

# Start the localdev VM if you have not already
vagrant up

# Re-load the VM if you already have the VM running 
vagrant reload
```

> Note: You should receive a message to verify your host IP. If you do not, you will likely run into issues throughout the workshop  

5. After the VM is built, SSH into the VM and confirm the samples repo was mounted. You should see multiple files in `/home/vagrant/containers`.
```bash
# SSH into the VM
vagrant ssh

# From your SSH session in the VM, list the contents of the samples repo.
[vagrant@m1 ~]$ ls /home/vagrant/containers   #<------------- LIST THE CONTENTS OF THE SAMPLES REPO

best-practices.md  DTaaS  http-echo  jenkins  leap  perl  python  README.md  simple_nodejsapp  springboot  toolbox
```

#### Issues

If the `ls /home/vagrant/containers` command returns an empty result, either your environment variable is set up incorrectly or you need to execute a `vagrant reload`.   

---

Continue to [writing Dockerfiles](./3-dockerfiles.md).

Return to [Table of Contents](../README.md#agenda)
