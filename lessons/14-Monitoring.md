### Monitoring Apps

### Production Monitoring 

If your app is deployed on CaaS, you get basic monitoring of your app's resource utilization by default. The platform will provide a real-time monitoring dashboard built using SysDig, which is still in a POC stage. 

If you need more app performance monitoring capabilities than the basic monitoring provided by the platform, you can connect your app to Ford's Dynatrace instance for a cost. You can sign up on the [Dynatrace team website](https://it1.spt.ford.com/sites/L1POE/Public/SitePages/Dynatrace.aspx).

### SysDig

SysDig is a monitoring tool that will allow for basic monitoring and alerting. The following is a list of some features and monitoring it provides: 

- Minor application process monitoring 
- Container level monitoring 
- Pod level monitoring 
- Compilation of all events 
- Ability to create alerts on any metric and event 
- File System usage

The tool is still in the POC stage and will be available in production in Q4. 

### Dynatrace

Dynatrace is available in production - but not on a system wide level. It will be the application team's responsibility to add the Dynatrace agent to the team's Dockerfile. However, the additions are relatively simple add-ons to any existing Dockerfile. When the final implementation is decided on by the Dynatrace team, this configuration will be made public for app teams to use. 

<!--
> NOTE: This implementation is subject to change 

#### Dockerfile Changes

Open Dockerfile-2 located in `springboot/image` for your own reference. We will review the additions that you can simply add to your Dockerfiles to include a Dyntrace agent in your containers. 

```Dockerfile
FROM registry.redhat.io/rhscl/python-27-rhel7 AS builder
ARG DT_API_URL="https://wwwqa.dynatrace.ford.com/e/114d327e-ea9d-46cc-92d3-3967eaedacde/api/"
ARG DT_API_TOKEN="YOUR_TOKEN_HERE"
ARG DT_ONEAGENT_OPTIONS="flavor=default&include=java"
ENV DT_HOME="/opt/dynatrace/oneagent"
USER root
RUN mkdir -p "$DT_HOME" && \
    wget --no-check-certificate -O "$DT_HOME/oneagent.zip" "$DT_API_URL/v1/deployment/installer/agent/unix/paas/latest?Api-Token=$DT_API_TOKEN&$DT_ONEAGENT_OPTIONS" && \
    unzip -d "$DT_HOME" "$DT_HOME/oneagent.zip" && \
    rm "$DT_HOME/oneagent.zip"
```

The first part of the Dockerfile sets arguments and environment variables for the Dynatrace URL, token, options, and home directory. The `RUN` step uses all these variables to make a directory in which to play the Dynatrace agent and unzip it. 

The rest of the Dockerfile is the Dockerfile is nearly the same as our previous Dockerfile, with another `FROM` statement. This is known as a [multi-stage build](https://docs.docker.com/develop/develop-images/multistage-build/). Each `FROM` statement can use a different base. Below is the rest of the Dockerfile. 

```Dockerfile
FROM registry.redhat.io/redhat-openjdk-18/openjdk18-openshift
EXPOSE 8080
COPY --from=builder /opt/dynatrace/oneagent /opt/dynatrace/oneagent #<--New Line
RUN sh /opt/dynatrace/oneagent/dynatrace-agent64.sh                 #<--New Line
ARG JAR_FILE=../build/libs/devenablement-service-helloworld.jar     
ADD ${JAR_FILE} devenablement-service-helloworld.jar
USER root                                                           #<--New Line
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","devenablement-service-helloworld.jar"]
```

In the second stage of our multi-stage build, we have most of the same Dockerfile as we did previously. There are 3 changes to include Dynatrace. 

These additions to your Dockerfile will enable your pods to send data to Dynatrace. 
-->
---

Continue to [Vanity URLs](./15-VanityUrl.md)

Return to [Table of Contents](../README.md#agenda)