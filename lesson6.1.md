## Day 2 - Lesson 6

## Vanity URLs and TLS Certificates

### Flowcharts & Diagrams 

- Review the [CaaS Engineering DNS Overview](https://github.ford.com/Containers/k8s-platform/blob/519eb82d7ece0e161bd3e017dc872cba6c124fdc/Day2/CaaS_Applications/User_docs/FAQ-Guide.md#overview--flow-chart)
![Route and Service Diagram](https://github.ford.com/DevEnablement/caas-workshop/blob/master/images/RouteServiceDiagram.PNG)
This lesson is a "hands-off" exercise in which we detail the necessary steps to set up and configure your vanity URL for your application with passthrough TLS termination. 

### Vanity URL Instructions

The CaaS platform provides the subdomain `*.app.caas.ford.com` that can be used to build a unique URL for an app. This will satisfy many uses; however, if the app is customer-facing, app teams may desire a [vanity URL](https://en.wikipedia.org/wiki/Vanity_domain).

At a high-level, to establish a new vanity URL, an app team will need to:
1. Create a request for Ford's DNS team to create a DNS CNAME alias using your vanity URL.
   - This alias should forward traffic to `caas.app.ford.com`.
   - You will also need to specify if this vanity URL should be exposed to the public internet (aka external-facing).
1. Create an OpenShift route object which refers to your vanity URL.
1. Create a request for a TLS certificate associated with your vanity URL.
1. Configure your app to serve the TLS certificate to clients requesting the vanity URL.

#### Request DNS

To submit a request to the DNS team:
1. For the purposes of this class, please DO NOT click submit, but let's take a look at the DNS request form and how to fill it out.
1. Open the [Network Operations DNS Tool](https://tools.netops.ford.com/dns).
1. Click Create (look for the giant Gear Icon).
1. Set Environment accordingly. Typically, this would be set to "Hosting/Servers".
1. Set Category=Alias.
1. Set Location. If you need the vanity URL external-facing, set Location=External DNS. If you need the vanity URL internal-facing, set location=Internal DNS. If you need both, submit one DNS request for each resulting in a total of two requests.
1. Set Hostname=`caas.app.ford.com`. This is where traffic destined for the vanity URL will be forwarded (the CaaS platform).
1. Set Alias=`<YOUR_VANITY_URL>`. For example, `www.caas-workshop.ford.com`.
1. Complete the remainder of the form. DO NOT click submit for this class, but if you were actually going to submit a real DNS request, you would click submit.

Here is an example DNS request for internal-facing vanity URL.

![DNS Request Screenshot](images/dns1.png)

If approved, the DNS team will configure this vanity URL on Ford's DNS servers. This means traffic destined for the vanity URL will be forwarded to the CaaS platform. The next steps are related to configuring TLS security for the app using the vanity URL. The app team must create a TLS certificate associated with the vanity URL and configure their app to serve this certificate.

#### Sign Certificate

Create a signing request for a TLS certificate associated with your vanity URL.
1. Create a new Certificate Signing Request (CSR) on your workstation.
   - View help guides [here](https://www.certman.ford.com/SSL/csrhelp.aspx) and [here](https://www.godaddy.com/help/apache-generate-csr-certificate-signing-request-5269)

The example below shoes a CSR and key generation done using OPENSSL for the creation of the domain: caas-workshop.ford.com

```bash
$ openssl req -new -newkey rsa:2048 -nodes -keyout caas-workshop.key -out caas-workshop.csr
Generating a RSA private key
.........................................+++++
................................................+++++
writing new private key to 'caas-workshop.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:Michigan
Locality Name (eg, city) []:Dearborn
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Ford Motor Company
Organizational Unit Name (eg, section) []:IT
Common Name (e.g. server FQDN or YOUR name) []:caas-workshop.ford.com
Email Address []:<YOUR-EMAIL-HERE>

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

An LL6+ will then use the .key and .csr files to complete steps 2-4

2. Open the [Certman Tool](https://www.certman.ford.com/SSL/).
3. Click New SSL Certificate.
4. Complete the form and submit the request.
   - Use your vanity URL in the Subject Alternative Names (SANs) field. You can associate multiple URLs with the certificate. For example, `www.caas-workshop.ford.com`, `wwwqa.caas-workshop.ford.com`, and `wwwdev.caas-workshop.ford.com`.
   - Enter the CSR you created in the earlier step.

If you are new to TLS certificates, or new to certs at Ford, the Certman [FAQ](https://www.certman.ford.com/SSL/faq.aspx) is pretty good. And the [OpenSSL Cookbook](https://www.feistyduck.com/library/openssl-cookbook/online/) is free online.

#### Deploy Secrets
Now that you have your key and certificate, you will need to deploy them to your namespace as a secret. You can do this as a tls secret or you can create a keystore file and deploy that as a generic secret. 

- For some apps that do not need extra configuration, you might simply deploy your key and cert as a TLS secret
```bash
$ oc create secret tls MY_SECRET_NAME --key /PATH_TO_KEY_FILE.key --cert /PATH_TO_CERT_FILE.crt -n MY_NAMESPACE
```
Example: 
```bash
$ oc create secret tls caas-workshop-secret --key /keys/caas-workshop.key --cert /keys/caas-workshop.crt -n devenablement-dev
``` 

- For other applications, like a Java/Springboot application, you might need to create a keystore and deploy that to your namespace as a generic secret
```bash
$ openssl pkcs12 -export -in caas-workshop.ford.com.crt -inkey caas-workshop.key -out caas-workshop.p12 -name caas-workshop.ford.com
Enter Export Password:
Verifying - Enter Export Password:
$ oc create secret generic workshop-keystore --from-file=keystore.p12=caas-workshop.p12
```

#### Edit Manifest

To enable HTTPS with passthrough termination, there are number of edits you must make to your manifest file. Depending on the type of application of you have, this will involve targeting specific ports and importing your key/cert/keystore as a volume. This involves changing the following Openshift Objects:

- Deployment
  - Add container port for HTTPS
  ```yaml
  ports:
  - name: https
    containerPort: 8443
  ```
  - Change liveness/readiness probe port and scheme
  ```yaml
  livenessProbe:
    httpGet:
      path: <PATH_TO_PROBE>
      port: 8443
      scheme: HTTPS
    timeoutSeconds: 5
  readinessProbe:
    httpGet:
      path: <PATH_TO_PROBE>
      port: 8443
      scheme: HTTPS
  ```
  - Mount your secret and configMap, if any
    - **Secret** - This will either be your TLS secret that contains your key/cert or your generic secret that contains your keystore
    - **ConfigMap** - Way to inject your application properties at the creation of the container
    ```yaml
        volumeMounts:
          - name: keystore-volume
            mountPath: "/etc/keystore"
          - name: "properties-volume"
            mountPath: "/opt/properties"
      volumes:
      - name: keystore-volume
        secret:
          secretName: workshop-keystore
      - name: "properties-volume"
        configMap:
          name: "app-properties"
    ```
- Service
  - Define port and name for HTTPS
  ```yaml
    ports:
    - protocol: TCP
      name: https
      port: 8443
      targetPort: 8443
  ```
- Route
  - Change termination to `passthrough` and the targetport and add your vanity URL
  ```yaml
  spec:
    host: springboot-hello-world.app.caas.ford.com
    host: www.caas-workshop.ford.com
  port:
    targetPort: 8443
  tls:
    termination: passthrough
    insecureEdgeTerminationPolicy: Redirect
  ```
- Secret
  - Ensure your secret for your TLS key/cert or your keystore has been created (as shown in the previous step)
- ConfigMap
  - If needed - define a ConfigMap to inject the properties of your application in the container. 
  
  Example - The following lines were added to application.properties that are injected at runtime for the container to allow the container to access the keystore. 
  ```
  server.port=8443
  server.ssl.key-store-password=workshop
  server.ssl.key-store=file:/etc/keystore/keystore.p12
  ```

Go to the [Springboot Passthrough Deployment Sample]() to see a sample Springboot application deployment.yaml with these configurations changed to enable passthrough termination. 

#### Apply Changes

Once you have finished all your changes to your manifest file(s), you will need to apply your changes for them to take affect. 

```bash
oc apply -f /home/vagrant/containers/springboot/manifest/deployment.yaml
```

Now when traffic destined for `www.caas-workshop.ford.com` arrives at the CaaS platform, it will be forwarded to the `springboot-hello-world` app. This concludes the steps necessary to route traffic to the app.

#### Other Dependencies

Now you need to configure your app to serve the TLS certificate that you created. This is unique depending on your development language. With java, you will likely be creating a JKS keystore and placing it in your project's `resources` folder.

Here are some java examples on the web.
- [How to enable HTTPS in a Spring Boot Java application](https://www.thomasvitale.com/https-spring-boot-ssl-certificate/)
- [Spring Boot SSL HTTPS Example](https://howtodoinjava.com/spring-boot/spring-boot-ssl-https-example/)

<!--
#### HTTP

If you need your application to be accessible over HTTP and HTTPS, you define the same information shown above for HTTPS and HTTP. For example, you would define the ports in your service as such: 

  ```yaml
    ports:
    - protocol: TCP
      name: https
      port: 8443
      targetPort: 8443
    - protocol: TCP
      name: http
      port: 8080
      targetport: 8080
  ```
-->
<!---
### Storage
  - Persistent storage options, TBD
  
### Jenkins Usage
TBD

CaaS onboarding https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#application-namespace-on-boarding
CaaS billing modelhttps://github.ford.com/Containers/k8s-platform/blob/master/Service-Management/CaaS-Operations.md#billing-model
CaaS service model – Support/Incident https://github.ford.com/Containers/k8s-platform/blob/master/Service-Management/CaaS-Operations.md#incidents
Container registry onboarding https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/CaaS_Platform_Onboarding.md#quay-on-boarding
Container registry robot accounts https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/FAQ-Guide.md#quay-robot-account-process
How to submit request for Application Mail relay registration in CaaS https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/FAQ-Guide.md#how-to-submit-request-for-application-mail-relay-registration-in-caas
How create vanity url's https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/FAQ-Guide.md#how-to-enroll-or-create-custom-routevanity-url-in-openshift-platform-for-production
How to expose applications externally https://github.ford.com/Containers/k8s-platform/blob/master/Day2/CaaS_Applications/User_docs/FAQ-Guide.md#how-to-enroll-or-create-custom-routevanity-url-in-openshift-platform-for-production

RedHat Developer Account http://developers.redhat.com/register
https://medium.com/@sbose78/running-keycloak-on-openshift-3-8d195c0daaf6 
http://blog.keycloak.org/2018/05/keycloak-on-openshift.html


-->

---

You have reached the end of the workshop :clap:

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop/tree/workshop-reformat#agenda)