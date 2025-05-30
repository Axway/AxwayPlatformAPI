# UsageReportingToPlatform


## About
This is a sample script to upload ST usage metrics to the Amplify Platform. It is intended to be used in the event that the ST server resides in a network saegment with no outbound connectivity to internet. 

This is intended to be an example and Axway provides no support or guarantees. Please review, test, and update as needed prior to using in PROD. 

It will generate a full report for the previous calendar month and submit it to the Axway Platform. A copy of the report will be saved under **/Reports**
## Configuration

1. In the **/conf** directory, rename the file **sample.env** to **.env** and populate it with the Client ID and secret from the Axway Platform.
2. In the **/conf** directory, rename the file **config-sample.ini** to **config.ini** and Populate it with the Client ID and secret from the Axway Platform.


## Axway documentation

### Axway Platform REST API specification
https://platform.axway.com/api-docs.html

### Usage Reporting Configuration in ST
https://docs.axway.com/bundle/SecureTransport_55_AdministratorGuide_allOS_en_HTML5/page/Content/AdministratorsGuide/setup/create-usage-reports.htm

### SecureTransport REST API specification (admin)
https://apidocs.axway.com/swagger-ui-st/admin-20/



