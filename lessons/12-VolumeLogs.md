## Application Logging

If you wish, you can also write your application logs to a PVC. We need to make some changes to our Dockerfile (and by extension, our Container Image) since our Springboot application needs some configurations made to work. 

### Configuring Application to Write Logs

For this exercise, we will continue using the Springboot application and making some modifications to it. We will use the knowledge you applied to creating a persistent volume claim to writing application logs to a file. We will use ConfigMaps and program arguments for our sample application. 

#### Config Maps

ConfigMaps are how we store non-sensitive configurations in the environment. If you are not familiar with the [12-factor app](https://12factor.net/), a best-practices for applications to be portable and resilient, storing configurations in the environment and NOT in code is a key component. 

The ConfigMap object provides mechanisms to inject containers with configuration data. A ConfigMap can be used to store information like individual properties or information like entire configuration files or JSON blobs.

The ConfigMap API object holds key-value pairs of configuration data that can be consumed in pods or used to store configuration data for system components such as controllers. ConfigMap is similar to secrets, but designed to more conveniently support working with strings that do not contain sensitive information.

### Exercise

#### Editing Files

1. Let's view the files that we will be using to configure our springboot application to write logs to a PVC. In `springboot\configs` are two files that we will use: `application.properties` and `logback.xml`. The `logback.xml` file is a simple log configuration file and the new `application.properties` we will use is the same as the existing `application.properties` with one small change. Let's review the important content and configuration related to Openshift and our containers. 

**Logback.xml**
```xml
<property name="fileName" value="/var/lib/mystorage/app.log" />
```
**application.properties**
```
logging.config=file:/opt/configuration/logback.xml
```

Notice that the `logback.xml` is referencing a directory location of `/var/lib/mystorage/`. This is the directory we defined in our volume mount section for our PVC. We will now use this drive to write our application logs and have them persist. 

The `application.properties` file tells our application to use the `logback.xml` file for logging. It says the drive where the `logback.xml` file exists is in `/opt/configuration`. This location does not currently exist, but we will create it. 

2. We need a way to inject our application properties at runtime, which means re-defining our Dockerfile and image. Open the Dockerfile located at `springboot\image\Dockerfile`. Comment line 26 of the Dockerfile and uncomment line 27. Line 27 is shown below. 

```dockerfile
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-Dspring.config.location=file:/opt/properties/application.properties","-jar","devenablement-service-helloworld.jar"]
```

This change adds another java command line argument, `-Dspring.config.location`. It says to use the `application.properties` file located at `/opt/properties`. Once again, that location does not exist yet, but we will create it. '

The important thing to note is the benefit of separating your application properties and configuration from your actual application. You can now edit your properties independently of your application. Any change you make to your properties file will no longer need a re-build of your image. 

3. Since we changed our Dockerfile, we need to build our image again. 

```bash
[vagrant@m1 ~]$ /home/vagrant/containers/springboot/image/build.sh
```

4. Since we rebuilt our image, we need to push it to Quay or the local docker daemon again. Use a different version number than the one you previously used. 

```bash
# Pushing your image to Quay
[vagrant@m1 ~]$ sudo podman push \
                    springboot-hello-world:0.0.1 \
                    registry.ford.com/devenablement/workshop:YOUR_VERSION_NUMBER
```


5. Open the `deployment-3.yaml` file located at `springboot\manifest\deployment-3.yaml`. Change line 59 to reference your new version number. 

```yaml
image: registry.ford.com/devenablement/workshop:0.0.1 #<---Your Tag Here
```

6. Let's review the additions to this deployment seen in lines 124-140. 
```yaml
        volumeMounts:                       
        - name: "volume-claim"       
          mountPath: "/var/lib/mystorage"        
        - name: "config-volume"           #<---New line
          mountPath: "/opt/configuration" #<---New line
        - name: "properties-volume"       #<---New line
          mountPath: "/opt/properties"    #<---New line
      volumes:
      - name: "volume-claim"
        persistentVolumeClaim:
          claimName: "my-manifest-claim"
      - name: "config-volume"             #<---New line
        configMap:                        #<---New line
          name: logconfig                 #<---New line
      - name: "properties-volume"         #<---New line
        configMap:                        #<---New line
          name: "app-properties"          #<---New line
```

Looking at the yaml file above, we see our previous `volumes` and `volumeMounts` definitions that we used to create our persistent volume claim. We will now create two new `volumes` - `config-volume` and `properties-volume`, which will hold our `logback.xml` and `application.properties` files respectively. 

You will notice the `/opt/properties` location for our `application.properties` file is what we put in our Dockerfile. The `/opt/configuration` location for our `logback.xml` file is what we put in the `application.properties` file. 

7. In order to use these configMaps, we need to deploy them to our namespace. Run the two commands to deploy the `logback.xml` and the `application.properties` file to your namespace. 

```bash
[vagrant@m1 ~]$ oc create configmap logconfig \
      --from-file=/home/vagrant/containers/springboot/configs/logback.xml
configmap/logconfig created

[vagrant@m1 ~]$ oc create configmap app-properties \
      --from-file=/home/vagrant/containers/springboot/configs/application.properties
configmap/app-properties created
```

As you can see, the names we gave the config maps are the names that we defined in the `deployment-3.yaml` for the configMaps. 

8. After creating our configMaps, we can deploy the rest of our application. 

```bash
oc create -f /home/vagrant/containers/springboot/manifest/deployment-3.yaml
```

9. After running the `deployment-3.yaml` file, we can go to the terminal of a running pod as we did in the previous lesson. Navigate to this drive and view your application's running logs. 

```bash
sh-4.2$ ls /var/lib/mystorage
app.log
sh-4.2$ cat /var/lib/mystorage/app.log
```

11. To confirm that your application logs will persist, in the Openshift console, delete your pod. After deleting your pod, wait for the new one to start up and repeat step 12. You should see your new container's application logs appended to the previously written logs. 

#### Saving Logs Locally

Having the logs in the container is one thing, but it is difficult to view them simply by using the `cat` command. We might want to store these logs if we cannot access them directly at all times. 

12. Return to your terminal and run the following commands to create a directory for the logs. 

```bash
[vagrant@m1 ~]$ cd /home/vagrant/containers/springboot
[vagrant@m1 springboot]$ mkdir logs
```

13. We will now use the `rsync` command to copy the directory of files locally. We need 3 things: a pod, the location where the logs are being written, and the location we want to store those logs. 

> NOTE: You must have admin rights on your namespace to execute these commands. You are an admin in localdev, but in the production version of Openshift, admin rights will likely reside with LL6+ or senior developers. 

```bash

[vagrant@m1 springboot]$ oc get pods
NAME                                      READY     STATUS    RESTARTS   AGE
springboot-hello-world-56d59b9669-r66qq   1/1       Running   0          2m

# Use your podname above in the next command
[vagrant@m1 springboot]$ oc rsync <POD NAME>:/var/lib/mystorage ./logs
receiving incremental file list
mystorage/
mystorage/app.log

sent 47 bytes  received 12,718 bytes  8,510.00 bytes/sec
total size is 12,587  speedup is 0.99
```

After we run this command, we can go into our `springboot/logs` directory and see that we have a new folder called `mystorage` which contains all of the contents we had within the same directory in the container. 

<!--
```bash
[vagrant@m1 ~]$ oc rsync $(oc get pods | grep 'springboot-hello-world' | head -1 | awk '{print $1}'):/var/lib/mystorage ./logs
```

Let's break down this command: 

- **oc rsync** - oc cli command to copy contents from a container directory to a local directory, or vice versa
- **$(oc get pods | grep 'springboot-hello-world' | head -1 | awk '{print $1}'):/var/lib/new** - A piped command that consists of a few parts
    - **oc get pods** - Returns a list of all the pods in the project you are currently working on
    - **grep 'springboot-hello-world'** - Filters the list of pods that contain the name `springboot-hello-world`
    - **head -1** - Returns the first result of the filter
    - **awk '{print $1}'** - Returns the first bit of information - which in this case - is the pod name
- **:/var/lib/mystorage** - The directory within the container that is mounted to our persistent volume claim where we are writing the app logs
- **./logs** - The directory we want to copy our logs to 
-->

14. Let's clean up our environment. Delete your app configurations and your persistent volume claim. 
```bash
# Only run the exit command if you are `rsh` into the pod
[vagrant@m1 ~]$ oc delete -f /home/vagrant/containers/springboot/manifest/deployment-3.yaml
[vagrant@m1 ~]$ oc delete pvc my-storage-claim
```

---

Continue to [Kibana](./13-Kibana.md)

Return to [Table of Contents](../README.md#agenda)