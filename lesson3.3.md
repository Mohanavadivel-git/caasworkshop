# Lesson 3, Advanced Topics

Further Reading: [Storage Operations and Troubleshooting Guide](https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/storage_troubleshooting_day2_guide.md#storage-operations-and-troubleshooting-guide)

## File Storage

Openshift comes with an NFS provisioner in localdev. The provisioner carries out the responsibility of creating or deleting new storages. You can request storage by providing a class type, a name, an access type, and a storage size. 

### Class Types

The StorageClass are different "classes" of storage that are offered. They might differ in quality-of-service levels, backup policies, or other arbitrary policies. In localdev (and in the exercise), the storage class available is NFS. In production Openshift, the classes are: 

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

1. If you have not already completed building the sample application and pushing it to Openshift, return to [Lesson 1.2](https://github.ford.com/JPOTTE46/caas-workshop/blob/master/lesson1.2.md) and complete through Lesson 2.2. Then, delete the python app configuration. 

```
[vagrant@m1 ~]$ oc delete all -l app=python
```

2. Navigate to the python sample project and click the Storage tab/icon and click "Create Storage". ([Direct Link](https://api.oc.local:8443/console/project/python/browse/storage))

3. Fill out the form with the following options and click create
- **Storage Class**: nfs
- **Name**: my-storage-claim
- **Access Mode**: Shared Access (RWX)
- **Size**: 5 MiB

> :floppy_disk: Size of volume needs to fit within the constraints of your app size limits - hence the small size of this drive

### Applying the Changes in the Manifest

4. Open the samples repo you previously cloned and open the python.yaml file (located at /manifest/python.yaml) in your editor of choice

> :raised_hands: Because your samples drive is mounted to the VM, you can edit the YAML file outside the VM

5. Uncomment lines 124-130 in the python.yaml and save the changes. 

> :eyes: If those lines are not there or do not align with the code below, please add them and ensure the tabbing/spacing aligns with the rest of the yaml file. 

```
        volumeMounts:
          - name: "volume-claim"
            mountPath: "/home/new"
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

> :exclamation: :collision: :fire: Deleting your PVC will delete the file storage and all files saved there. Do not execute this command in production unless you are SURE you want to delete your storage and all associated files :fire: :collision: :exclamation:

### Storage Creation via Manifest

13. Re-open the python.yaml in the manifest folder and uncomment lines 131-142

> :eyes: If those lines are not there, please add them and ensure the tabbing/spacing aligns with the rest of the yaml file. 

```
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

```
claimName: "my-manifest-claim"
```

15. Since we deleted to application configurations, run the create command again. 

```
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/python/manifest/python.yaml
```

You'll see that the [storage was created with the name specified in line 135](https://api.oc.local:8443/console/project/python/browse/storage). Navigating to the terminal of a running pod, you will find the same mount path has been created. 

```
(app-root)sh-4.2$ ls /home
new
```

This path DOES NOT contain the myFile.txt we created earlier because that storage was deleted. When the storage is deleted, the provisioner in Openshift will delete the actual storage and contents.

16. Return to your Bash/Powershell terminal and delete the file share and app configurations.

```
[vagrant@m1 ~]$ oc delete all -l app=python
[vagrant@m1 ~]$ oc delete pvc my-manifest-claim
```

