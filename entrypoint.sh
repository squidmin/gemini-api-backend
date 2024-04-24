# !/bin/bash

pyenv local 3.12.0b4
eval "$(pyenv init --path)"
python3 --version

export GOOGLE_CLOUD_PROJECT="lofty-root-378503"
export GEMINI_API_KEY_SECRET_NAME="gemini-api-key"

# Fetch the project ID and API key secret name from environment variables
project_id="${GOOGLE_CLOUD_PROJECT}"
api_key_secret_name="${GEMINI_API_KEY_SECRET_NAME}"

if [[ -z "$project_id" || -z "$api_key_secret_name" ]]; then
    echo "Project ID or API Key Secret Name is not set."
    exit 1
fi

# Construct the full name of the secret version
secret_version_name="projects/${project_id}/secrets/${api_key_secret_name}/versions/latest"

# Use gcloud to access the secret and assign it to a variable
GEMINI_API_KEY=$(gcloud secrets versions access latest --secret="${api_key_secret_name}" --project="${project_id}")

# Check if the GEMINI_API_KEY retrieval was successful
if [[ -z "GEMINI_API_KEY" ]]; then
    echo "Failed to fetch the Gemini API Key."
    exit 1
else
    echo "Successfully fetched the Gemini API Key."
    # Export the OPENAI_API_KEY environment variable
    export GEMINI_API_KEY
fi

pip3 install -r requirements.txt

uvicorn main:app --reload
