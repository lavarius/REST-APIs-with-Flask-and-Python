# Import the necessary modules for your tests
import json
import pytest
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema
from app import app  # Import your Flask app instance


blp = Blueprint("stores", __name__, description="Operations on stores")

# Create a test client to interact with your app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client



@blp.route("/store")
class StoreList(MethodView):
    # Define a test case for an API endpoint
    @blp.arguments(StoreSchema)
    def test_hello_world(self, client, store_data):
        response = client.get('/store')  # Replace with your actual endpoint URL
        # data = json.loads(response.get_data(as_text=True))
        
        # Add your assertions to test the response
        assert response.status_code == 200
        assert store_data['name'] == 'Hello, World!'

    def get(self):
        return {"stores": list(stores.values())}