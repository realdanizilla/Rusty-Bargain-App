# Vehicle Price Prediction and Management App

## Table of Contents
- [Project Objective](#project-objective)
- [Project Structure and Steps](#project-structure-and-steps)
- [Tools and Techniques Utilized](#tools-and-techniques-utilized)
- [Specific Results and Outcomes](#specific-results-and-outcomes)
- [What I Have Learned from This Project](#what-i-have-learned-from-this-project)
- [How to Use This Repository](#how-to-use-this-repository)
- [Future Improvements and Enhancements](#future-improvements-and-enhancements)

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
0. Create the database an inital table automatically.
1. Load the existing raw vehicle data into the bronze table using a SQL script.
2. Perform CRUD operations to manage the data (create, read, update, delete).
3. Use the ML module to predict vehicle prices based on input features.
4. Re-train the model with updated database records as needed.

---

## Tools and Techniques Utilized

### **Backend and database**
- **FastAPI**: Framework for building RESTful APIs.
- **PostgreSQL**: Database for storing vehicle records.
- **SQLAlchemy**: ORM for database interactions.

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
   - Integration of frontend (Streamlit) and backend (FastAPI) with a database.

2. **Machine Learning Lifecycle**:
   - From model construction on jupyter notebook to deployment with real-time predictions and re-training the model.
   - Handling preprocessing pipelines for the entire database and also for a single record, ensuring consistent encoding and scaling of features.

3. **Database Management**:
   - Efficient handling of relational data using PostgreSQL and SQLAlchemy.
   - Splitting raw data on a 'bronze' and preprocessed data ready to be consumed by the ML model on a 'gold' table

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

### 4. **Access the Application**
- **Frontend**: Visit `http://localhost:8501` for the Streamlit app.
- **Backend**: Access API documentation at `http://localhost:8000/docs`.
- **Database**: Use PgAdmin4 to access the PostgreSQL database:
  - Visit `http://localhost:5050`.
  - Log in with the credentials defined in your `docker-compose.yml`.
  - Add a new server connection:
    - **Host**: `host.docker.internal`
    - **Port**: `55432`
    - **Username**: (as defined in `docker-compose.yml`)
    - **Password**: (as defined in `docker-compose.yml`)
    - **Database**: `rusty_bargain` (or the database name you are using).
    - once logged in, run the file data/raw_data_loader.py to generate raw_car_data.sql
    - run raw_car_data.sql to populate the database


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

1. Automate initial sql script execution (raw_car_data.sql) - So when the application starts for the first time, the bronze table with raw data is already automatically populated
2. Create a streamlit tab for the ML part - re-training the model and getting predictions
3. Create detailed documentation using mkdocs
4. Create tests using pytest
5. Add more features to the Streamlit app - such as displaying the model's performance metrics and graphs
6. Automate creation of the 'gold' table and ML model training once the application is started for the first time
7. Allow filtering and sorting on the streamlit table with all the 300 thousand car records and improve layout