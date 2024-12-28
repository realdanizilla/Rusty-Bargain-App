# This file is used to preprocess raw vehicle data from postgres database into a 
# format that can be used for training a machine learning model. 
# The functions in this file are used to preprocess the data 
# data pipeline can be saved (currently inactivated)

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MaxAbsScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from database.database import engine


# Pipeline functions
def column_name_cleaning(df: pd.DataFrame):
    df.columns = df.columns.str.lower()
    return df

def handling_date_formats(df: pd.DataFrame):
    df['datecrawled'] = pd.to_datetime(df['datecrawled'],format='%d/%m/%Y %H:%M')
    df['datecreated'] = pd.to_datetime(df['datecreated'],format='%d/%m/%Y %H:%M')
    df['lastseen'] = pd.to_datetime(df['lastseen'],format='%d/%m/%Y %H:%M')
    return df
    
def handling_missing_values(df: pd.DataFrame):
    df['vehicletype'] = df["vehicletype"].fillna('unknown')
    df['gearbox'] = df["gearbox"].fillna('unknown')
    df['model'] = df["model"].fillna('unknown')
    df['fueltype'] = df["fueltype"].fillna('unknown')
    df['notrepaired'] = df["notrepaired"].fillna('unknown')
    return df

    # handling outliers
def handling_outliers_mileage(df: pd.DataFrame):
    mileage = df["mileage"].values
    ## Calculate the quartiles
    mileageQ1 = np.percentile(mileage, 25)
    mileageQ3 = np.percentile(mileage, 75)
    ## Calculate the IQR
    mileageIQR = mileageQ3 - mileageQ1
    ## Calculate the whisker values
    lower_whisker = mileageQ1 - 1.5 * mileageIQR
    mileage_censored = np.where(mileage < lower_whisker, lower_whisker, mileage)
    df["mileage_censored"] = mileage_censored
    return df

def handling_outliers_power_registrationyear(df: pd.DataFrame):
    # power and registration year
    power = df["power"].values
    regyear = df["registrationyear"].values
    
    # calculating thresholds
    threshold1 = np.mean(power) + 3 * np.std(power)
    threshold2 = np.mean(regyear) + 3 * np.std(regyear)

    # Getting indexes for outliers in each column
    outlier_indices1 = np.where(power > threshold1)[0]
    outlier_indices2 = np.where(regyear > threshold2)[0]

    # Combining outlier indexes from both columns
    outlier_indices = np.union1d(outlier_indices1, outlier_indices2)
    # removing records corresponding to the indexes
    df = df.drop(df.index[outlier_indices])
    return df

def handling_categoricals_ohe(df: pd.DataFrame):
    df = pd.get_dummies(df, columns=['gearbox', 'fueltype', 'notrepaired', 'vehicletype'],dtype=int)
    return df

def handling_categoricals_label(df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
    """
    Fit the label encoder on the categorical columns if fit is True,
    otherwise transform the DataFrame using the fitted label encoder.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the categorical columns to encode.
    fit (bool): If True, fit the label encoder; if False, transform the DataFrame.
    
    Returns:
    pd.DataFrame: The DataFrame with encoded columns and original columns dropped.
    """
    categorical_cols = ['brand', 'model']
    
    if fit:
        # Fit the label encoder and save it
        le = LabelEncoder()
        for col in categorical_cols:
            df[f"{col}_encoded"] = le.fit_transform(df[col])
            joblib.dump(le, f'label_encoder_{col}.pkl')
    else:
        # Apply label encoding to the categorical columns
        for col in categorical_cols:
            # Load the fitted label encoder
            le = joblib.load(f'label_encoder_{col}.pkl')
            if col in df.columns:
                df[f"{col}_encoded"] = le.transform(df[col])
    
    # Drop the original categorical columns
    df.drop(columns=categorical_cols, inplace=True, errors='ignore')
    
    return df  

def scaling_numericals(df: pd.DataFrame, fit: bool = False):
    numeric = ['registrationyear', 'power', 'mileage_censored', 'registrationmonth',  'numberofpictures', 'postalcode']
    if fit:
        scaler = MaxAbsScaler()
        scaler.fit(df[numeric])
        joblib.dump(scaler, 'scaler.pkl')
        df[numeric] = scaler.transform(df[numeric])
    else:
        scaler = joblib.load('scaler.pkl')
        df[numeric] = scaler.transform(df[numeric])
    return df

def dropping_unnecessary_columns(df: pd.DataFrame):
    df.drop(columns=['datecrawled', 'mileage', 'datecreated', 'lastseen'], inplace=True)
    return df

# transformer class for the entire dataset
class CustomTransformerDataset(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = column_name_cleaning(X)
        X = handling_date_formats(X)
        X = handling_missing_values(X)
        X = handling_outliers_mileage(X)
        X = handling_outliers_power_registrationyear(X)
        X = handling_categoricals_ohe(X)
        X = handling_categoricals_label(X, True)
        X = scaling_numericals(X, True)
        X = dropping_unnecessary_columns(X)
        return X

# transformer class for a single record
class CustomTransformerSingle(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.le = None
        self.scaler = None

    def fit(self, X, y=None):
        return self
    
    # def load_label_encoder_brand(self):
    #     self.le = joblib.load('label_encoder_brand.pkl')
    #     return self.le

    # def load_scaler(self):
    #     self.scaler = joblib.load('scaler.pkl')
    #     return self.scaler

    def transform(self, X):
        # if self.le is None:
        #     self.load_label_encoder()
        # if self.scaler is None:
        #     self.load_scaler()

        X = column_name_cleaning(X)
        X = handling_date_formats(X)
        X = handling_missing_values(X)
        X = handling_outliers_mileage(X)
        X = handling_outliers_power_registrationyear(X)
        X = handling_categoricals_ohe(X)
        X = handling_categoricals_label(X, False)
        X = scaling_numericals(X, False)
        X = dropping_unnecessary_columns(X)
        return X

pipeline_dataset = Pipeline(steps=[('custom_transformer', CustomTransformerDataset())])

pipeline_single = Pipeline(steps=[('custom_transformer', CustomTransformerSingle())])



# Save the pipeline
#joblib.dump(pipeline, 'preprocessing_pipeline.pkl')

# Load the pipeline
#loaded_pipeline = joblib.load('preprocessing_pipeline.pkl')

if __name__ == "__main__":
    query = 'SELECT * FROM car_data'
    data_df = pd.read_sql(query,engine)
    #data = pd.read_csv('../data/car_data.csv')
    processed_df = pipeline_dataset.fit_transform(data_df)
    processed_df.to_csv('../data/processed_data.csv', index=False)
    
    # sample data for testing
    data_single = {
    'DateCrawled': ['24/03/2016 11:52'],
    'Price': [480],
    'VehicleType': [None],  # Assuming empty value is represented as None
    'RegistrationYear': [1993],
    'Gearbox': ['manual'],
    'Power': [0],
    'Model': ['golf'],
    'Mileage': [150000],
    'RegistrationMonth': [0],
    'FuelType': ['petrol'],
    'Brand': ['volkswagen'],
    'NotRepaired': [None],  # Assuming empty value is represented as None
    'DateCreated': ['24/03/2016 00:00'],
    'NumberOfPictures': [0],
    'PostalCode': [70435],
    'LastSeen': ['07/04/2016 03:16']
}
    
    # Create the DataFrame for single record
    df_single_row = pd.DataFrame(data_single)
    df_single_row.columns = df_single_row.columns.str.lower()
    processed_df_single = pipeline_single.fit_transform(df_single_row)
    processed_df_single.to_csv('../data/processed_data_single.csv', index=False)
