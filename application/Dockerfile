# Use an official Python runtime as a parent image
FROM registry.redhat.io/rhscl/python-36-rhel7

# required by Python's pip installer because LD_LIBRARY_PATH env var is empty during docker build
ARG LD_LIBRARY_PATH=/opt/rh/python36/root/usr/lib64

# Define environment variables
ENV \
    HOME=/app \
    USER_UID=1001 \
    SUMMARY="A simple python web app"	\
    DESCRIPTION="This is a python web app to demonstrate basic container and kubernetes concepts." \
    NAME=World

# Set the working directory to /app
WORKDIR $HOME

# Copy the current directory contents into the container at /app
COPY ./src $HOME

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

### The RedHat python image ships with unprivileged user default, 1001.
# "Processes In Containers Should Not Run As Root" > https://medium.com/@mccode/processes-in-containers-should-not-run-as-root-2feae3f0df3b
USER $USER_UID

# Run app.py when the container launches
CMD ["python", "app.py"]