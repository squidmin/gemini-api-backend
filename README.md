# gemini-api-backend

This is a backend service for experimenting with the Gemini API.

## Installation

### 1. Install Python

You can install Python using `pyenv` on macOS or Linux. On Windows, you can use `pyenv-win`.

### 2. Install dependencies

You can install the dependencies using `pip` and the `requirements.txt` file.

```shell
pip3 install -r requirements.txt
```

### 3. Run the application

You can run the application using `uvicorn`.

```shell
uvicorn main:app --reload
```

The `--reload` flag enables hot reloading so the server will automatically reload when you make changes to your code.
You should see output indicating that the server is running, typically on `http://127.0.0.1:8000`.

### Building a Docker image

You can build the Docker image using the `Dockerfile` in the root directory.

```shell
docker build -t gemini-api-backend .
```

### Running a container locally

Use the `docker run` command and pass the `gemini-api-backend` service account key as an environment variable:

```shell
docker run -p 8000:8000 \
  -v /Users/admin/.config/gcloud/sa-private-key.json:/secrets/sa-private-key.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/sa-private-key.json \
  gemini-api-backend
```

---

## Usage

You can use the backend to interact with Gemini models, execute code, and perform other tasks.
