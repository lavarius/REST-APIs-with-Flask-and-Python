# REST APIS with Flask and Python Project Extended with Docker

This base of this project started from Teclado's Jose Salvetierra's course, and I have made modifications
to run docker-compose locally and test endpoints and get familiar with the CRUD operations of APIs.

Render was used for deploying the Flask app on a Web Service and using a Redis server.
PostgreSQL was available for free on ElephantSQL.

Remarks: Great highlights are getting exposed to Flask-Smorest and the usages of Blueprints and MethodViews

Docker

- Introduction
- Mapping volumes from host to Docker Container,
- Bind mount your app code to a Docker container

SQL Storage

- Local development with Flask-SQLAlchemy
- Concepts of Models, one-to-many relationships
- using `db` to insert, get, update, retrive a list, delete models
- Delete models with relationships with cascades
- Create a many-to-many relationships with items and tags
- Build upon the above base knowledge
- Database migrations, making changes to tables in your database using Flask-Migrate and Alembic
- Going into production ready mode, WSGI service like gunicorn is used and moved reference of database to a PostgreSQL database cloud storage service.

---

From here, we want to change things up and using services you'll see at Enterprises, so we'll use Azure in this case since I'm most familiar with it at the moment.

To Do: Extend with Azure Web Services

- Azure Cache for Redis
- Azure Database for PostgreSQL
- Azure App Service for Web App

  - Create RG and Azure Container Registry
  - Create App Service Plan
  - Create Web App
  - Deploy Docker Container

- Nice to Have: Get familiar with resources and try an automated resource provisioning with Terraform
- Stretch: Get really fancy with Azure Pipelines?

- Implement React for frontend with the endpoints already available
