# Managing FIM Security Groups with API Calls

## Summary

Ford's CaaS platform uses FIM Security Groups to control access to Kubernetes Namespaces. FIM groups can be managed through a web portal or through API calls. An individual FIM group can be configured for either web management or API management, but not both.

This document shows how the Dev Enablement team uses API calls to add and remove members to a FIM group that controls access to our CaaS Workshop namespace.

## Usage
Before you can call the FIM API, you'll have to add your client app to the API portal. You will establish a client ID and client secret that you will use to get a token allowing your client app to call the FIM API.

We use Postman to call the FIM API to add/remove member(s) to/from the FIM group `DEV-ENABLEMENT-WORKSHOP-DEVELOPER`. You can use any tool you want, but we have already configured a Postman Collection for our particular FIM group that has our client ID and client secret embedded in it. The collection is saved in our team's network drive which permissions are restricted to only our team.

You will have to work with the FIM team to

- Install Postman tool
  - For Windows, download the Ford-hosted [Binary](https://it2.spt.ford.com/sites/WebCOE/Docs/Downloads/Web%20Components/Postman-win64-7.14.0-Setup.exe).
  - For Other OS, download Postman from [getpostman.com](https://www.getpostman.com/).
- Get the Collection from our shared network drive
  - Map ` \\ecc9000201` to a drive, e.g. W:
  - Check that you have permissions to access folder `\\ecc9000201\j2ee` where we store the collection file containing client_id, client_secret and app_id.
- Open Postman, click on `Import` button shown as screenshot below:
  - Select `Choose Files`
  - Select `W:\j2ee\CaaSWorkshopSGPAPI\CaaSWorkshopSGPAPI.json`
  - Click Open
- The collection should be imported like the screenshot below:
- You can invoke an API by clicking on it

To add members:

Edit the body of the POST request by replacing `CDSID` with the cdsid of the individual you want to add. To add multiple individuals, separate each cdsid with “,”, e.g. “cdsid01”, “cdsid02”, “cdsid03”.

To delete members:

*Do something similar*

## Errors

If you get the response like below:
    "httpCode": "401",
    "httpMessage": "Unauthorized",
"moreInformation": "application is not registered, or active"

Click on “Authorization” tab, click on red buttons “Get New Access Token”, “Request Token” and “Use Token” consecutively on popup window; then click on blue button “Send”.
