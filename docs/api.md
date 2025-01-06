Here is the revised and detailed documentation for the Rusty Bargain App API, including the endpoints for CRUD operations.

---

# Rusty Bargain App API Documentation

## Overview

The Rusty Bargain App provides a comprehensive RESTful API for managing vehicle data and running machine learning workflows for price prediction. The API is built using **FastAPI** and provides endpoints for:

- **CRUD operations**: Manage vehicle records.
- **Data preprocessing**: Prepare data for analysis and modeling.
- **Machine learning workflows**: Train, retrain, and predict vehicle prices.

You can explore and test all API endpoints using the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## API Endpoints

### CRUD Operations

#### 1. **Get All Vehicles**
- **Endpoint**: `/vehicles/`
- **Method**: `GET`
- **Description**: Retrieve a list of all vehicle records.
- **Response**:
    - **Status Code**: `200 OK`
    - **Body**: A list of vehicle objects.
    ```json
    [
      {
        "id": 1,
        "datecrawled": "2025-01-02T00:04:26.076Z",
        "price": 3500,
        "vehicletype": "sedan",
        "gearbox": "manual",
        ...
      }
    ]
    ```

#### 2. **Get a Single Vehicle**
- **Endpoint**: `/vehicles/{vehicle_id}`
- **Method**: `GET`
- **Description**: Retrieve details of a specific vehicle by its ID.
- **Path Parameter**:
    - `vehicle_id` (integer): The ID of the vehicle to retrieve.
- **Response**:
    - **Status Code**: `200 OK`
    - **Body**: A single vehicle object.

#### 3. **Add a New Vehicle**
- **Endpoint**: `/vehicles/`
- **Method**: `POST`
- **Description**: Add a new vehicle record to the database.
- **Request Body**:
    - JSON object representing the vehicle details.
      ```json
      {
        "datecrawled": "2025-01-02T00:04:26.076Z",
        "price": 4500,
        "vehicletype": "SUV",
        ...
      }
      ```
- **Response**:
    - **Status Code**: `201 Created`
    - **Body**: The created vehicle object.

#### 4. **Update a Vehicle**
- **Endpoint**: `/vehicles/{vehicle_id}`
- **Method**: `PUT`
- **Description**: Update details of an existing vehicle.
- **Path Parameter**:
    - `vehicle_id` (integer): The ID of the vehicle to update.
- **Request Body**:
    - JSON object with the updated vehicle details.
      ```json
      {
        "price": 4800,
        "vehicletype": "sedan",
        ...
      }
      ```
- **Response**:
    - **Status Code**: `200 OK`
    - **Body**: The updated vehicle object.

#### 5. **Delete a Vehicle**
- **Endpoint**: `/vehicles/{vehicle_id}`
- **Method**: `DELETE`
- **Description**: Remove a vehicle record from the database.
- **Path Parameter**:
    - `vehicle_id` (integer): The ID of the vehicle to delete.
- **Response**:
    - **Status Code**: `200 OK`

---

### Data Preprocessing

#### **Preprocess Data**
- **Endpoint**: `/preprocessdata`
- **Method**: `GET`
- **Description**: Preprocess raw vehicle data to prepare it for analysis.
- **Response**:
    - **Status Code**: `200 OK`
    - **Body**:
      ```json
      {
        "Message": "Data preprocessed successfully"
      }
      ```

---

### Machine Learning Workflows

#### 1. **Train Model**
- **Endpoint**: `/train_model`
- **Method**: `GET`
- **Description**: Train a machine learning model using preprocessed data.
- **Response**:
    - **Status Code**: `200 OK`
    - **Body**:
      ```json
      {
        "Message": "Model trained successfully"
      }
      ```

#### 2. **Load Model**
- **Endpoint**: `/load_model`
- **Method**: `GET`
- **Description**: Load the trained machine learning model for use.
- **Response**:
    - **Status Code**: `200 OK`
    - **Body**:
      ```json
      {
        "Message": "Model loaded successfully"
      }
      ```

#### 3. **Predict Price**
- **Endpoint**: `/predict_price/`
- **Method**: `POST`
- **Description**: Predict vehicle prices based on the provided input features.
- **Request Body**:
    - A list of JSON objects, each representing a vehicle's features.
      ```json
      [
        {
          "datecrawled": "2025-01-02T00:04:26.076Z",
          "vehicletype": "SUV",
          "gearbox": "automatic",
          ...
        }
      ]
      ```
  - **Response**:
    - **Status Code**: `200 OK`
    - **Body**:
      ```json
      {
        "Message": "Price predicted",
        "Price prediction": [3561.33, 4200.50]
      }
      ```

---

## Interactive API Documentation

You can test and explore the API endpoints using the Swagger-based interactive documentation available at:
- **URL**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Features:
- **Explore Endpoints**: View all available API routes and their details.
- **Test APIs**: Send requests directly from your browser.
- **View Schemas**: Understand the structure of request and response bodies.

---

## Error Handling

- **400 Bad Request**: Invalid input or missing fields.
- **404 Not Found**: Resource not found (e.g., invalid `vehicle_id`).
- **500 Internal Server Error**: Unexpected server-side error.

---

## Security

Currently, the API does not include authentication. Before deploying to production, consider implementing security mechanisms such as API keys or OAuth.

---

This documentation provides a detailed overview of the Rusty Bargain App API. For more information, refer to the source code or test the endpoints using the interactive documentation. 🚀