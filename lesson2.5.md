## Day 1 - Lesson 2

## Best Practices for CaaS Manifests

Through the CaaS manifest you have significant control over how CaaS will run your application. App teams can define, test, and revise the resources allocation to an application without any action from an operations team.

#### Avoid defaults

If you do not specify a value in the manifest, CaaS will use a ridiculous default, i.e. 10 MB of RAM. So if your app exhibits unexpected behavior or poor performance, check that you have explicitly defined values such as CPU, memory, readiness health endpoints, etc... in the app's manifest.

The manifests in the samples repository should get you started. For more details, read the [Developer Guide](https://docs.openshift.com/container-platform/3.11/dev_guide) on the OpenShift website.

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
    
To end Day 1 of the workshop, we will execute a `vagrant suspend`. To do so, you must exit out of SSH first. 

```bash
[vagrant@m1 ~]$ exit
$ vagrant suspend
```

When we issue a `vagrant up` command on Day 2, we will still have our project, secret, and connections saved. 

---  

Continue to [Lesson 3](./lesson3.1.md).

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop/tree/workshop-reformat#agenda)
