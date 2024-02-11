import azure.functions as func
from azure.storage.blob import BlobServiceClient
import logging
import os
from datetime import datetime
import random
import uuid
import io
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
       # Load environment variables for Azure Storage credentials
       connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
       container_name = os.environ["AZURE_STORAGE_CONTAINER_NAME"]
       storage_account_name= os.environ["AZURE_STORAGE_ACCOUNT_NAME"]

       # Generate data with randomized values
       data = {
           "timestamp": datetime.utcnow().isoformat(timespec='seconds'),
           "module": random.choice(["Marija", "Petar", "Marko", "Ana", "Ivan"]),
           "sensor_id": str(uuid.uuid4()),
           "sensor_type": random.choice(["temperature", "humidity", "pressure"]),
           "value": random.uniform(0, 100),
           "unit": random.choice(["celsius", "fahrenheit", "pascal"])
       }

       # Create a unique file name
       file_name = f"{data['sensor_id']}.json"

       # Serialize data to JSON string
       json_string = json.dumps(data, indent=4)

       # Upload the JSON data to Azure Storage container
       with io.BytesIO(json_string.encode()) as data_stream:
           blob_service_client = BlobServiceClient.from_connection_string(connection_string)
           blob_client = blob_service_client.get_container_client(container_name).get_blob_client(file_name)
           blob_client.upload_blob(data_stream, overwrite=True)

       # Generate the file URL
       file_url = f"https://{storage_account_name}.blob.core.windows.net/{file_name}"

       return func.HttpResponse(
           body=f"JSON file {file_name} generated and uploaded: {file_url}",
           status_code=200,
           mimetype="text/plain"
       )

    except Exception as e:
        return func.HttpResponse(
           body=f"Error generating and uploading JSON: {e}",
           status_code=500,
           mimetype="text/plain"
       )
    