import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import OneHotEncoder

def splitting_travels(df, fewer_static_features):
    
    grouped = df.groupby(fewer_static_features)
    dataframes = [group for _, group in grouped]
    
    return dataframes


def extraction_validation_set(dataset_test, days_to_be_used):
    complete_preprocessed_dataset = []; information_on_travel = []
    for i in tqdm(range(len(dataset_test))):
        df_current = dataset_test[i]
        for current_day in days_to_be_used:
            available_part = df_current[df_current.sale_day_x + 1 <= current_day]
            unavailable_part = df_current[df_current.sale_day_x + 1 > current_day]
            complete_preprocessed_dataset.append([available_part, unavailable_part])
            information_on_travel.append([df_current.sale_day_x, df_current.departure_date, df_current.origin_station_name, df_current.destination_station_name])
    
    return complete_preprocessed_dataset, information_on_travel


def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop([feature_to_encode], axis=1)
    return(res)

def cyclic_features_transform(features, periodic_features_day, periodic_features_month):

    for col in periodic_features_day:
        features[col+"_sin"] = np.sin(features[col]*(2.*np.pi/31))
        features[col+"_cos"] = np.cos(features[col]*(2.*np.pi/31))
    for col in periodic_features_month:
        features[col+"_sin"] = np.sin(features[col]*(2.*np.pi/12))
        features[col+"_cos"] = np.cos(features[col]*(2.*np.pi/12))
    
    return features

def create_inout_sequences(input_data, tw):
    inout_seq = []
    for df in tqdm(input_data):
        L = len(df)
        for i in range(L-tw):
            train_seq = df.iloc[i:i+tw]["scaled_price"]
            train_label = df.iloc[i+tw:i+tw+1]["scaled_demand"]
            inout_seq.append((train_seq, train_label))
    return inout_seq

def create_inout_sequences_validation(input_data, tw):
    input_data["scaled_price"] = scaler_price.transform(np.array(input_data.price).reshape(-1, 1))
    inout_seq = []; real_target = []
    L = len(input_data)
    for i in range(L-tw):
        val_seq = input_data.iloc[i:i+tw]["scaled_price"]
        inout_seq.append(val_seq)
        real_target.append(input_data.iloc[i+tw]["demand"])
    return inout_seq, real_target