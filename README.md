# Vehicle Price Prediction and Management App

## Table of Contents
- [Project Objective](#project-objective)
- [Project Structure and Steps](#project-structure-and-steps)
- [Tools and Techniques Utilized](#tools-and-techniques-utilized)
- [Specific Results and Outcomes](#specific-results-and-outcomes)
- [What I Have Learned from This Project](#what-i-have-learned-from-this-project)
- [How to Use This Repository](#how-to-use-this-repository)
- [Future Improvements and Enhancements](#future-improvements-and-enhancements)

For detailed documentation, please check [this link](https://realdanizilla.github.io/Rusty-Bargain-App/)

---

## Project Objective

This project aims to create a comprehensive application for managing vehicle data for a car re-seller and for predicting vehicle prices based on their features. The app consists of two main parts:
1. **CRUD Operations**: Manage a vehicle database, including adding, retrieving, updating, and deleting vehicle records.
2. **Machine Learning (ML) Prediction**: Predict vehicle prices using a trained ML model. Users can also re-train the model using updated data from the CRUD operations.

This project provides an intuitive interface for vehicle data management while integrating advanced predictive capabilities, making it a versatile tool for vehicle dealerships or marketplaces.

---

## Project Structure and Steps

The project is divided into the following components:

### 1. **Backend (CRUD Operations)**
- Built using FastAPI, the backend allows users to perform CRUD operations on the vehicle database.
- API Endpoints include:
  - Add new vehicle records.
  - Retrieve specific or all vehicle records.
  - Update existing vehicle information.
  - Delete vehicle records.

### 2. **PostgreSQL database to store vehicle data**.
The database consists of 2 tables:
1. A 'bronze' table with the raw car data. This is mainly used in the CRUD operations
2. A 'gold' table with preprocessed car data ready to be consumed by the ML model
3. The admin can use pgadmin4 to access and manage the database


### 3. **Frontend**
- Built using Streamlit, the frontend provides an interactive interface to:
  - View and manage vehicle records.
  - Input data for prediction.
  - Enter features for a vehicle and get a prediction on its price.
  - Re-train the ML model.

### 4. **Machine Learning Module**
- A CatBoost regression model is used to predict vehicle prices based on features such as mileage, power, brand, and type.
- The model can be re-trained with updated data from the CRUD operations to ensure accuracy and adaptability.

### 5. **Steps**
0. Create the database and inital 'bronze' table automatically.
1. Load the existing raw vehicle data into the bronze table using a SQL script.
2. Perform CRUD operations to manage vehicle data (create, read, update, delete).
3. Use the ML module to predict vehicle prices based on input features.
4. Re-train the ML model with updated database records as needed.
5. Check logs on pydantic's logfire

---

## Tools and Techniques Utilized

### **Backend and database**
- **FastAPI**: Framework for building RESTful APIs.
- **PostgreSQL**: Database for storing vehicle records.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: for data validation (input/output)

### **Frontend**
- **Streamlit**: Web app framework for creating interactive interfaces for CRUD operations, getting predictions from the ML model and re-training the model

### **Machine Learning**
- **CatBoost**: Gradient boosting algorithm used for price prediction.
- **Scikit-learn**: Data preprocessing and model evaluation.

### **Containerization and Deployment**
- **Docker**: To containerize the frontend, backend, database and database admin access (pgadmin4).
- **Docker Compose**: Orchestrate multi-container applications.

---

## Specific Results and Outcomes

1. **Database Management**:
   - Seamless CRUD operations via a user-friendly interface.
   - Ability to create, query, update, or delete specific vehicle records.

2. **Price Prediction**:
   - Accurate vehicle price predictions using the CatBoost model.
   - Prediction results are displayed interactively in the frontend.

3. **Model Retraining**:
   - Users can re-train the ML model using updated vehicle records.
   - Re-training ensures the model stays relevant to new data patterns.

---

## What I Have Learned from This Project

1. **Full-Stack Development**:
   - Integration of frontend (Streamlit) and backend (FastAPI) with a database (PostgreSQL).

2. **Machine Learning Lifecycle**:
   - From model construction on jupyter notebook to deployment with real-time predictions and re-training the model.
   - Handling preprocessing pipelines for the entire database and also for a single record, ensuring consistent encoding and scaling of features.

3. **Database Management**:
   - Efficient handling of relational data using PostgreSQL and SQLAlchemy.
   - MVC database model (model, viewer, controller)
   - Data validation with Pydantic schemas
   - Splitting raw data on a 'bronze' table and preprocessed data ready to be consumed by the ML model on a 'gold' table

4. **Containerization**:
   - Simplified deployment and scalability using Docker and Docker Compose.

5. **User Experience**:
   - Designing intuitive interfaces for non-technical users to interact with advanced ML models.

---

## How to Use This Repository

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-repository-url.git
cd your-repository-url
```

### 2. **Set Up Environment**
Ensure Docker and Docker Compose are installed on your system or download/use Docker Desktop

### 3. **Run the Application**
Use Docker Compose to start the frontend, backend, database and pgadmin (database administration):
```bash
docker-compose up --build
```
Once application is running, monitor activity on logfire. Database will be populated automatically with raw data.

### 4. **Access the Application**
- **Frontend**: Visit `http://localhost:8501` for the Streamlit app.
- **Backend**: Access API documentation at `http://localhost:8000/docs`.
- **Database**: Use PgAdmin4 to access the PostgreSQL database:
  - Visit `http://localhost:5050`.
  - Log in with the credentials defined in your `docker-compose.yml`.
  - Add a new server connection:
    - **Host**: `host.docker.internal`
    - **Port**: `55432`
    - **Username**: `ùser`
    - **Password**: `password`
    - **Database**: `rusty_bargain` (or the database name you are using).

### 5. **Perform CRUD Operations**
- Use the Streamlit interface to manage the vehicle database.
- Test the API directly using the Swagger UI at `http://localhost:8000/docs`.

### 6. **Predict Vehicle Prices**
- Use the Streamlit interface to Input vehicle features and get a price prediction.

### 7. **Re-train the Model**
- Use the re-train option in the frontend to update the model with new database records.

---

For more details, refer to the original inspiration and project structure at [Rusty Bargain App](https://github.com/realdanizilla/Rusty-Bargain-App).

# Future Improvements and Enhancements

1. Create tests using pytest
2. Implement a modern dark theme for streamlit