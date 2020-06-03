# Cloning the Sample Application

For this workshop, we will use a sample application located within the `application` directory of this repository.

### Clone/Download Repository

1. Open a terminal and navigate to any workspace directory of your choosing.

```bash
cd ~/workspace
```

2. Clone the workshop repository. If you have the Github desktop application, you can use that to clone the repository.

```bash
git clone git@github.ford.com:DevEnablement/caas-workshop.git      # Using SSH
git clone https://github.ford.com/DevEnablement/caas-workshop.git  # Using HTTPS
```

**NOTE**: If you are unable to clone the repository, go to the [repository home page](https://github.ford.com/DevEnablement/caas-workshop) and click the green `Clone or download` button where you can download the `.ZIP` of the repository. Unzip the content in a directory of your choosing.

3. View the contents of the `application` directory:

    - **manifests**: This directory contains all the manifests that we will use to build and deploy this application to CaaS
    - **src**: Since this is a simple python application, the src sections contains the simple python code and the requirements listing the necessary python packages.
    - **Dockerfile**: This is the `Dockerfile` that will be used to build our container image

---

Continue to [Writing Dockerfiles](./04-dockerfiles.md).

Return to [Table of Contents](../README.md#agenda)
