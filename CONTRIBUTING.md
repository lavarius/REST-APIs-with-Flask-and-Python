# CONTRIBUTING

## Create Docker file locally
```
docker build -t rest-apis-flask-python .
```

## How to run the Dockerfile locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

## How to run docker-compose locally
### Powershell
```
startup_services.ps1
```
### bash
```
sh startup.services.sh
```

## How to run the Flask App with Cloud Services (Render.com and ElephantSQL)
The .env file should have environment variables
```
ENV=local
DATABASE_URL=
REDIS_URL=
```

When running on the cloud, the web app should run the docker-entrypoint.sh and the Environment Variables set with the 3 above where
```
ENV=cloud
```