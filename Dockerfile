# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Add the requirements file to the container
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Install docker-compose
RUN apt-get update && \
   apt-get install -y docker-compose

# Run the command to start uWSGI
CMD ["flask", "run", "--host", "0.0.0.0"]