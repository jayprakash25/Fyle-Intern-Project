# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py

# Run migrations
RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]