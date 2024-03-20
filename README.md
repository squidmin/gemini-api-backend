# gemini-api-backend

This is a backend service for experimenting with the Gemini API.

## Installation

### 1. Install Python

You can install Python using `pyenv` on macOS or Linux. On Windows, you can use `pyenv-win`.

### 2. Install dependencies

You can install the dependencies using `pip` and the `requirements.txt` file.

```shell
pip install -r requirements.txt
```

### 3. Run the application

You can run the application using `uvicorn`.

```shell
uvicorn main:app --reload
```

The `--reload` flag enables hot reloading so the server will automatically reload when you make changes to your code.
You should see output indicating that the server is running, typically on `http://127.0.0.1:8000`.

## Usage

You can use the backend to interact with Gemini models, execute code, and perform other tasks.
