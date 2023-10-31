FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN apk add --no-cache docker-compose
CMD ["flask", "run", "--host", "0.0.0.0"]