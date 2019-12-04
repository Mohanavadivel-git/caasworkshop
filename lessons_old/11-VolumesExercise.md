## Creating Volumes

Further Reading: [Storage Operations and Troubleshooting Guide](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/storage_troubleshooting_day2_guide.md#storage-operations-and-troubleshooting-guide)

### Storage Creation via Web Console

1. Let us first delete the current running deployment of our application. 

```bash
[vagrant@m1 ~]$ oc delete -f /home/vagrant/containers/springboot/manifest/deployment-1.yaml
```

2. Navigate to your namespace in the Console and click the Storage tab/icon and click "Create". ([Direct Link](https://api.oc.local:8443/console/project/my-namespace/browse/storage))

3. Fill out the form with the following options to create the persistent volume claim (PVC) and click "create." 
- **Storage Class**: nfs
- **Name**: my-storage-claim
- **Access Mode**: Shared Access (RWX)
- **Size**: 5 MiB

> :floppy_disk: Size of volume needs to fit within the constraints of your app size limits - hence the small size of this drive

### Applying the Changes in the Manifest

4. Open the file `deployment-2.yaml` and review the additions at lines 124-130. 

```yaml
        volumeMounts:
          - name: "volume-claim"            #<-------|
            mountPath: "/var/lib/mystorage" #        | These two lines must match
      volumes:                              #        |
      - name: "volume-claim"                #<-------|
        persistentVolumeClaim:
          claimName: "my-storage-claim"
```

- **volumes**
  - *name* - A name to reference the volume in our manifest
  - *persistentVolumeClaim* - Tells Openshift that this volume is a persistent volume claim
    - *claimname* - The name of the PVC we just created
- **volumeMounts**
  - *name* - The name we created for our volume in the volumes section 
  - *mountPath* - The location within the container we want our volume to be mounted 

5. Change line 59 to reflect your tag name in the `deployment-2.yaml` file. 
```yaml
image: registry.ford.com/devenablement/workshop:0.0.1 #<---Your Tag Here
```

6. After making the edit for your tag, let's create our new deployment that will leverage our new file storage. 

```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/deployment-2.yaml
```

### Writing a file to the storage

7. In the Openshift web console, [in the Spring project, go to Applications->Pods](https://api.oc.local:8443/console/project/my-namespace/browse/pods). Selecting the Pod with a "Running" status and click the terminal tab. 

8. In the Openshift terminal, confirm the mount path defined in the yaml file exists

```bash
sh-4.2$ ls /var/lib
alternatives  dbus  games  initramfs  machines  misc  mystorage  rhsm  rpm  rpm-state  systemd  yum
```

9. Let's write a text file to this file share. 
```bash
sh-4.2$ cd /var/lib/mystorage
sh-4.2$ echo "I am writing to my new file share" > myFile.txt
sh-4.2$ cat myFile.txt
I am writing to my new file share
```

### Verifying Results

10. We now are going to delete all the existing pods to demonstrate that the file persists. You can delete the pod in the right-hand corner of the console and click `Actions->Delete`. 

You can delete the pod(s) outside of the console using terminal/bash/powershell. 

```bash
[vagrant@m1 ~]$ oc get pods
NAME                                     READY     STATUS    RESTARTS   AGE
springboot-hello-world-b4f5f74c6-wc5p9   1/1       Running   0          2m

# Use the exact pod name in the `oc delete pod` command
[vagrant@m1 ~]$ oc delete pod springboot-hello-world-b4f5f74c6-wc5p9
pod "springboot-hello-world-b4f5f74c6-wc5p9" deleted
```

11. After successfull deletion of the pod, a new will pod will be spun up automatically. We will now show that file perisisted. You can either return to the Openshift console and go to [Applicatons->Pods](https://api.oc.local:8443/console/project/my-namespace/browse/pods), select the new running pod, and go to the terminal. 

12. Check that your text file persisted and exists in our new pod. 

```bash
sh-4.2$ cat /var/lib/mystorage/myFile.txt
I am writing to my new file share
```

### Accessing the Pod Terminal Outside the Console

13. We can also access this pod terminal through our existing bash/powershell window using [`oc rsh <pod name>`](https://docs.openshift.com/container-platform/3.11/dev_guide/ssh_environment.html). First, we need a pod name. 
```bash
[vagrant@m1 ~]$ oc get pods
NAME                                      READY     STATUS    RESTARTS   AGE
springboot-hello-world-7d6cbdd9f7-hf56h   1/1       Running   0          14m
```

14. Copy your pod name from running the above command into the command below. Notice that the shell prompt changes to indicate you are now in the container. 

```bash
[vagrant@m1 ~]$ oc rsh <POD-NAME>
sh-4.2$ 
```

15. List the contents of /var/lib/mystorage to show you can access your files via this method as well.
```bash
sh-4.2$ ls /var/lib/mystorage
myFile.txt
```

16. Let's clean up our environment by deleting our deployment and our storage. 
```bash
# Run the below command only if you `oc rsh` into the pod
sh-4.2$ exit

[vagrant@m1 ~]$ oc delete -f /home/vagrant/containers/springboot/manifest/deployment-2.yaml
[vagrant@m1 ~]$ oc delete pvc my-storage-claim
```

> When you delete a PVC - you delete all its contents. Don't delete storages unless you are certain you do not need the files stored in them. 

### Storage Creation via Manifest

17. Open the storage.yaml file to review the contents. 

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-storage-claim
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs
  resources:
    requests:
      storage: 5Mi
```

Everything we defined in step 3 we are now doing in the yaml file. We are defining a PVC, giving it a name, defining its access mode, storage class, and size to be allocated. 

18. Run the create command using the `storage.yaml` file to create the storage. 
```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/storage.yaml
```

19. Now, let's re-create our deployment. 

```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/deployment-2.yaml
```

You'll see that the [storage was created with the name specified](https://api.oc.local:8443/console/project/my-namespace/browse/storage). Navigating to the terminal of a running pod, you will find the same mount path has been created. 

20. Confirm our storage was mounted to the container again. 
```bash
sh-4.2$ ls /var/lib
alternatives  dbus  games  initramfs  machines  misc  mystorage  rhsm  rpm  rpm-state  systemd  yum
```
This path **DOES NOT** contain the myFile.txt we created earlier because that storage was deleted. When the storage is deleted, the provisioner in Openshift will delete the actual storage and contents.

21. Let's clean up our environment by deleting our deployment. We will leave our PVC for now. 

```bash
[vagrant@m1 ~]$ oc delete -f /home/vagrant/containers/springboot/manifest/deployment-2.yaml
```

Continue to [writing application logs to a volume](./12-VolumeLogs.md)

Return to [Table of Contents](../README.md#agenda)