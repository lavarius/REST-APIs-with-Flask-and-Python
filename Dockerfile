# Use an official Python runtime as a parent image
FROM python:3.11
WORKDIR /app

# Add the requirements file to the container
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
