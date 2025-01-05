

# button 1 - Preprocess data  -> hits the backend endpoint - calls the pre-processing pipeline
# button 2 - train model -> hits the backend endpoint - calls the training pipeline

import streamlit as st
import requests
import pandas as pd
from crud.schemas import FueltypeBase, VehicleTypeBase, GearboxBase
from st_aggrid import AgGrid, GridOptionsBuilder


# variables to access Enum values from schemas
vehicle_types = [vehicle.value for vehicle in VehicleTypeBase]
fuel_types = [fuel.value for fuel in FueltypeBase]
gearbox_types = [gearbox.value for gearbox in GearboxBase]

st.set_page_config(layout="wide")

#st.image("/frontend/logo2.jpg", width=200)

st.title("Rusty Bargain - The best car bang for your buck!")

tabs = st.tabs(["Vehicle Database","ML Model"])

# Auxiliary function to display detailed error messages
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operation successfull!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # Se o erro for uma lista, extraia as mensagens de cada erro
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Error: {errors}")
                else:
                    # Caso contrário, mostre a mensagem de erro diretamente
                    st.error(f"Error: {data['detail']}")
        except ValueError:
            st.error("Unknown error. Could not decode the response.")

# Tab 1 - Vehicle database
with tabs[0]:
    # Add vehicle
    with st.expander("Add a new vehicle"):
        with st.form("new_vehicle"):
            datecrawled = st.date_input("Enter the date when this vehicle was found", value='today', format='YYYY/MM/DD')
            price = st.number_input('Enter the current price', min_value=0, value=None)
            vehicletype = st.selectbox("Select a vehicle type", options=vehicle_types)
            gearboxtype = st.selectbox("Select a gearbox type", options=gearbox_types)
            fueltype = st.selectbox("Select a fuel type", options=fuel_types)
            power = st.number_input("Enter the vehicle's horsepower", min_value=0, value=None)
            model = st.text_input("Enter the vehicle's model")
            mileage = st.number_input("Enter the vehicle's mileage", min_value=0, value=None)
            registrationmonth = st.number_input("Enter the month when the vehicle was registered",min_value=0, max_value=12, value=None)
            registrationyear = st.number_input("Enter the year when the vehicle was registered (YYYY)", min_value=1950, value=None)
            brand = st.text_input("Enter the vehicle's brand")
            notrepaired = st.selectbox("This vehicle has never been repaired",[None, "yes", "no"])
            datecreated = st.date_input("Enter the date when this vehicle was registered on our system", value='today', format='YYYY/MM/DD')
            numberofpictures = st.number_input("How many good quality pictures do we for this vehicle?", min_value=0, value=None)
            postalcode = st.number_input("Which zipcode is the vehicle parked at?", min_value=10000, value=None)
            lastseen = st.date_input("Enter the date we last saw this vehicle")

            submit_button = st.form_submit_button("Add vehicle")

            if submit_button:
                response = requests.post(
                    "http://backend:8000/vehicles/",
                    json={
                        "datecrawled": datecrawled.isoformat() if datecrawled else None,
                        "price": price,
                        "vehicletype": vehicletype,
                        "gearbox": gearboxtype,
                        "power": power,
                        "model": model,
                        "mileage": mileage,
                        "registrationmonth": registrationmonth,
                        "registrationyear": registrationyear,
                        "fueltype": fueltype,
                        "brand": brand,
                        "notrepaired": notrepaired,
                        "datecreated": datecreated.isoformat() if datecreated else None,
                        "numberofpictures": numberofpictures,
                        "postalcode": postalcode,
                        "lastseen": lastseen.isoformat() if lastseen else None,
                    },
                )
                show_response_message(response)


    # View vehicles
    with st.expander("View Vehicles"):
        # Use session state to store the DataFrame
        if "vehicle_data" not in st.session_state:
            st.session_state.vehicle_data = None

        if st.button("Show all Vehicles"):
            response = requests.get("http://backend:8000/vehicles/")
            if response.status_code == 200:
                vehicle = response.json()
                df = pd.DataFrame(vehicle)

                df = df[
                    [
                        "datecrawled",
                        "price",
                        "vehicletype",
                        "gearbox",
                        "power",
                        "model",
                        "mileage",
                        "registrationmonth",
                        "registrationyear",
                        "fueltype",
                        "brand",
                        "notrepaired",
                        "datecreated",
                        "numberofpictures",
                        "postalcode",
                        "lastseen",
                    ]
                ]

                # Store the data in session state
                st.session_state.vehicle_data = df
            else:
                show_response_message(response)

        # Check if data is available in session state
        if st.session_state.vehicle_data is not None:
            df = st.session_state.vehicle_data

            # Configure the AgGrid table
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(editable=True, filter=True, sortable=True, resizable=True)
            gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)
            gb.configure_side_bar()  # Enable a sidebar for filtering
            grid_options = gb.build()

            # Display the AgGrid table
            response = AgGrid(
                df,
                gridOptions=grid_options,
                height=600,
                fit_columns_on_grid_load=True,
                enable_enterprise_modules=False
            )


    # Get details from one vehicle
    with st.expander("Get Vehicle Details"):
        get_id = st.number_input("Vehicle ID", min_value=1, format="%d")
        if st.button("Search Vehicle"):
            response = requests.get(f"http://backend:8000/vehicles/{get_id}")
            if response.status_code == 200:
                vehicle = response.json()
                df = pd.DataFrame([vehicle])

                df = df[
                    [
                        "datecrawled",
                        "price",
                        "vehicletype",
                        "gearbox",
                        "power",
                        "model",
                        "mileage",
                        "registrationmonth",
                        "registrationyear",
                        "fueltype",
                        "brand",
                        "notrepaired",
                        "datecreated",
                        "numberofpictures",
                        "postalcode",
                        "lastseen",
                    ]
                ]

                # Configure the AgGrid table
                gb = GridOptionsBuilder.from_dataframe(df)
                gb.configure_default_column(editable=True, filter=True, sortable=True, resizable=True)
                gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)
                gb.configure_side_bar()  # Enable a sidebar for filtering
                grid_options = gb.build()

                # Display the AgGrid table
                response = AgGrid(
                    df,
                    gridOptions=grid_options,
                    height=600,
                    fit_columns_on_grid_load=True,
                    enable_enterprise_modules=False
                )
                # Show DataFrame without index
                #st.write(df.to_html(index=False), unsafe_allow_html=True)
            else:
                show_response_message(response)

    # Delete Vehicle
    with st.expander("Delete Vehicle"):
        delete_id = st.number_input("ID of Vehicle to be deleted", min_value=1, format="%d")
        if st.button("Delete Vehicle"):
            response = requests.delete(f"http://backend:8000/vehicles/{delete_id}")
            show_response_message(response)

    # Update Vehicle old
    # with st.expander("Update Vehicle old"):
    #     with st.form("update_vehicle old"):
    #         update_id = st.number_input("Vehicle ID", min_value=1, format="%d")
    #         new_datecrawled = st.date_input("Enter the date when this vehicle was found", value='today', format='YYYY/MM/DD')
    #         new_price = st.number_input('Enter the current price')
    #         new_vehicletype = st.selectbox("Select a vehicle type", options=vehicle_types)
    #         new_gearboxtype = st.selectbox("Select a gearbox type", options=gearbox_types)
    #         new_fueltype = st.selectbox("Select a fuel type", options=fuel_types)
    #         new_power = st.number_input("Enter the vehicle's horsepower")
    #         new_model = st.text_area("Enter the vehicle's model")
    #         new_mileage = st.number_input("Enter the vehicle's mileage")
    #         new_registrationmonth = st.number_input("Enter the month when the vehicle was registered",min_value=0, max_value=12)
    #         new_registrationyear = st.number_input("Enter the month when the vehicle was registered (YYYY)")
    #         new_brand = st.text_area("Enter the vehicle's brand")
    #         new_notrepaired = st.selectbox("This vehicle has never been repaired",[None, "yes", "no"])
    #         new_datecreated = st.date_input("Enter the date when this vehicle was registered on our system", value='today', format='YYYY/MM/DD')
    #         new_numberofpictures = st.number_input("How many good quality pictures do we for this vehicle?")
    #         new_postalcode = st.number_input("Which zipcode is the vehicle parked at?")
    #         new_lastseen = st.date_input("Enter the date we last saw this vehicle")

    #         update_button = st.form_submit_button("Update Vehicle")

    #         if update_button:
    #             update_data = {}
    #             if new_datecrawled:
    #                 update_data["datecrawled"] = new_datecrawled
    #             if new_price:
    #                 update_data["price"] = new_price
    #             if new_vehicletype:
    #                 update_data["vehicletype"] = new_vehicletype
    #             if new_gearboxtype:
    #                 update_data["gearbox"] = new_gearboxtype
    #             if new_fueltype:
    #                 update_data["fueltype"] = new_fueltype
    #             if new_power:
    #                 update_data["power"] = new_power
    #             if new_model:
    #                 update_data["model"] = new_model
    #             if new_mileage:
    #                 update_data["mileage"] = new_mileage
    #             if new_registrationmonth:
    #                 update_data["registrationmonth"] = new_registrationmonth
    #             if new_registrationyear:
    #                 update_data["registrationyear"] = new_registrationyear
    #             if new_brand:
    #                 update_data["brand"] = new_brand
    #             if new_notrepaired:
    #                 update_data["notrepaired"] = new_notrepaired
    #             if new_datecreated:
    #                 update_data["datecreated"] = new_datecreated
    #             if new_numberofpictures:
    #                 update_data["numberofpictures"] = new_numberofpictures
    #             if new_postalcode:
    #                 update_data["postalcode"] = new_postalcode
    #             if lastseen:
    #                 update_data["lastseen"] = lastseen

    #             if update_data:
    #                 response = requests.put(
    #                     f"http://backend:8000/vehicles/{update_id}", json=update_data
    #                 )
    #                 show_response_message(response)
    #             else:
    #                 st.error("No information provided for update")

    # Update Vehicle new
    with st.expander("Update Vehicle"):
        # Step 1: Input the Vehicle ID
        vehicle_id = st.number_input("Enter Vehicle ID to Load Data", min_value=1, format="%d")
        load_button = st.button("Load Vehicle Data")

        # Initialize vehicle_data in Streamlit session state
        if "vehicle_data" not in st.session_state:
            st.session_state.vehicle_data = None

        if load_button:
            # Fetch the existing data from the backend
            try:
                response = requests.get(f"http://backend:8000/vehicles/{vehicle_id}")
                if response.status_code == 200:
                    st.session_state.vehicle_data = response.json()  # Store data in session state
                    st.success("Vehicle data loaded successfully!")
                else:
                    st.error("Failed to load vehicle data. Check the Vehicle ID.")
                    st.session_state.vehicle_data = None
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching vehicle data: {e}")
                st.session_state.vehicle_data = None

        # Step 2: Populate the form if vehicle data is available
        if st.session_state.vehicle_data is not None and not st.session_state.vehicle_data.empty:
            vehicle_data = st.session_state.vehicle_data  # Retrieve data from session state

            with st.form("update_vehicle"):
                # Populate fields with existing data
                new_datecrawled = st.date_input(
                    "Enter the date when this vehicle was found",
                    value=vehicle_data.get("datecrawled", None)
                )
                new_price = st.number_input(
                    "Enter the current price",
                    value=vehicle_data.get("price", 0.0)
                )
                new_vehicletype = st.selectbox(
                    "Select a vehicle type",
                    options=vehicle_types,
                    index=vehicle_types.index(vehicle_data.get("vehicletype", vehicle_types[0]))
                )
                new_gearboxtype = st.selectbox(
                    "Select a gearbox type",
                    options=gearbox_types,
                    index=gearbox_types.index(vehicle_data.get("gearbox", gearbox_types[0]))
                )
                new_fueltype = st.selectbox(
                    "Select a fuel type",
                    options=fuel_types,
                    index=fuel_types.index(vehicle_data.get("fueltype", fuel_types[0]))
                )
                new_power = st.number_input(
                    "Enter the vehicle's horsepower",
                    value=vehicle_data.get("power", 0)
                )
                new_model = st.text_area(
                    "Enter the vehicle's model",
                    value=vehicle_data.get("model", "")
                )
                new_mileage = st.number_input(
                    "Enter the vehicle's mileage",
                    value=vehicle_data.get("mileage", 0)
                )
                new_registrationmonth = st.number_input(
                    "Enter the month when the vehicle was registered",
                    min_value=0, max_value=12,
                    value=vehicle_data.get("registrationmonth", 0)
                )
                new_registrationyear = st.number_input(
                    "Enter the year when the vehicle was registered (YYYY)",
                    value=vehicle_data.get("registrationyear", 0)
                )
                new_brand = st.text_area(
                    "Enter the vehicle's brand",
                    value=vehicle_data.get("brand", "")
                )
                new_notrepaired = st.selectbox(
                    "This vehicle has never been repaired",
                    options=[None, "yes", "no"],
                    index=[None, "yes", "no"].index(vehicle_data.get("notrepaired", None))
                )
                new_datecreated = st.date_input(
                    "Enter the date when this vehicle was registered on our system",
                    value=vehicle_data.get("datecreated", None)
                )
                new_numberofpictures = st.number_input(
                    "How many good quality pictures do we have for this vehicle?",
                    value=vehicle_data.get("numberofpictures", 0)
                )
                new_postalcode = st.number_input(
                    "Which zipcode is the vehicle parked at?",
                    value=vehicle_data.get("postalcode", 0)
                )
                new_lastseen = st.date_input(
                    "Enter the date we last saw this vehicle",
                    value=vehicle_data.get("lastseen", None)
                )

                # Update button
                update_button = st.form_submit_button("Update Vehicle")

                if update_button:
                    # Prepare the updated data
                    update_data = {
                        "datecrawled": new_datecrawled.isoformat() if new_datecrawled else None,
                        "price": new_price,
                        "vehicletype": new_vehicletype,
                        "gearbox": new_gearboxtype,
                        "fueltype": new_fueltype,
                        "power": new_power,
                        "model": new_model,
                        "mileage": new_mileage,
                        "registrationmonth": new_registrationmonth,
                        "registrationyear": new_registrationyear,
                        "brand": new_brand,
                        "notrepaired": new_notrepaired,
                        "datecreated": new_datecreated.isoformat() if new_datecreated else None,
                        "numberofpictures": new_numberofpictures,
                        "postalcode": new_postalcode,
                        "lastseen": new_lastseen.isoformat() if new_lastseen else None,
                    }

                    try:
                        # Send updated data to the backend
                        response = requests.put(
                            f"http://backend:8000/vehicles/{vehicle_id}",
                            json=update_data
                        )
                        if response.status_code == 200:
                            st.success("Vehicle updated successfully!")
                        else:
                            st.error(f"Failed to update vehicle. Error: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error updating vehicle. Error: {e}")

# Tab 2 - ML Model
with tabs[1]:
    st.header("ML Model")
    st.write("This section will handle vehicle price predictions and model retraining.")

   # Add model training / retraining functionality
    with st.expander("Train/Re-train Model"):
        if st.button("Start (re)training model"):
                try:

                    # request 1 - preprocess raw data
                    response = requests.get("http://backend:8000/preprocessdata")
                    if response.status_code == 200:
                        st.success("Model Data Preprocessing sucessful!")
                        
                        # request 2 - load preprocessed data into gold table
                        response = requests.get("http://backend:8000/load_preprocessed_dataset")
                        if response.status_code == 200:
                            st.success("Model Data Loaded!")

                            # request 3 - train the model
                            response = requests.get("http://backend:8000/train_model")
                            if response.status_code == 200:
                                st.success("Model Trained!")
                            
                                # request 4 - load the model
                                response = requests.get("http://backend:8000/load_model")
                                if response.status_code == 200:
                                    st.success("Model Loaded!")
                                else:
                                    st.error(f"Failed to load the model. Error: {response.text}")        
                            else:
                                st.error(f"Failed to train the model. Error: {response.text}")        
                        else:
                            st.error(f"Failed to load model data. Error: {response.text}")        
                    else:
                            st.error(f"Failed to preprocess model data. Error: {response.text}")    
                except requests.exceptions.RequestException as e:
                    show_response_message(response)
                    st.error(f"Error training the model: {e}")

    # Add inputs for vehicle price prediction
    with st.expander("Predict Vehicle Price"):
        with st.form("predict_price"):
            st.subheader("Predict Vehicle Price")
            # input fields
            predict_datecrawled = st.date_input("Enter the date when this vehicle was found", value='today', format='YYYY/MM/DD')
            predict_vehicletype = st.selectbox("Select a vehicle type", options=vehicle_types)
            predict_gearboxtype = st.selectbox("Select a gearbox type", options=gearbox_types)
            predict_fueltype = st.selectbox("Select a fuel type", options=fuel_types)
            predict_power = st.number_input("Enter the vehicle's horsepower", min_value=0, value=None)
            predict_model = st.text_input("Enter the vehicle's model")
            predict_mileage = st.number_input("Enter the vehicle's mileage", min_value=0, value=None)
            predict_registrationmonth = st.number_input("Enter the month when the vehicle was registered",min_value=0, max_value=12, value=None)
            predict_registrationyear = st.number_input("Enter the year when the vehicle was registered (YYYY)", min_value=1950, value=None)
            predict_brand = st.text_input("Enter the vehicle's brand")
            predict_notrepaired = st.selectbox("This vehicle has never been repaired",[None, "yes", "no"])
            predict_datecreated = st.date_input("Enter the date when this vehicle was registered on our system", value='today', format='YYYY/MM/DD')
            predict_numberofpictures = st.number_input("How many good quality pictures do we for this vehicle?", min_value=0, value=None)
            predict_postalcode = st.number_input("Which zipcode is the vehicle parked at?", min_value=10000, value=None)
            predict_lastseen = st.date_input("Enter the date we last saw this vehicle")

            predict_button = st.form_submit_button("Predict Price")
            if predict_button:
                try:
                    response = requests.post(
                        f"http://backend:8000/predict_price",
                        json=[{
                            "datecrawled": predict_datecrawled.isoformat() if datecrawled else None,
                            "vehicletype": predict_vehicletype,
                            "gearbox": predict_gearboxtype,
                            "power": predict_power,
                            "model": predict_model,
                            "mileage": predict_mileage,
                            "registrationmonth": predict_registrationmonth,
                            "registrationyear": predict_registrationyear,
                            "fueltype": predict_fueltype,
                            "brand": predict_brand,
                            "notrepaired": predict_notrepaired,
                            "datecreated": predict_datecreated.isoformat() if datecreated else None,
                            "numberofpictures": predict_numberofpictures,
                            "postalcode": predict_postalcode,
                            "lastseen": predict_lastseen.isoformat() if lastseen else None,
                        }],
                    )
                    if response.status_code == 200:
                        st.success(response.text)
                    else:
                        st.error(f"Error generating prediction. Error: {response.text}")
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"Error generating prediction: {e}")