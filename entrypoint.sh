#!/bin/bash

echo "Setting up the environment..."

export GOOGLE_CLOUD_PROJECT="lofty-root-378503"
export GEMINI_API_KEY_SECRET_NAME="gemini-api-key"

project_id="${GOOGLE_CLOUD_PROJECT}"
api_key_secret_name="${GEMINI_API_KEY_SECRET_NAME}"

if [[ -z "$project_id" || -z "$api_key_secret_name" ]]; then
    echo "Project ID or API Key Secret Name is not set."
    exit 1
fi

# Authenticate using service account
if [[ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
    echo "GOOGLE_APPLICATION_CREDENTIALS not set."
    exit 1
fi

gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Construct the full name of the secret version
secret_version_name="projects/${project_id}/secrets/${api_key_secret_name}/versions/latest"

# Access the secret and assign it to a variable
GEMINI_API_KEY=$(gcloud secrets versions access latest --secret="${api_key_secret_name}" --project="${project_id}")

# Check if the GEMINI_API_KEY retrieval was successful
if [[ -z "GEMINI_API_KEY" ]]; then
    echo "Failed to fetch the Gemini API Key."
    exit 1
else
    echo "Successfully fetched the Gemini API Key."
    export GEMINI_API_KEY
fi

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
