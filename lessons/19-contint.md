# Continuous Integration 

There are a number of ways to employ continuous integration, namely through Github and Jenkins. In this lesson we will just simply go over how to employ continuous integration through GitHub in your `BuildConfig` by looking at a sample `BuildConfig`. 

## Sample BuildConfig

Open `build-config-git-sample.yaml` so the integration of Github can be reviewed. 

### Source

```yaml
  source:
    contextDir: /image
    git:
      uri: 'git@github.ford.com:MALYASS/auto-build.git'
    sourceSecret:
      name: github-repo
    type: Git
```

In this section, we define a few different parameters:

- contextDir: This is the path within the Github repository to our `Dockerfile`
- sourceSecret: This secret contains the private SSH key saved to Openshift as a secret. The public key is saved in Github with the repo as a `Deploy Key`. 
- uri: This is the SSH uri to the Github repo

### Triggers 

```yaml
  triggers:
    - github:
        secretReference:
          name: githooksecret
      type: GitHub
```

In this section, we create a webhook trigger on Github. There are 3 parts to creating this webhook: 

1. Add the webhook to your repository in Github
2. Add the secret for the webhook to Openshift
3. Reference the webhook secret as a trigger in your yaml. 

To get the webhook URL you need to use on a `BuildConfig`, we can use the `describe` functionality of the `oc` CLI. 

#### Exercise

Run the following command to get details on your `BuildConfig`

```bash
$ oc describe bc/app-build-<CDSID>
```

The output provided gives all the details saved in Openshift about your build config. It also provides a `Webhook Github URL`, which looks similar to this: 

```
https://api.caas.ford.com:443/apis/build.openshift.io/v1/namespaces/devenablement-workshop-dev/buildconfigs/app-build-malyass/webhooks/<secret>/github
```

In Github, you would copy and paste this URL as the webhook payload. You would then replace `<secret>` with a password of some kind. That password gets stored as an Openshift secret, which is then referenced in the yaml. In this example, `githooksecret` contains the password for this payload. 

---

Return to [Table of Contents](../README.md#agenda)
