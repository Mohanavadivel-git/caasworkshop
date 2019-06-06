
# Troubleshooting for OpenShift localdev Setup

## Issue - VPN
### Behavior
Vagrant up will fail/timeout at this section. 

```bash
 INFO oc-localdev: Writing CoreDNS Corefile
 INFO oc-localdev: Writing CoreDNS zonefile
 INFO oc-localdev: Writing CoreDNS reverse zonefile
 INFO oc-localdev: Starting CoreDNS service
 INFO oc-localdev: Updating the local DNS setting
```

### Root Cause and Workaround
As a general note - localdev will NOT work over VPN. There is no current workaround. 

---
## Issue - Timeout/Endless Loop
### Behavior

After issuing the `vagrant up` command, you reach a point of an endless loop that looks similar to the examples below: 

```bash
openshift-enterprise-3.11.98-master: Waiting for calico-node-* pod to start 1407 seconds ...
openshift-enterprise-3.11.98-master: The connection to the server api-int.oc.local:8443 was refused - did you specify the right host or port?
openshift-enterprise-3.11.98-master: Waiting for calico-node-* pod to start 1410 seconds ...
openshift-enterprise-3.11.98-master: The connection to the server api-int.oc.local:8443 was refused - did you specify the right host or port?
openshift-enterprise-3.11.98-master: Waiting for calico-node-* pod to start 1413 seconds ...
```

or 

```bash
openshift-enterprise-3.11.98-master: Waiting for apiserver-* pod to start 66 seconds ...
openshift-enterprise-3.11.98-master: No resources found.
openshift-enterprise-3.11.98-master: Unable to connect to the server: net/http: TLS handshake timeout
openshift-enterprise-3.11.98-master: Waiting for apiserver-* pod to start 69 seconds ...
openshift-enterprise-3.11.98-master: No resources found.
openshift-enterprise-3.11.98-master: The connection to the server api-int.oc.local:8443 was refused - did you specify the right host or port?
openshift-enterprise-3.11.98-master: Waiting for apiserver-* pod to start 72 seconds ...
openshift-enterprise-3.11.98-master: No resources found.
openshift-enterprise-3.11.98-master: The connection to the server api-int.oc.local:8443 was refused - did you specify the right host or port?
openshift-enterprise-3.11.98-master: Waiting for apiserver-* pod to start 75 seconds ...
```

### Root Cause and Workaround
This is a result of the number of CPU cores your machine has. You must have a 4 core CPU. 

---
## Issue - Proxy Settings
### Behavior
$ oc login https://console.oc.local:8443
error: Service Unavailable

### Root Cause and Workaround
Terminal has proxy environment variables set causing traffic to go to proxy server which could not route traffic back to the localhost. Remove proxy variables or add `.local` to `no_proxy` env vars.
```bash
export NO_PROXY=$NO_PROXY,.local
export no_proxy=$no_proxy,.local
```
---
## Issue - Local DNS Issue
### Behavior
$ curl -s -v https://console.oc.local:8443
```bash
*Rebuilt URL to: https://console.oc.local:8443/
*timeout on name lookup is not supported
*getaddrinfo(3) failed for console.oc.local:8443
*Couldn't resolve host 'console.oc.local'
*Closing connection 0
```
### Root Cause and Workaround

Localdev uses a self-signed cert. Use the `--insecure-skip-tls-verify` flag when logging in: `oc login https://console.oc.local:8443 --insecure-skip-tls-verify`

---

## Issue - Self-Signed TLS Certificate
### Behavior
```bash
oc login https://console.oc.local:8443
error: The server uses a certificate signed by unknown authority. You may need to use the --certificate-authority flag to provide the path to a certificate file for the certificate authority, or --insecure-skip-tls-verify to bypass the certificate check and use insecure connections.
```
### Root Cause and Workaround

Localdev uses a self-signed cert. Use the `--insecure-skip-tls-verify` flag when logging in: `oc login https://console.oc.local:8443 --insecure-skip-tls-verify`.


---

## Issue - Builder Pod Cannot Authenticate with GitHub
### Behavior
```bash
$ oc new-app git@github.ford.com:YES/my-demo.git
$ oc logs -f bc/my-demo
Cloning "git@github.ford.com:YES/python-demo.git" ...
error: Host key verification failed.
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
```
### Root Cause and Workaround

Localdev builder pod needs SSH keys to clone repos from Ford's GitHub. See section below to set up a source clone secret and use it when creating a new-app. Also see https://docs.openshift.com/container-platform/3.11/dev_guide/builds/build_inputs.html#source-clone-secrets.

---
## Issue - Bash Script Failing to Run
### Behavior
I wrote a bash script in a Windows text editor, but when I try to execute that script from the CaaS/localdev virtual machine, it fails with the following.
```bash
# ./build.sh
-bash: ./build.sh: /bin/bash^M: bad interpreter: No such file or directory
```
### Root Cause and Workaround

The error is telling use that the bash binary is not found at `/bin/bash^M`. The `^M` is due to the script containing Windows/DOS line endings being executed in a Linux environment. Windows/DOS uses carriage return and line feed ("\r\n") as a line ending while Unix uses just line feed ("\n"). To resolve, convert the script to Unix line endings, i.e. `dos2unix build.sh`.

---

## Issue - IP Prompt
### Behavior
You are not be prompted for your IP address after running vagrant up. 
```bash
Bringing machine 'openshift-enterprise-3.11.98-master' up with 'virtualbox' provider...
==> openshift-enterprise-3.11.98-master: Running triggers before up ...
==> openshift-enterprise-3.11.98-master: Running trigger: before up...
==> openshift-enterprise-3.11.98-master:
==> openshift-enterprise-3.11.98-master: Executing trigger before up or provision... # <--- You ought to be prompted for your IP address after this step
 INFO oc-localdev: Writing CoreDNS Corefile
 INFO oc-localdev: Writing CoreDNS zonefile
 INFO oc-localdev: Writing CoreDNS reverse zonefile
 INFO oc-localdev: Starting CoreDNS service
```

### Root Cause and Workaround

This may lead to errors when your IP address changes (going on/off wifi, changing buildings, etc). Ensure you do not have an environment variable set for DEFAULT_HOST_IP
```bash
unset DEFAULT_HOST_IP
```

---
## Issue - Failed to start Virtual Box
### Behavior
```bash
>vagrant up
......
Stderr: VBoxManage.exe: error: The virtual machine 'CaaS-localdev' has terminated unexpectedly during startup with exit code 1 (0x1).  More details may be available in 'C:\Users\{CDSID}\VirtualBox VMs\CaaS-localdev\Logs\VBoxHardening.log'
VBoxManage.exe: error: Details: code E_FAIL (0x80004005), component MachineWrap, interface IMachine
Open C:\Users\{CDSID}\VirtualBox VMs\CaaS-localdev\logs\VBoxHardening.log, it will have the lines like below in the log:
........
5798.4578:     FileDescription: BeyondTrust PowerBroker for Windows DLL
5798.4578: supR3HardenedWinInitAppBin(0x0): '\Device\HarddiskVolume4\Program Files\Oracle\VirtualBox'
5798.4578: supR3HardenedWinReInstallHooks: Reinstalling NtCreateSection (00007ffd32eaffc0: e9 13 05 f5 ff cc cc cc cc cc ff e0 03 fe 7f 01).
5798.4578: Calling main()
5798.4578: SUPR3HardenedMain: pszProgName=VBoxHeadless fFlags=0x0
5798.4578: supR3HardenedWinInitAppBin(0x0): '\Device\HarddiskVolume4\Program Files\Oracle\VirtualBox'
5798.4578: '\Device\HarddiskVolume4\Program Files\Oracle\VirtualBox\VBoxHeadless.exe' has no imports
5798.4578: supHardenedWinVerifyImageByHandle: -> 24202 (\Device\HarddiskVolume4\Program Files\Oracle\VirtualBox\VBoxHeadless.exe)
5798.4578: SUPR3HardenedMain: Respawn #2
5798.4578: Error (rc=-5640):
5798.4578: More than one thread in process
5798.4578: Error -5640 in supR3HardenedWinReSpawn! (enmWhat=1)
5798.4578: More than one thread in process
4624.5910: supR3HardNtChildWaitFor[1]: Quitting: ExitCode=0x1 (rcNtWait=0x0, rcNt1=0x0, rcNt2=0x103, rcNt3=0x103, 23 ms, the end);
```
### Root Cause and Workaround

BeyondTrust Services interrupt Virtual Box starting process.
Go to C:\Program Files\BeyondTrust\PowerBroker for Windows Client\Tools\Diagnostics
Run PBWDiagnosticsApp.exe
Stop all running services
Try 'vagrant up' command again

---

## Issue - VM Failure
### Behavior
```
INFO oc-localdev: completed trigger processing
==> openshift-enterprise-3.11.98-master: Importing base box 'openshift-enterprise-basic-cnx-3.11'...
==> openshift-enterprise-3.11.98-master: Matching MAC address for NAT networking...
==> openshift-enterprise-3.11.98-master: Checking if box 'openshift-enterprise-basic-cnx-3.11' version '3.11.98-1' is up to date...
==> openshift-enterprise-3.11.98-master: Setting the name of the VM: CaaS-localdev
The name of your virtual machine couldn't be set because VirtualBox
is reporting another VM with that name already exists. Most of the
time, this is because of an error with VirtualBox not cleaning up
properly. To fix this, verify that no VMs with that name do exist
(by opening the VirtualBox GUI). If they don't, then look at the
folder in the error message from VirtualBox below and remove it
if there isn't any information you need in there.
```

or

```
VBoxManage.exe: error: Could not rename the directory 'C:\Users\CDSID\VirtualBox VMs\openshift-enterprise-3.11.98-master_1558533015087_71698' to 'C:\Users\CDSID\VirtualBox VMs\CaaS-localdev' to save the settings file (VERR_ALREADY_EXISTS)
VBoxManage.exe: error: Details: code E_FAIL (0x80004005), component SessionMachine, interface IMachine, callee IUnknown
VBoxManage.exe: error: Context: "SaveSettings()" at line 3111 of file VBoxManageModifyVM.cpp
```

### Root Cause and Workaround
To resolve this error, delete the VM `CaaS-localdev` from VirtualBox. 
1. Open Virtual Box Manager from the windows start menu
2. Locate the VM named `CaaS-localdev` in the Virtual box manager, then open a windows explorer window to the storage location for Virtual Box VMs
    - This location should be in the error message, generally in `C:\Users\CDSID\VirtualBox VMs`
3. Locate and delete the folder `CaaS-localdev`
4. Retry starting localdev again by issuing the `vagrant up` command from the terminal

