# This file is used to preprocess raw vehicle data into a format that can be used for training a machine learning model. 
# The functions in this file are used to preprocess the data 
# pipeline can be saved (currently inactivated)

import pandas as pd
import numpy as np
#import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MaxAbsScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

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

def handling_categoricals_label(df: pd.DataFrame):    
    categorical_cols = ['brand', 'model']
    le = LabelEncoder()
    for col in categorical_cols:
        df[f"{col}_encoded"] = le.fit_transform(df[col])
    df.drop(columns=['model', 'brand'], inplace=True)
    return df

def scaling_numericals(df: pd.DataFrame):
    numeric = ['registrationyear', 'power', 'mileage_censored', 'registrationmonth',  'numberofpictures', 'postalcode']
    scaler = MaxAbsScaler()
    scaler.fit(df[numeric])
    df[numeric] = scaler.transform(df[numeric])
    return df

def dropping_unnecessary_columns(df: pd.DataFrame):
    df.drop(columns=['datecrawled', 'mileage', 'datecreated', 'lastseen'], inplace=True)
    return df
    
class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = handling_date_formats(X)
        X = handling_missing_values(X)
        X = handling_outliers_mileage(X)
        X = handling_outliers_power_registrationyear(X)
        X = handling_categoricals_ohe(X)
        X = handling_categoricals_label(X)
        X = scaling_numericals(X)
        X = dropping_unnecessary_columns(X)
        return X

pipeline = Pipeline(steps=[('custom_transformer', CustomTransformer())])


# Save the pipeline
#joblib.dump(pipeline, 'preprocessing_pipeline.pkl')

# Load the pipeline
#loaded_pipeline = joblib.load('preprocessing_pipeline.pkl')

if __name__ == "__main__":
    data = {
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

    # Create the DataFrame
    df_single_row = pd.DataFrame(data)
    df_single_row.columns = df_single_row.columns.str.lower()

    processed_df = pipeline.fit_transform(df_single_row)
    pd.set_option('display.max_columns', None)
    print(processed_df)

    # issues
    # 1. scaler is not scaling the single value for prediction
    # 2. categorical variables not handled correctly for single value
     