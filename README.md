## Introduction 

The purpose of this exercise is to gain hands-on experience for mainly Azure Functions, but in terms of other elementary services, such as Azure Databases and Blob Storage. 

Here we are going to create two Azure functions which we will deploy to a single Function App. The first one will create sensor data, save it in a json file and upload it to Blob storage. This function is planned to be triggered via an HTTP request. The second function should get triggered on the upload of this file to the specific location inside of Storage account (i.e. to have a Blob Trigger) and should to some “transformations” on that uploaded file and save it in a Postgres table. 

We are going to develop these functions locally, test them and deploy them to Azure, and finally test them there. And of course, do the clean-up! 

Simplified process for creating the first function using VS Code can be found here, in the official Microsoft documentation. The GitHub repository provided below serves only as a guide and support to create and run this application, but we are going to start from scratch. 

### Pre- requisites 

* Python installed 
* Docker installed and running 
* VS Code installed 
* Azure Subscription  
* Postman installed (or similar tool) 
* DBeaver installed (or similar tool) 
* Storage Account and blob container created 
* Optional: Microsoft Azure Storage Explorer  

## Steps 

* Clone this repo: https://github.com/celikovicmarija/functionappdemo It is just a guide, and copy-pasting. Please create a separate, empty folder for your work. 
* Download and install Azure CLI  
* Open VS Code 

Install the following extensions: 

* Azure Functions 
Azure Account 

Create function app (from portal preferably) with a Python runtime 
After installing the extensions, Azure tab should be available on the right side inside VS Code. There should be two sections: Resources(top) and Workspace(bottom). Click on the Azure function logo to create the Azure Function, following the requested steps. 



First function should have HTTP trigger. Function should have a Python runtime and use Programming model V1. The Authorization level is Anonymous. To learn more about this trigger, this page could be useful. 
After the function is created, the virtual environment is created automatically for you. You need to activate it: 

`.venv\Scripts\activate (Windows) `

`source .venv/bin/activate (Mac) ` (if the virtual environment was not created automatically, you can do so manually from the terminal: python -m venv .venv) 

Okay, we have the basics. Now let’s look at file file structure: 

File local.settings.json : all the connections to other services, environment variables can be defined here, as in the cloned repo: 
```
{ 
  "IsEncrypted": false, 
  "Values": { 
    "AzureWebJobsStorage": ""${STORAGE_CONN_STRING}", 
    "FUNCTIONS_WORKER_RUNTIME": "python", 
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing", 
    "AZURE_STORAGE_CONNECTION_STRING": "${STORAGE_CONN_STRING}", 
    "AZURE_STORAGE_CONTAINER_NAME": "${CONTAINER}", 
    "AZURE_STORAGE_ACCOUNT_NAME":"${STORAGE_ACCOUNT_NAME}", 
    "host":"${DB_HOST}, 
    "user":"${DB_USER}", 
    "password":"${DB_PWD}" 
  } 
} 
```
 

NOTE: All these variables will have to be re-created manually in the portal, under FunctionApp -> Settings-> Environment variables! Since local.settings.json is used only for local development is ignored during deployment! 
File *host.json*: updated compared to auto-generated file to add logging configuration. Feel free to copy-paste the content. It contains configuration options that affect all functions in a function app instance. For more information, please refer to this page. 
File *requirements.txt* with python dependencies used for local development. Update your file with the values in the cloned repo. 
File *.funcignore*: file where one can see/ add elements which needn’t be deployed. 

Inside of the folder for the created function: function.json. This file configures triggers and bindings. To understand the basic function of it and content, please read the following page (up until “Connect to database section”). 
The function content itself could be taken from __init__.py file in event_generation_sensors folder. Take a moment to observe the code. 
This function would need connection to Storage account; therefore we need connection string. Put it in place of  AZURE_STORAGE_CONNECTION_STRING value inside of local.settings.json 



Time to test everything! Open Postman! Click FN+ F5 to run the application. After a minute, you will receive an endpoint in the terminal: 

Awesome, that works. We move on to creating a different function which will be triggered on the file upload. To learn about the Blob trigger, have a look at this page. Follow the same procedure and create another function which has the blob trigger. 
Copy paste the code from __init__.py file in mace_blob_trigger folder to your newly created function. Adjust the blob connection strings, in you haven’t already done so through the VS Code prompt. Also adjust DB credentials in local.settings.json.  
Run the function again. This time, on the file upload, in the postgres DB table you should see a new row added (by doing query  select * from public.station_data): 


At the end, run the following command (for this step, Docker needs to be up and running- no other installations needed): 
`func azure functionapp publish ${FUNCTION_APP_NAME} --build-native-deps `

 

What is left is to test the deployed app. First, check the URL for HTTP Trigger Function in the portal: 

Test it in the Postman.
Ultimately, check the DB to see if there is a new row added to the DB. 
Pat yourself on the back! 

## Final Thoughts 

Please, do a clean-up of all the resources you have created. You can do that by deleting the resource group(s) created during this exercise. The code also could be integrated with a version control system (e.g. GitHub) to enable automated CI/CD process (e.g. Using GitHub Workflows). 
