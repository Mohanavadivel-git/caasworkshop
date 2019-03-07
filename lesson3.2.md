# Lesson 3, Advanced Topics

### Vanity URLs and TLS Certificates

The CaaS platform provides the subdomain `*.app.caas.ford.com` that can be used to build a unique URL for an app. This will satisfy many uses; however, if the app is customer-facing, app teams may desire a [vanity URL](https://en.wikipedia.org/wiki/Vanity_domain).

At a high-level, to establish a new vanity URL, an app team will need to:
1. Create a request for Ford's DNS team to create a DNS CNAME alias using your vanity URL.
   - This alias should forward traffic to `caas.app.ford.com`.
   - You will also need to specify if this vanity URL should be exposed to the public internet (aka external-facing).
1. Create an OpenShift route object which refers to your vanity URL.
1. Create a request for a TLS certificate associated with your vanity URL.
1. Configure your app to serve the TLS certificate to clients requesting the vanity URL.

#### Exercise

To submit a request to the DNS team:
1. For the purposes of this class, please DO NOT click submit, but let's take a look at the DNS request form and how to fill it out.
1. Open the [Network Operations DNS Tool](https://tools.netops.ford.com/dns).
1. Click Create (look for the giant Gear Icon).
1. Set Environment accordingly. Typically, this would be set to "Hosting/Servers".
1. Set Category=Alias.
1. Set Location. If you need the vanity URL external-facing, set Location=External DNS. If you need the vanity URL internal-facing, set location=Internal DNS. If you need both, submit one DNS request for each resulting in a total of two requests.
1. Set Hostname=`caas.app.ford.com`. This is where traffic destined for the vanity URL will be forwarded (the CaaS platform).
1. Set Subnet or IP=`19.13.2.3` for internal-facing and `136.2.64.8` for external-facing.
1. Set Alias=`<YOUR_VANITY_URL>`. For example, `www.electrictrucks.ford.com`.
1. Complete the remainder of the form. DO NOT click submit for this class, but if you were actually going to submit a real DNS request, you would click submit.

Here is an example DNS request for internal-facing vanity URL.

![DNS Request Screenshot](images/dns1.png)

If approved, the DNS team will configure this vanity URL on Ford's DNS servers. This means traffic destined for the vanity URL will be forwarded to the CaaS platform. In the next exercise, we will add the vanity URL to an OpenShift route object so that the platform will be able to route the traffic appropriately.

#### Exercise

Create an OpenShift route object which includes your vanity URL.
1. Building on the sample app, open the `manifest/python.yaml` file for editing.
1. Add the vanity URL to the existing route object and save the file. See below.
1. Deploy the app to CaaS again.

```
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  labels:
    app: python
  name: python
spec:
  host: python.app.oc.local
  host: www.saffron.ford.com  <---------------- ADD THIS
  port:
    targetPort: 8080
  tls:
    termintaion: edge
    insecureEdgeTerminationPolicy: Redirect
```

Now when traffic destined for `www.saffron.ford.com` arrives at the CaaS platform, it will be forwarded to the `python` app. This concludes the steps necessary to route traffic to the app.

The next steps are related to configuring TLS security for the app using the vanity URL. The app team must create a TLS certificate associated with the vanity URL and configure their app to serve this certificate.

#### Exercise

Create a signing request for a TLS certificate associated with your vanity URL.
1. Create a new Certificate Signing Request (CSR) on your workstation.
   - If you don't know what this means, there is some help [here](https://www.certman.ford.com/SSL/csrhelp.aspx).
1. Open the [Certman Tool](https://www.certman.ford.com/SSL/).
1. Click New SSL Certificate.
1. Complete the form and submit the request.
   - Use your vanity URL in the Subject Alternative Names (SANs) field. You can associate multiple URLs with the certificate. For example, `www.saffron.ford.com`, `wwwqa.saffron.ford.com`, and `wwwdev.saffron.ford.com`.
   - Enter the CSR you created in the earlier step.

If you are new to TLS certificates, or new to certs at Ford, the Certman [FAQ](https://www.certman.ford.com/SSL/faq.aspx) is pretty good. And the [OpenSSL Cookbook](https://www.feistyduck.com/library/openssl-cookbook/online/) is free online.

#### Exercise

Now you need to configure your app to serve the TLS certificate that you created in the previous exercise. This is unique depending on your development language. With java, you will likely be creating a JKS keystore and placing it in your project's `resources` folder.

Here are some java examples on the web.
- [How to enable HTTPS in a Spring Boot Java application](https://www.thomasvitale.com/https-spring-boot-ssl-certificate/)
- [Spring Boot SSL HTTPS Example](https://howtodoinjava.com/spring-boot/spring-boot-ssl-https-example/)

<!---
### Storage
  - Persistent storage options, TBD
  
### Jenkins Usage
TBD
-->