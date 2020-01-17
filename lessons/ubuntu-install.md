The copy of `oc` for Linux hosted by Ford does not work with Ubuntu and may not work with certain other Linux distributions that we have not tested. If you encounter the following error use the steps below:

```
./oc: error while loading shared libraries: libcrypto.so.10: cannot open shared object file: No such file or directory
```

Download the tar file named `openshift-origin-client-tools-{some-version}-linux-64bit.tar.gz` from [here](https://artifacts-openshift-release-3-11.svc.ci.openshift.org/zips/) and extract it with:

```
tar -xzvf <file-name>
```

Then follow the Mac/Linux instructions on [the oc page](./5-console.md) to add it to your path.
