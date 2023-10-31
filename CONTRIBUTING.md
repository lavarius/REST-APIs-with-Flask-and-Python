# CONTRIBUTING

# How to run the Dockerfiel locally

Since `docker-compose.yml` and `Dockerfile` depend on each other, simply run the following in the command line:
```
docker compose up -d
```

Previously before implementing Redis, the command line was:
```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python
```

with prior Docker builds done like:
```
docker build -t rest-apis-flask-python .
```
