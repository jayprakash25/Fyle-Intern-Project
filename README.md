## Setup

This application can be run either using Docker or directly on your machine.

### Prerequisites

- Python 3.8 installed on your machine. You can download Python [here](https://www.python.org/downloads/).
- Docker installed on your machine (optional). You can download Docker [here](https://www.docker.com/products/docker-desktop).

### Running with Docker

1. Clone the repository:
    ```
    git clone https://github.com/jayprakash25/Fyle-Intern-Project.git
    ```

2. Navigate to the project directory:
    ```
    cd Fyle-Intern-Project
    ```

3. Build the Docker image:
    ```
    docker build -t my-python-app .
    ```

4. Run the Docker container:
    ```
    docker run -p 5000:5000 my-python-app
    ```

The application should now be running at `http://localhost:5000`.

### Running without Docker

1. Clone the repository:
    ```
    git clone https://github.com/jayprakash25/Fyle-Intern-Project.git
    ```

2. Navigate to the project directory:
    ```
    cd Fyle-Intern-Project
    ```

3. Create a virtual environment and activate it:
    ```
    virtualenv env --python=python3.8
    source env/bin/activate
    ```

4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

5. Reset the database:
    ```
    export FLASK_APP=core/server.py
    rm core/store.sqlite3
    flask db upgrade -d core/migrations/
    ```

6. Start the server:
    ```
    bash run.sh
    ```


## Application Structure

- `core/server.py`: This is the main application file.
- `core/migrations/`: This directory contains database migration files.
- `requirements.txt`: This file contains a list of python dependencies to be installed.
- `app.ini`: This is the uWSGI configuration file.
- `run.sh`: This is a bash script to start the server.

## Note

The Dockerfile in this project uses Python 3.8 slim image. It sets the working directory in the container to `/app`. It then adds the current directory contents into the container at `/app` and installs the necessary packages specified in `requirements.txt`. It sets the environment variable `FLASK_APP` to `core/server.py` and runs database migrations. It exposes port 5000 and starts the uWSGI server.
