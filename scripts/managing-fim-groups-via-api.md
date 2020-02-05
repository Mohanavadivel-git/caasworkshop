# Managing FIM Security Groups with API Calls

## Summary

Ford's CaaS platform uses FIM Security Groups to control access to Kubernetes Namespaces. FIM groups can be managed through a web portal or through API calls. An individual FIM group can be configured for either web management or API management, but not both.

This document shows how the Dev Enablement team uses API calls to add and remove members to a FIM group that controls access to our CaaS Workshop namespace.

## Usage
Before you can call the FIM API, you'll have to add your client app to the [API portal](https://thehubat.ford.com/groups/platform-enablement). You will establish a client ID and client secret that you will use to get a token allowing your client app to call the FIM API.<br>
You will have to work with the FIM team to make the FIM security group(s) API managed if they are existing and created by using [Security Group Portal](https://iam.ford.com/IdentityManagement/default.aspx).

We use Postman to call the FIM API to add/remove member(s) to/from the FIM group `DEV-ENABLEMENT-WORKSHOP-DEVELOPER`. You can use any tool you want, but we have already configured a Postman Collection for our particular FIM group that has our client ID and client secret embedded in it. The collection is saved in our team's network drive which permissions are restricted to only our team. Following the steps below to install Postman, setup requests colection and invoke API:<br>

- Install Postman tool
  - For Windows, download the Ford-hosted [setup executable](http://www.nexus.ford.com/#browse/search=keyword%3DPostman:2f6cfc0a843140c285b19238d9b55dbf:d13f75665f0cf9bcc272d3bfcc65a857).
  - For Other OS, download Postman from [getpostman.com](https://www.getpostman.com/).
- Get the Collection from our shared network drive
  - Map network folder `\\ecc9000201\proj` to an available local drive ( usually it is mapped to drive W).
  - Make sure you have permissions to access folder `\\ecc9000201\proj\j2ee` where we store the collection file containing client_id, client_secret and app_id.<br>
  ![CaaS Workflow](/images/ShareDrive.png)
- Open Postman, click on `Import` button shown as screenshot below:<br>
 ![CaaS Workflow](/images/Postman01.png)
  - Select `Choose Files`
  ![CaaS Workflow](/images/Postman02.png)
  - Select `W:\j2ee\CaaSWorkshopSGPAPI\CaaSWorkshopSGPAPI.json`
  - Click Open<br>
  ![CaaS Workflow](https://github.ford.com/jchen45/caas-workshop/blob/master/images/Postman03.png)
- The collection should be imported like the screenshot below:<br>
 ![CaaS Workflow](/images/Postman04.png)
- You can invoke an API by clicking on it

To add members:
Edit the body of the POST request by replacing `CDSID` with the cdsid of the individual you want to add. To add multiple individuals, separate each cdsid with “,”, e.g. “cdsid01”, “cdsid02”, “cdsid03”.<br>
![CaaS Workflow](/images/Postman05.png)

To delete members:
Select the API shown as screenshot below. Edit the body of the PATCH request similar to "add member" process above to delete single or multiple individuals.
![CaaS Workflow](/images/Postman06.png)
*Do something similar*

## Errors

If you get the response like below:
    "httpCode": "401",
    "httpMessage": "Unauthorized",
"moreInformation": "application is not registered, or active"

Click on “Authorization” tab, select "Client Credentials" for "Grant type", click on red buttons “Get New Access Token”, “Request Token” and “Use Token” consecutively on popup window; then click on blue button “Send”.
