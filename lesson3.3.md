# Lesson 3: Logging, Monitoring, and Storage

## Kubernetes Volumes

Since containers are not persistent, all their contents are cleared whenever the pod they are contianed within is destroyed. The file system is completely fresh with each pod and file systems do not persist unless you define them through persisten volume claims. 

Openshift comes with an NFS provisioner in localdev. The provisioner carries out the responsibility of creating or deleting new storages. You can request storage by providing a class type, a name, an access type, and a storage size. 

### Diagram

![Dynamic Persistent Volume](https://github.ford.com/DevEnablement/caas-workshop/blob/master/images/PVC_Diagram.png)

### Class Types

The StorageClass are different "classes" of storage that are offered. They might differ in quality-of-service levels, backup policies, or other arbitrary policies. In localdev, the available storage classes are nfs and rook-ceph-block-replicated. We will be using nfs. In production Openshift, the classes are: 

- ecc-block-performance
- ecc-file-performance
- edc1h1-block-extreme
- edc1h1-block-performance
- edc1h1-file-extreme
- edc1h1-file-performance

> :exclamation: Block volumes CANNOT be attached to multiple container instances at the same time - file volumes CAN. Mounting and cross-mounting are only for file based storage plans - block storage plans cannot be concurrently mounted.

Below are further definitions for the storage classes. IOPS are a measure of I/O per second. 

- **File** - NAS
- **Block** - SAN
- **Performance** 
    - Maximum SLO: 4096 IOPS/TB
    - Minimum SLA: 2048 IOPS/TB
    - Database and virtualized applications
- **Extreme** 
    - Maximum SLO: 12288 IOPS/TB
    - Minimum SLA: 6144 IOPS/TB
    - Latency-sensitive applications

### Access Types

- Single User (RWO - Read Write Once)
  - The volume can be mounted as read-write by a single node
- Shared Access (RWX - Read Write Many)
  - The volume can be mounted as read-write by many nodes
- Read Only (ROX - Read Only Many)
  - The volume can be mounted read-only by many nodes

> :point_right: Need to provide shared access if you want multiple applications to be able to write to it (e.g FTP Server)

---

Please watch this short series of videos for further information

- [Intro to Persistent Volume Claims](https://www.youtube.com/watch?v=VB7vI9OT-WQ)
- [Understanding Persistent Volume and Persistent Volume Claim](https://www.youtube.com/watch?v=OulmwTYTauI&t=)
- [How Things Connect](https://www.youtube.com/watch?v=X6Vkz-ny574)

---

Continue to [Lesson 3.4](./lesson3.4.md)