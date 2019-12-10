## Openshift Console and CLI

Before we build our container image and deploy the application, we will interact with the Openshift console and use the `oc` CLI. In this class, we will be interacting with the production cluster of Openshift. You will be granted access to a namespace to run your application in the production cluster. 

At the moment, there is only a single, production cluster of CaaS. This is different from PCF, which has separate "clusters" (referred to as foundations in PCF) for pre-prod and prod and different "clusters" for the different data centers. To have separate environments in CaaS, you will have a separate namespace for each environment. For example, you could have 3 separate namespaces, `dev`, `qa`, and `prod`, for your single application.  

In Openshift, `project` and `namespace` are used interchangeably. It is a logicial construct where you deploy your Openshift objects. Your application instances/replicas may span different nodes and data centers, but you can manage them all within your single namespace. 

---

### Download OC CLI

To deploy objects into Openshift, you will need the `oc` CLI. 

1. Go to https://files.caas.ford.com:9443/oc-cli/latest/ and click on the proper download for your operating system.

1. Extract the contents of the zip/tar. If you are on Windows, the contents will be `oc.exe` and on Mac it will be the `oc` file. 

1. Add the path to the `oc` binary to your system's path.
    - Windows:
         - **Option 1**
            - Copy the `oc.exe` file into your `System32` directory (C:\Windows\System32)
         - **Option 2**
            - Move the `oc.exe` to a more permanent location outside of your `Downloads` folder
                - Example: `C:\Users\<CDSID>`
            - Copy the path you chose to save the `oc.exe` file
            - Open up your system environment variables by typing `path` into the windows search and click `Environment Variables` 
            - Add the path to the `oc.exe` to the system variable's `PATH` (see the image below)
        - **Option 3** - If you do not have admin rights on your machine, move the `oc.exe` to one of the locations already listed in path (e.g. follow the Mac instructions)
    - Mac:
        - Open up a terminal
        - Type `echo $PATH`
        - Choose one of paths that was printed and move the `oc` file in that location
        - Restart the terminal

- Windows Path Example
<p align="center">
    <img src="../images/oc_cli.PNG" width="825" height="400">
</p>

### Openshift Console

1. Go to https://api.caas.ford.com
2. Login with your CDSID and password
3. Confirm you see the `devenablement-workshop-dev` namespace on the far right side of the webpage. 

### Terminal Login

1. Open git bash, the command line, or powershell. 
2. Enter the following command and provide your CDSID and password when prompted. 

```bash
# If using git bash
$ winpty oc login api.caas.ford.com

# If using terminal/powershell
$ oc login api.caas.ford.com
```

3. Confirm your project selection with the following commands. 

```bash
$ oc project
Using project "devenablement-workshop-dev" on server "https://api.caas.ford.com:443".
```

If you are defaulted to a different project, run the command below to select the `devenablement-workshop-dev` namespace. 

```bash
$ oc project devenablement-workshop-dev
Now using project "devenablement-workshop-dev" on server "https://api.caas.ford.com:443".
```

## Requesting a Namespace

As mentioned previously, this is a namespace used only for this workshop. The workshop will be wiped clean in preparation for the next workshop and your credentials will be removed from accessing this namespace at the end of the workshop. To procure your own namespace, visit the [Ford Cloud Portal](https://www.cloudportal.ford.com/openshift). A free-trial version exists where you can receive a namespace for 120 days.

---  

Continue to [container build tools](./6-buildtools.md).

Return to [Table of Contents](../README.md#agenda)
