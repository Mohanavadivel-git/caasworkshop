# Lesson 2, Running Apps in CaaS

### Restarting CaaS localdev

Next you will be deploying to CaaS localdev the container image you built in the last session. Deploying to localdev is similar to how you might deploy the container image to the production instance of CaaS.

<!-- Your instance of localdev is probably still running with the `build-host` profile. Which is optimized for building container images, but does not start the OpenShift service. So before you can deploy the app container, you need to restart CaaS localdev with the `basic-cnx` profile. Instructions for doing this are included in the exercise notes below. -->

Reminder: Must run shell as administrator


#### Exercise

```
# Change the localdev profile and restart VM
$ cd ~/workspace/localdev

# If not already set, then set profile.
$ export LOCAL_DEV_PROFILE='basic-cnx'

# If not already set, then set synchronized folders. Modify the path and CDSID for your environment.

#On MacOS
$ export ADDITIONAL_SYNCED_FOLDERS='/Users/CDSID/Projects/workspace/samples=>/home/vagrant/containers'

# On Windows Powershell
$env:ADDITIONAL_SYNCED_FOLDERS = 'C:/Users/CDSID/Projects/workspace/samples=>/home/vagrant/containers'

#On Windows GitBash
$ export ADDITIONAL_SYNCED_FOLDERS='/C/Users/CDSID/Projects/workspace/samples=>/home/vagrant/containers'

$ vagrant destroy -f
$ vagrant box update
$ vagrant box prune

$ vagrant up
```

Now your instance of localdev has started with a full installation of OpenShift. Test to confirm that OpenShift is running and ready by opening the web management in a browser at https://console.oc.local:8443/. Your browser will give you an error about the self-signed SSL certificate, but just tell it to proceed anyway. And you will have to do that twice because of a redirect.

Once you get a log in prompt, use the following:

```
Username: admin
Password: sandbox
```

In addition to the web interface, you can communicate directly with the OpenShift API using a command line tool called `oc` from Red Hat, or the more generic Kubernetes command-line tool `kubectl`. This workshop uses `oc`. Try this:
```
$ vagrant ssh

[vagrant@m1 ~]$ oc login https://api.oc.local:8443
Username: admin
Password: sandbox
Login successful.
```

<!---
If you get an error like, "no such host" or "couldn't resolve host", the issue is likely with the name resolution of `console.oc.local`. The localdev installation runs a local DNS service to provide name resolution for the `oc.local` domain. Sometimes, you will need to wait a bit longer for the DNS service to start, or manually flush your DNS cache with `ipconfig /flushdns` on Windows (or escape the fwd slash in Git Bash like `ipconfig //flushdns`).
-->
---  

Continue to [Lesson 2.2](./lesson2.2.md).
