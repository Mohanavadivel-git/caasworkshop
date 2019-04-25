# Workstation Setup

Before attending the workshop, you must pre-install some software on your laptop or workstation. You will likely be on wireless during the workshop, and the initial installation and setup of these packages will take hours if performed over wireless. So please install ahead of time to avoid wasting class time.

At a high level, these set up instructions will install Vagrant and VirtualBox on your workstation which will be used to run a virtual machine (VM). During the workshop, you will be working from the VM to complete the exercises.

### Install Software on Workstation
- Ensure that your workstation meets the minimal requirement of **4 CPU cores and 8GB of RAM**.
- Install the following software on your workstation.
  - Text editor of your choice, such as Notepad++, Eclipse, IntelliJ, [Visual Studio Code](https://code.visualstudio.com/), etc...
  - [Git](https://git-scm.com/downloads)
  - [Vagrant v2.2.2+](https://www.vagrantup.com/downloads.html)
  - VirtualBox v6.0.0+, [Windows download](https://files.caas.ford.com:9443/virtualbox/6.0.4/VirtualBox-6.0.4-128413-Win.exe) or [MacOS download](https://files.caas.ford.com:9443/virtualbox/6.0.4/VirtualBox-6.0.4-128413-OSX.dmg)

### Get CaaS Localdev

CaaS localdev is a VM image that runs a small installation of OpenShift CaaS. When you are finished with the instructions below, you will have a VM on your workstation that you can use to build and run app container images.

Open a terminal as Administrator and complete the instructions below. Note that the instructions are optimized for Git Bash on Windows. You may have to modify the commands slightly if you are using PowerShell or cmd as your terminal.

```
# Change directory to your project workspace if you have a preferred one.
cd ~/workspace

# Clone the localdev git repo and checkout the latest version.
git clone git@github.ford.com:Containers/localdev.git
cd localdev
git checkout tags/v3.11.98-1

# Pick ***ONE*** of the options below to set an env var used by localdev.
export LOCAL_DEV_PROFILE='basic-cnx'  # <----- Git Bash/MacOS/Linux OR
$env:LOCAL_DEV_PROFILE = 'basic-cnx'  # <----- Windows Powershell OR
SET LOCAL_DEV_PROFILE='basic-cnx'     # <----- Windows legacy command/cmd shell

# Start up localdev virtual machine.
vagrant up

# You will be prompted to confirm your IP address. Press Y to confirm it. See example output below.
# After that, you can take a break if you want because the install
# can take up to 15 minutes even on a hard-wired network connection.

 INFO oc-localdev: OpenShift localdev v3.11.98-1
 INFO oc-localdev: Current OpenShift localdev profile 'basic-cnx'
Bringing machine 'openshift-enterprise-3.11.98-master' up with 'virtualbox' provider...
==> openshift-enterprise-3.11.69-master: Running triggers before up ...
==> openshift-enterprise-3.11.69-master: Executing trigger before up or provision...
No environment variable 'DEFAULT_HOST_IP' found                                          |-------------|
Please verify if your host IP is 19.47.12.230 [y/n] y  <---------------------------------| TYPE Y HERE |
 INFO oc-localdev: Writing CoreDNS Corefile                                              |-------------|
 INFO oc-localdev: Writing CoreDNS zonefile
...
...
```

Once the scrolling stops from the commands above and you get your terminal prompt back, check the status of the VM with `vagrant status`. The response should look like this:

```
vagrant status

 INFO oc-localdev: OpenShift localdev v3.11.98-1
 INFO oc-localdev: Current OpenShift localdev profile 'basic-cnx'
 INFO oc-localdev: Setting up host directory sharing:
        Host Directory:C:/Users/jpotte46/workspace/
        VM Directory:/home/vagrant/workspace
Current machine states:

openshift-enterprise-3.11.98-master running (virtualbox)

The VM is running...
```

If the output looks like the output above, then you have a running VM on your workstation that is running a local copy of OpenShift CaaS!
<!--
Leave the terminal open because you will come back to it soon to suspend the VM.

You can also check that you can access the OpenShift Web Console opening a web browser and opening [https://console.oc.local:8443](https://console.oc.local:8443. **Note that your web browser will give you an SSL certificate error.** The localdev installation of OpenShift CaaS uses a self-signed certificate which causes the browser alert. Just proceed and accept the certificate. You may have to do this twice because there is a URL redirect.

You will know the OpenShift Web Console is working if you get a web page with a Ford Mustang on it with a login prompt. If you'd like to explore the OpenShift Web Console before the workshop, the credentials are:

    ```
    Username: admin
    Password: sandbox
    ```
-->
You will now suspend the VM by typing `vagrant suspend` in the terminal. This will gracefully pause and save the state of the VM. The response should look like this:

```
vagrant suspend

 INFO oc-localdev: OpenShift localdev v3.11.98-1
 INFO oc-localdev: Current OpenShift localdev profile 'basic-cnx'
==> openshift-enterprise-3.11.98-master: Running triggers before suspend ...
==> openshift-enterprise-3.11.98-master: Running trigger: suspend...
==> openshift-enterprise-3.11.98-master: Saving VM state and suspending execution...
```

You're done! At the workshop, you will be able to resume the VM quickly with `vagrant up`. If you want to know more about CaaS localdev, you can review the README in the localdev [repo](https://github.ford.com/containers/localdev) on GitHub.
