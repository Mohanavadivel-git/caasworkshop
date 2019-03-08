# Lesson 1, App Container Images

### Installing CaaS localdev

Localdev uses Vagrant and VirtualBox to run a virtual machine on your workstation. The VM contains an installation of OpenShift as well as a set of container image build tools.

CaaS localdev can be obtained from the localdev [repo](https://github.ford.com/containers/localdev) on GitHub. In the exercise below, you will install the pre-requisite dependencies for localdev, clone the repo, and start up localdev.

#### Exercise

To get started with localdev:
1. Install the software required to run localdev on your workstation. Here is the [required software](https://github.ford.com/containers/localdev#minimum-requirements).
   - Essentially, you'll need Git, Vagrant, VirtualBox, and a few other things you probably already have installed.
1. Open a terminal 'as Administrator' on Windows, and do the following to pull down localdev and start it. The instructions below are in Git Bash, so you may need to modify them if you prefer Windows cmd or Powershell.

```
# Change directory to your project workspace if you have a preferred one.
$ cd ~/workspace

# Clone the localdev git repo.
$ git clone git@github.ford.com:Containers/localdev.git
$ cd localdev
$ git checkout -b tags/v3.11.82-1

# Set an env var to use the build-host profile.
$ export LOCAL_DEV_PROFILE='build-host'

# Start up localdev virtual machine.
$ vagrant up

# You will be prompted to confirm your IP address. Press Y to confirm it. See example output below.
 INFO oc-localdev: OpenShift localdev v3.11.82-1
 INFO oc-localdev: Current OpenShift localdev profile 'build-host'
Bringing machine 'openshift-enterprise-3.11.82-master' up with 'virtualbox' provider...
==> openshift-enterprise-3.11.69-master: Running triggers before up ...
==> openshift-enterprise-3.11.69-master: Executing trigger before up or provision...
No environment variable 'DEFAULT_HOST_IP' found                                          |-------------|
Please verify if your host IP is 19.47.12.230 [y/n] y  <---------------------------------| TYPE Y HERE |
 INFO oc-localdev: Writing CoreDNS Corefile                                              |-------------|
 INFO oc-localdev: Writing CoreDNS zonefile
...
...
```

When you issue `vagrant up` vagrant is starting the localdev VM in the VirtualBox hypervisor. It will take a while for the VM to start. Review the [Quickstart](https://github.ford.com/containers/localdev#quick-start) section in the localdev README while you wait.

Also note that we are using the `build-host` profile, so the VM that starts will not be running CaaS. You'll notice if you try to access localdev from a web browser, you'll get an error because OpenShift isn't started. That's OK because we will just be building container images in the next exercise which is what the `build-host` profile is optimized for.

Once the scrolling stops and you get your terminal prompt back, check the status of the VM. The response should look like this:

```
$ vagrant status

 INFO oc-localdev: OpenShift localdev v3.11.82-1
 INFO oc-localdev: Current OpenShift localdev profile 'build-host'
 INFO oc-localdev: Setting up host directory sharing:
        Host Directory:C:/Users/jpotte46/workspace/
        VM Directory:/home/vagrant/workspace
Current machine states:

openshift-enterprise-3.11.82-master running (virtualbox)

The VM is running...
```

---  

Continue to [Lesson 1.3](./lesson1.3.md).