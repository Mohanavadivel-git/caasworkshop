## Writing Dockerfiles

This lesson will go over Dockerfile basics and the process of writing a Dockerfile.

---

A Dockerfile is a text file that defines our container image. An image building tool (like docker, buildah, or podman) takes a Dockerfile as input and outputs a container image.

Before creating our container image, let's evaluate an example Dockerfile. This is the Dockerfile for our sample Python application. The Dockerfile for a real-world production application will likely be much more complex, so be sure to review this external [best practices article](https://takacsmark.com/dockerfile-tutorial-by-example-dockerfile-best-practices-2018/) for how to write good, slim Dockerfiles.

```dockerfile
FROM registry.redhat.io/rhscl/python-36-rhel7

ARG LD_LIBRARY_PATH=/opt/rh/python36/root/usr/lib64

ENV \
    HOME=/app \
    USER_UID=1001 \
    SUMMARY="A simple python web app"	\
    DESCRIPTION="A simple python web app to demonstrate basic container and kubernetes concepts." \
    NAME=World

WORKDIR $HOME

COPY ../src $HOME

RUN pip install --trusted-host pypi.python.org -r requirements.txt && \
    mkdir $HOME/logs

EXPOSE 8080

USER $USER_UID

CMD ["python", "app.py"]
```

The capitalized keywords at the beginning of each line above are Docker instructions. Here is a brief description of the instructions.

- **FROM** - Every Dockerfile must begin with a FROM statement that defines the base image to be built upon. You can view some example base images available for use at Ford in the [Redhat Container Catalog](https://access.redhat.com/containers/#/).
- **ARG** - Creates a variable that can be used within the Dockerfile. Variables created by ARG are only available during the image build (also called build-time). These variables are not available in the resulting Docker image or running container.
- **ENV** - Creates an environment variable. In contrast to ARG, variables created by ENV are available in the Docker image and running container.
- **WORKDIR** - Defines the working directory of the container.
- **COPY** - First argument is the source and second argument is the destination. There exists another command called **ADD** that contains extra features, but most of the time, **COPY** will suffice.
- **RUN** - Used to execute commands. Here, the RUN instruction uses Python's package manager to download additional libraries used by the app, and also makes a `logs` directory. Multiple commands should be combined into a single Docker instructions using `&&` as in the example above. This will minimize the number of steps Dockerfile which will improve image pull performance.
- **EXPOSE** - Used to expose (but not publish) ports listed.
- **USER** - This specifies the user and is the user used for subsequent commands. It is important that containers run as an unprivileged user. Containers [should not run as root](https://medium.com/@mccode/processes-in-containers-should-not-run-as-root-2feae3f0df3b) as this is a security vulnerability. Ford's CaaS platform will not execute any containers that attempt to run as root.
- **CMD** - Specifies what to run when the container starts. Takes an executable command (python) and parameters (app.py)

### Typical process of container development

1. Pick the correct base image
    - If you are building a container for a specific type of app or service (for example, a MySQL service or Java app), then use a base image made for it. For example, the Dockerfile above uses a Python base image available from Redhat's Container Catalog.
2. Build your environment step-by-step. When you are sure of a step, add it to your Dockerfile.
3. After adding the step to your Dockerfile, build the image. Ensure it produces the expected results.
4. Repeat steps 2 and 3 until your environment is built
5. Re-factor your Dockerfile if necessary per best practices

---

Continue to [Openshift console](./05-openshift-console.md).

Return to [Table of Contents](../README.md#agenda)
