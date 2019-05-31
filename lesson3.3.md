# Lesson 3, Advanced Topics

Further Reading: [Storage Operations and Troubleshooting Guide](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/storage_troubleshooting_day2_guide.md#storage-operations-and-troubleshooting-guide)

## File Storage

Openshift comes with an NFS provisioner in localdev. The provisioner carries out the responsibility of creating or deleting new storages. You can request storage by providing a class type, a name, an access type, and a storage size. 

### Class Types

The StorageClass are different "classes" of storage that are offered. They might differ in quality-of-service levels, backup policies, or other arbitrary policies. In localdev, the available storage classes are nfs and rook-ceph-block-replicated. We will be using nfs. In production Openshift, the classes are: 

- ecc-block-performance
- ecc-file-performance
- edc1h1-block-extreme
- edc1h1-block-performance
- edc1h1-file-extreme
- edc1h1-file-performance

> :exclamation: Block volumes CANNOT be attached to multiple container instances at the same time - file volumes CAN. Mounting and cross-mounting are only for file based storage plans - block storage plans cannot be concurrently mounted.

### Access Types

- Single User (RWO - Read Write Once)
  - The volume can be mounted as read-write by a single node
- Shared Access (RWX - Read Write Many)
  - The volume can be mounted as read-write by many nodes
- Read Only (ROX - Read Only Many)
  - The volume can be mounted read-only by many nodes

> :point_right: Need to provide shared access if you want multiple applications to be able to write to it (e.g FTP Server)

## Exercise

### Storage Creation via Web Console

1. If you have not already completed building the sample application and pushing it to Openshift, return to [Lesson 1.2](https://github.ford.com/JPOTTE46/caas-workshop/blob/master/lesson1.2.md) and work to this lesson. Then, delete the springboot app configuration. 

```bash
[vagrant@m1 ~]$ oc delete all -l app=springboot-hello-world
```

2. Navigate to the Springboot sample project and click the Storage tab/icon and click "Create". ([Direct Link](https://api.oc.local:8443/console/project/springboot-hello-world/browse/storage))

3. Fill out the form with the following options and click create
- **Storage Class**: nfs
- **Name**: my-storage-claim
- **Access Mode**: Shared Access (RWX)
- **Size**: 5 MiB

> :floppy_disk: Size of volume needs to fit within the constraints of your app size limits - hence the small size of this drive

### Applying the Changes in the Manifest

4. Open the samples repo you previously cloned and open the deployment.yaml file (located at springboot/manifest/deployment.yaml) in your editor of choice

> :raised_hands: Because your samples drive is mounted to the VM, you can edit the YAML file outside the VM

5. Uncomment lines 124-130 in the deployment.yaml and save the changes. 

If you do not have those lines, please retrieve the [latest yaml file](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/manifest/deployment.yaml) which will contain them. 

> :eyes: If you manually add these lines, the yaml needs to be properly aligned. In this example - volumeMounts needs to be aligned with "readinessProbe" and "volumes" needs to be aligned with "containers"

```yaml
        volumeMounts:
          - name: "volume-claim"
            mountPath: "/var/lib/new"
      volumes:
      - name: "volume-claim"
        persistentVolumeClaim:
          claimName: "my-storage-claim"
```

- claimName: Refers the name of the storage you defined in the web console
- mountPath: Refers to the path within the container that will be mounted to the volume share

6. Run the following command to apply the changes

```bash
[vagrant@m1 ~]$ oc apply -f ~/containers/springboot/manifest/deployment.yaml
```

### Verifying Results

7. In the Openshift web console, [in the Python project, go to Applications->Pods](https://api.oc.local:8443/console/project/springboot-hello-world/browse/pods). Selecting the Pod with a "Running" status and click the terminal tab. 

8. In the Openshift terminal, confirm the mount path defined in the yaml file exists

```bash
(app-root)sh-4.2$ ls /var/lib
alternatives  dbus  games  initramfs  machines  misc  new  rhsm  rpm  rpm-state  systemd  yum
# The drive "new" exists so we know the path was created successfully
```

We can also access this pod terminal through our existing bash/powershell window using [`oc rsh <pod>`](https://docs.openshift.com/container-platform/3.11/dev_guide/ssh_environment.html)
```bash
[vagrant@m1 ~]$ oc rsh $(oc get pods -o name)
sh-4.2$ ls /var/lib
alternatives  dbus  games  initramfs  machines  misc  new  rhsm  rpm  rpm-state  systemd  yum
```

9. Let's write a text file to this file share. You can use the console method or the remote shell method. 

```bash
# Console Method
(app-root)sh-4.2$ cd /var/lib/new
(app-root)sh-4.2$ echo "I am writing to my new file share" > myFile.txt
(app-root)sh-4.2$ cat myFile.txt
I am writing to my new file share
```

```bash
# Remote shell method
sh-4.2$ cd /var/lib/new
sh-4.2$ echo "I am writing to my new file share" > myFile.txt
sh-4.2$ cat myFile.txt
I am writing to my new file share
```

10. We now are going to delete all the existing pods to demonstrate that the file persists. To do this, you must return to your bash/powershell window. If you `oc rsh` into the pod, then you must exit the pod first. 

```bash
# If you did not `rsh` into the pod, do not run the exit command
sh-4.2$ exit       
exit
[vagrant@m1 ~]$ oc delete pod --all
```

11. After successfull deletion of the pod, a new will pod will be spun up automatically. We will now show that file perisisted. You can either return to the Openshift console and go to [Applicatons->Pods](https://api.oc.local:8443/console/project/springboot-hello-world/browse/pods), select the new running pod, and go to the terminal.  Alternatively, you can `oc rsh` into the new pod from your bash/powershell window. 

```bash
# Console terminal method
(app-root)sh-4.2$ cat /var/lib/new/myFile.txt
I am writing to my new file share
```

```bash
# Remote Shell Method
[vagrant@m1 ~]$ oc rsh $(oc get pods -o name)
sh-4.2$ cat /var/lib/new/myFile.txt
I am writing to my new file share
```

12. If you ran the commands in the Console terminal, return to your Bash/Powershell terminal and delete the file share and app configurations. If you ran the command while `oc rsh` into the pod, exit first, and then run the delete command

```bash
# Run the below command only if you `oc rsh` into the pod
sh-4.2$ exit

[vagrant@m1 ~]$ oc delete all -l app=springboot-hello-world
[vagrant@m1 ~]$ oc delete pvc my-storage-claim
```

> :exclamation: :collision: :fire: Deleting your PVC will delete the file storage and all files saved there. Do not execute this command in production unless you are SURE you want to delete your storage and all associated files :fire: :collision: :exclamation:

### Storage Creation via Manifest

13. Re-open the deployment.yaml in the manifest folder and uncomment lines 131-142

> :eyes: If those lines are not there, please add them and ensure the tabbing/spacing aligns with the rest of the yaml file. 

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-manifest-claim
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs
  resources:
    requests:
      storage: 10Mi
```

Everything we defined in step 3 we are now doing in the yaml file. We are defining a PVC, giving it a name, defining its access mode, storage class, and size to be allocated. 

14. Since we are using a different name, edit line 130 of the file to reflect this change.

```yaml
claimName: "my-manifest-claim"
```

15. Since we deleted the application configurations, run the create command again. 

```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/deployment.yaml
```

You'll see that the [storage was created with the name specified in line 135](https://api.oc.local:8443/console/project/springboot-hello-world/browse/storage). Navigating to the terminal of a running pod, you will find the same mount path has been created. 

```bash
(app-root)sh-4.2$ ls /var/lib
alternatives  dbus  games  initramfs  machines  misc  new  rhsm  rpm  rpm-state  systemd  yum
```

Again, you can run this in the bash/powershell window after you `exec` into the pod. 

```bash
[vagrant@m1 ~]$ oc rsh $(oc get pods -o name)
sh-4.2$ ls /var/lib
alternatives  dbus  games  initramfs  machines  misc  new  rhsm  rpm  rpm-state  systemd  yum
```

As you can see, the `new` folder was created which serves as the mount point for our VM and the persistent volume claim. 

This path **DOES NOT** contain the myFile.txt we created earlier because that storage was deleted. When the storage is deleted, the provisioner in Openshift will delete the actual storage and contents.

16. Return to your Bash/Powershell terminal and delete the file share and app configurations. Once again, if you are `oc rsh` into the pod, exit first. 

```bash
# Only run the exit command if you are `rsh` into the pod
sh-4.2$ exit
exit
[vagrant@m1 ~]$ oc delete all -l app=springboot-hello-world
[vagrant@m1 ~]$ oc delete pvc my-manifest-claim
```

17. Exit VM and destroy 
```bash
[vagrant@m1 ~]$ exit
logout
Connection to 127.0.0.1 closed.

$ vagrant destroy -f
```

You have reached the end of the workshop :clap: