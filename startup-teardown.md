### Start Up

When bringing up localdev, if you do not save your environment variables as permanent environment variables, you will have to re-declare your environment variables again.

```bash
# Bash/Mac
export LOCAL_DEV_PROFILE='basic-cnx'
export ADDITIONAL_SYNCED_FOLDERS='/c/YOUR_PATH_TO_REPO/samples=>/home/vagrant/containers'

#Powershell
$env:LOCAL_DEV_PROFILE='basic-cnx'
$env:ADDITIONAL_SYNCED_FOLDERS='/c/YOUR_PATH_TO_REPO/samples=>/home/vagrant/containers'
```

Navigate to the localdev directory and bring it up. 
```bash
$ cd <PATH_TO_LOCALDEV_DIRECTORY>
$ vagrant up
```

Additionally, when you start up localdev, it will default to the `cluster-ops` project. You must change to using your project when you log in. 

```bash
[vagrant@m1 ~]$ oc project my-namespace
```

If you had to delete your VM, you will need to re-deploy the secret for Quay. 
```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/pullsecret.yaml
secret/devenablement-workshop-pull-secret created
```

### Teardown

When you want to take a break, work an another project, or stop for the day, you need to clean up your development environment. With vagrant, there are few different commands that you can use. 

- **Suspend**:
    - Save current running state of the machine
    - `vagrant up` will resume where you left off
    - Very fast to "re-boot" 
    - VM uses lots of disk space to store the state of the VM RAM on disk
- **Halt**:
    - Gracefully shut down guest OS and power down guest machine
    - Preserves contents of disk, will cleanly start with `vagrant up`
    - Takes a little extra time to sstart up
    - Guest machine consumes some disk space
- **Destroy**:
    - Removes all traces of guest machine from system
    - Disk/RAM used by guest machine is reclaimed, host machine is clean
    - `vagrant up` is a completely fresh start
    - Takes extra time to reimport machine and re-provision it
    
For the purposes of the workshop, execute a `vagrant suspend` so that we can return to our material already loaded and created. 

```bash
[vagrant@m1 ~]$ exit
$ vagrant suspend
```

When we return and issue a `vagrant up`, we will still have our project, secret, and connections saved. 

---  

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop#agenda)
