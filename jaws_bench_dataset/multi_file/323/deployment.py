# This module handles the deployment of the cloud function to the cloud provider.

import subprocess

def deploy_function(function_path):
    # Command to deploy the cloud function
    # Replace 'gcloud' with the appropriate command for your cloud provider
    command = f"gcloud functions deploy myFunction --runtime python39 --trigger-http --allow-unauthenticated --entry-point main --source {function_path}"

    # Execute the deployment command
    subprocess.run(command, shell=True, check=True)