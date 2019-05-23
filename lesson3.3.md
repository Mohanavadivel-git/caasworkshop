# Lesson 3, Advanced Topics

[Storage Operations and Troubleshooting Guide](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/storage_troubleshooting_day2_guide.md#storage-operations-and-troubleshooting-guide)

## File Storage

Openshift comes with an NFS provisioner in localdev. The storage provisioner carries out the responsibility of creating or deleting new volumes. You can request volumes by providing a class type, a name, an access type, and a storage size. 

### Class Types

The StorageClass are different "classes" of storage that are offered. They might differ in qualityof-service levels, backup policies, or other arbitrary policies. In localdev (and in the exercise) the, the storage class available is NFS. In production Openshift, the classes are: 

- ecc-block-performance
- ecc-file-performance
- edc1h1-block-extreme
- edc1h1-block-performance
- edc1h1-file-extreme
- edc1h1-file-performance

> NOTE: Block volumes CANNOT be attached to multiple container instances at the same time - file volumes CAN. Mounting and cross-mounting are only for file based storage plans - block storage plans cannot be concurrently mounted. 

### Access Types

- Single User (RWO)
- Shared Access (RWX)
- Read Only (ROX)

> NOTE: Need to provide shared access if you want multiple applications to be able to write to it (e.g FTP Server)

## Exercise

### Creating the Volume Share

1. If you have not already completed building the sample application and pushing it to Openshift, return to [Lesson 1.2](https://github.ford.com/JPOTTE46/caas-workshop/blob/master/lesson1.2.md) and complete through Lesson 2.2, but do not delete the objects at the end (i.e. do not execute the "oc delete all -l app=python" command)

- If you have already run the delete command, re-run the create command below:

```
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/python/manifest/python.yaml
```

2. Navigate to the [python sample project](https://api.oc.local:8443/console/project/python/overview) and click the Storage tab/icon and click "Create Storage". 

3. Fill out the form with the following options
- **Storage Class**: nfs
- **Name**: my-storage-claim
- **Access Mode**: Shared Access (RWX)
- **Size**: 5 MiB

> NOTE: Size of volume needs to fit within the constraints of your app size limits - hence the small size of this drive

### Applying the Changes in the Manifest

4. Open the samples repo you previously cloned and open the python.yaml file (located at /manifest/python.yaml) in your editor of choice

> NOTE: Because your samples drive is mounted to the VM, you can edit the YAML file outside the VM

5. Uncomment lines 124-130 in the python.yaml and save the changes.

```
        volumeMounts:
          - name: "volume-claim"
            mountPath: "/home/newPath"
      volumes:
      - name: "volume-claim"
        persistentVolumeClaim:
          claimName: "my-storage-claim"
```

- claimName: Refers the name of the storage you defined in the web console
- mountPath: Refers to the path within the container that will be mounted to the volume share

6. Run the following command to apply the changes

```
[vagrant@m1 ~]$ oc apply -f ~/containers/python/manifest/python.yaml
```

### Verifying Results

7. In the Openshift web console, [in the Python project, go to Applications->Pods](https://api.oc.local:8443/console/project/python/browse/pods). Selecting the Pod with a "Running" status and click the terminal tab. 

8. In the Openshift terminal, confirm the mount path defined in the yaml file exists

```
(app-root)sh-4.2$ ls /home
new
```

9. Write a new text file to this file share

```
(app-root)sh-4.2$ cd /home/new
(app-root)sh-4.2$ echo "I am writing to my new file share" > myFile.txt
(app-root)sh-4.2$ cat myFile.txt
I am writing to my new file share
```

10. Return to your Bash/Powershell terminal and run the following commands to delete all existing pods

```
[vagrant@m1 ~]$ oc delete pod --all
```

11. After successfull deletion, return to the Openshift console and go to [Applicatons->Pods](https://api.oc.local:8443/console/project/python/browse/pods) and select the new running pod. Run the following command to confirm your file share still exists in the new pod. 

```
(app-root)sh-4.2$ cat /home/new/myFile.txt
I am writing to my new file share
```

12. Return to your Bash/Powershell terminal and delete the file share and app configurations.

```
[vagrant@m1 ~]$ oc delete all -l app=python
[vagrant@m1 ~]$ oc delete pvc my-storage-claim
```

### Storage Creation via Manifest

13. Re-open the python.yaml in the manifest folder and uncomment lines 131-142

```
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-manifest-claim
spec:
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  resources:
    requests:
      storage: 10Mi
```

14. Edit line 130 of the file to read:

```
claimName: "my-manifest-claim"
```

15. Execute the create command again
```
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/python/manifest/python.yaml
```

You'll see that the storage was created with the name specified in line 135. Navigating to the terminal of a running pod, you will find the same mount path has been created. 

```
(app-root)sh-4.2$ ls /home
new
```

This path DOES NOT contain the myFile.txt we created earlier because that storage was deleted. When the storage is deleted, the provisioner in Openshift will delete the actual NAS drive.  