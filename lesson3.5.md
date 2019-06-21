# Lesson 3, Advanced Topics

## Application Logging

If you wish to write application log files, you can still do so in Openshift. Depending on your application, this may require further editing of your application and Dockerfile. 

### Configuring Application to Write Logs

For this exercise, we will continue using the Springboot application and making some modifications to it. We will use the knowledge you applied to creating a persistent volume claim to writing application logs to a file. We will use ConfigMaps and program arguments for our sample application. 

#### Config Maps

The ConfigMap object provides mechanisms to inject containers with configuration data. A ConfigMap can be used to store information like individual properties or information like entire configuration files or JSON blobs.

The ConfigMap API object holds key-value pairs of configuration data that can be consumed in pods or used to store configuration data for system components such as controllers. ConfigMap is similar to secrets, but designed to more conveniently support working with strings that do not contain sensitive information.

### Exercise

#### Editing Files

1. First, let's create a new application.properties file. Your application.properties file for the Springboot sample sits at `springboot\src\main\resources\application.properties`. Duplicate this file and re-name it `application-prod.properties`. 

2. Add the following line at the end of your `application-prod.properties` file: 

```
logging.config=file:/opt/configuration/logback.xml
```

This location defined here is not local - it will be the location within the container defined by our ConfigMap. This is the reason it is applied in a different file from our application.properties file - our gradle build will fail if it tries to access this location which does not exist locally. 

3. In the same resources directory, create a new file called `logback.xml`. Copy/Paste the following XML configuration to that file and save it. 

```xml
<configuration scan="true" scanPeriod="30 seconds">
    <property name="fileName" value="/var/lib/new/app.log" />
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
      <encoder>
         <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
      </encoder>
    </appender>
    <appender name="FILE-ROLLING" class="ch.qos.logback.core.rolling.RollingFileAppender">
      <file> ${fileName} </file>
      <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
        <fileNamePattern>/var/lib/new/archived/app.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
        <maxFileSize>1MB</maxFileSize>
        <totalSizeCap>20GB</totalSizeCap>
        <maxHistory>60</maxHistory>
      </rollingPolicy>
      <encoder>
         <pattern>%d{yyyy-MM-dd} | %d{HH:mm:ss} | %-20.20thread | %5p | %-25.25logger{25} | %m%n</pattern>
         <charset>utf8</charset>
      </encoder>
   </appender>
   <root level="info">
      <appender-ref ref="FILE-ROLLING"/>
      <appender-ref ref="STDOUT"/>
   </root>
</configuration>
```

This XML formats our logs and provides a root level of info for the logs to be provided. You will notice that these logs write files to the location `/var/lib/new/` - which is the same file storage we created in [Lesson 3.3](./lesson3.3.md). 

4. Open the Dockerfile located at `springboot\image\Dockerfile`. Replace the last line, the `ENTRYPOINT` command, to the following: 

```dockerfile
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-Dspring.config.location=file:/opt/properties/application-prod.properties","-jar","devenablement-service-helloworld.jar"]
```

This change adds another command line argument, `-Dspring.config.location` with the location for where we will store the `application-prod.properties` file in our container. 

5. Open the deployment.yaml file located at `springboot\manifest\deployment.yaml`. Where you had previously uncommented the sections related to the PersistentVolumeClaim, we will now add volume configurations for our ConfigMaps. This section begins at line 124. 

```yaml
        volumeMounts:                       
        - name: "volume-claim"       
          mountPath: "/var/lib/new"        
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

Looking at the yaml file above, we see our previous `volumes` and `volumeMounts` definitions that we used to create our persistent volume claim. We will now create two new `volumes` - `config-volume` and `properties-volume`, which will hold our logback.xml and application-prod.properties files respectively. The sections marked with the "#<---New line" comment are for you to add, giving you some exposure to writing and properly formatting yaml files.

6. Now, we need to repeat our previous steps in building our Docker image and push/pull the image from the registry. If you used the local docker registry to push your image, you will need to push it to your local registry again. If you pushed to Quay last time, follow the instructions that follow to change your image. 

```bash
[vagrant@m1 ~]$ /home/vagrant/containers/springboot/image/build.sh
```

7. After our image is built, login to the console using the `oc` CLI. 

```bash
[vagrant@m1 ~]$ oc login https://api.oc.local:8443
Username: admin
Password: sandbox
Login successful.
```

8. If your project does not already exist, create it. 
```bash
[vagrant@m1 ~]$ oc new-project springboot-hello-world
```

9. Push the image to your local docker registry or to Quay. 

```bash
#Pushing your image to the local registry
[vagrant@m1 ~]$ sudo podman push \
                  springboot-hello-world:0.0.1 \
                  docker-daemon:registry.ford.com/devenablement/workshop:0.0.1
```

```bash
# Pushing the container to Quay
# You will be given the credentials of the robot account to login in class
[vagrant@m1 ~]$ sudo podman login registry.ford.com
Username:
Password:
Login Succeeded!

# Pushing your image to Quay and deploy your secret
[vagrant@m1 ~]$ sudo podman push \
                    springboot-hello-world:0.0.1 \
                    registry.ford.com/devenablement/workshop:YOUR_VERSION_NUMBER

[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/pullsecret.yaml
secret/devenablement-workshop-pull-secret created
```

If you push your image to Quay, ensure that `YOUR_VERSION_NUMBER` matches the version number in your `deployment.yaml` file. 

10. We will now create our ConfigMaps for our two files. 

```bash
[vagrant@m1 ~]$ oc create configmap logconfig \
      --from-file=/home/vagrant/containers/springboot/src/main/resources/logback.xml
configmap/logconfig created

[vagrant@m1 ~]$ oc create configmap app-properties \
      --from-file=/home/vagrant/containers/springboot/src/main/resources/application-prod.properties
configmap/app-properties created
```

As you can see, the names we gave the config maps are the names that we defined in the `deployment.yaml` for the configMap. 

11. After creating our configMaps, we can deploy the rest of our application. 

```bash
oc create -f /home/vagrant/containers/springboot/manifest/deployment.yaml
```

12. After running the `deployment.yaml` file, we can go to the terminal of a running pod as we did in [Lesson 3.3](./lesson3.3.md). Navigate to this drive and view your application's running logs. 

```bash
sh-4.2$ ls /var/lib/new
app.log
sh-4.2$ cat /var/lib/new/app.log
```

13. To confirm that your application logs will persist, in the Openshift console, delete your pod. After deleting your pod, wait for the new one to start up and repeat step 12. You should see your new container's application logs appended to the previously written logs. 

#### Saving Logs Locally

Having the logs in the container is one thing, but it is difficult to view them simply by using the `cat` command. We might want to store these logs if we cannot access them directly at all times. 

14. Return to your terminal and run the following commands to create a directory for the logs. 

```bash
[vagrant@m1 ~]$ cd /home/vagrant/containers/springboot
[vagrant@m1 ~]$ mkdir logs
```

15. We will now use the `rsync` command to copy the directory of files locally. 

> NOTE: You must have admin rights on your namespace to execute these commands. You are an admin in localdev, but in the production version of Openshift, admin rights will likely reside with LL6+

```bash
[vagrant@m1 ~]$ oc rsync $(oc get pods | grep 'springboot-hello-world' | head -1 | awk '{print $1}'):/var/lib/new ./
```

Let's break down this command: 

- **oc rsync** - oc cli command to copy contents from a container directory to a local directory, or vice versa
- **$(oc get pods | grep 'springboot-hello-world' | head -1 | awk '{print $1}'):/var/lib/new** - A piped command that consists of a few parts
    - **oc get pods** - Returns a list of all the pods in the project you are currently working on
    - **grep 'springboot-hello-world'** - Filters the list of pods that contain the name `springboot-hello-world`
    - **head -1** - Returns the first result of the filter
    - **awk '{print $1}'** - Returns the first bit of information - which in this case - is the pod name
- **:/var/lib/new** - The directory within the container that is mounted to our persistent volume claim where we are writing the app logs
- **./** - The local directory, which here, is the current working directory (`/containers/springboot`)

After we run this command, we can go into our springboot directory and see that we have a new folder called `new` which contains all of the contents we had within the container. 

16. Delete your app configurations and your persistent volume claim. 
```bash
# Only run the exit command if you are `rsh` into the pod
[vagrant@m1 ~]$ oc delete all -l app=springboot-hello-world
[vagrant@m1 ~]$ oc delete pvc my-manifest-claim
```

---

You have reached the end of the workshop :clap: