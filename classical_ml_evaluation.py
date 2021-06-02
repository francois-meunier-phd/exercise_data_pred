from sklearn.ensemble import RandomForestRegressor
import numpy as np

#classical protocol for evaluating ML from preprocessd data
def protocol_classical_ML_predictor(complete_preprocessed_dataset, features_kept, regressor, information_on_travel):

    prediction_until_travel = []
    real_values = []
    information_on_travel_corrected = []
    i = 0
    for unavailable in complete_preprocessed_dataset:
        unavailable = unavailable[1]
        target_test = unavailable.demand
        features_test = unavailable[features_kept]
        if len(features_test) > 0:
            prediction = regressor.predict(features_test)
            prediction_until_travel.append(int(np.sum(prediction)))# + 0.5))# rounding value as result must be an integer
            real_values.append(np.sum(target_test))
            information_on_travel_corrected.append(information_on_travel[i])
        i = i + 1
        
    return real_values, prediction_until_travel, information_on_travel_corrected