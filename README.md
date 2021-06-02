## General Info
***
People reading this documentation are assumed to have already seen the presentation of this work/challenge.
We will simply explain our approach, things that have worked and others not.
Needed libraies are in requirements.txt.
To make everything work, go to a location where you can get the code :
```
$ git clone git@github.com:francois-meunier-phd/exercise_data_pred.git
$ cd exercise_data_pred
```
If you want, it is possible (but not necessary in this case) to create a new environement :
```
$ py -m pip install --user virtualenv
$ py -m venv env
$ .\env\Scripts\activate
```
Then, required packages to run the code :
```
$ pip install -r requirements
```
For conveniance (and because of lack of time if the 4 to 8 hours of challenge are respected) : the code is in the main jupyter notebook called "global_main.ipynb", and calls separate external files for functions that can be factorized.
A next step of integration would be indeed to create a clean package that would be easily transportable and reused for pre-prod goals.
Data need to be in a directory called "dataset" at the root of the repo.

## Classical Machine Learning approach
### Data pretreament
***
When using ML approaches, it is necessary to clearly define input features and target.
In our case, the global target (ie summed demand on all remaining days) may not be the target of a classical predictor, as if inputs features are all the available data for a day N, then the output would simply be the demand for day N. A final sum will be necessary to get the expected output.
Then, our first proposition relies on the prediction of the Nth day using all its available features.
Then the target is easily defined as demand, and the input features all the others.

### Features preprocessing
***
As we expect to use trees, scaling of features is not necessary.
Several classical steps have been realized for features pretreatment, and the main ones are :
1. convertion to float types when possible
2. one hot encoder for categories
3. trigonometry transformation for cyclic features (components extracted from dates like day of the month).

Moreover, it seems thta some data would need a bit more clearing, as for example

### Experimentation on validation set
***
When launching the protocol, we get following results :
 * We propose MAE, RMSE and R2 to have an idea of our performances; however, with no information on the preferences of he business in terms of prediction gap acceptance, we focused on MAE, which in more neutral in regression; moreover, a standard deviation on the MAE allows to see the stability of the model.
 * Grid search approach for tuning algorithms is useless in our case, as performances remained the same.
 * Features preprocessing appears to not improve performances, and so seeem to be not necessary with this model.

With the final computed sum (on all days before departure) :
 * On the sum for all remaining days to predict on, MAE was around 35, but this isn't a good way to evaluate in this case as some sums are done on 90 days, and others on 1 day. departure); further studie would need to compare between equivalent number of remaining days. 

The use of Random Forests regressor and Gradient boosting showed that these approaches give similar perfomances.

## Deep learning approach
In this context, deep learning has a reason to be used when time series are considered. However, it is not possible to implement it when the prediction has to be done at day -90, as we don't have, in this case, an history od the current time series. That's why this set of methods could only be used from day -60 (in our task of prediction).
### Choice of structure
***
When facing time series prediction, the two most appropriated neural networks are GRU and LSTM. The main difference is the number of parameters to tune in each neuron of their networks, as LSTM have 3 and GRU 2. With the forget parameter, LSTM should be able to deal with longer sequences than GRU. With the great number of data we face, we proposed to try LSTM as a prediction problem. 
This may be reconsidered with further studies.

### Approach proposed
***
LSTM for prediction needs sequential data, where the input is made of one or several time series, and the output is a vector of targets.
In this case, we tried an network thta took as input the prices of the last 14 days (fixed training window), and as output the demand of the 14th day.
The network is made of a 100 neurons LSTM layer and a 100 neurons linear layer, which was experimentally well performing on equivalent tasks.


### First results
***
Performances do not follow our expectations, and therefore were not carried until full validation : indeed, no convergence was seen on our tests. This can be explained with the fact that the selected batch size needed to be short enough for the available computation power for this exercice.

## Conclusion
During the few hours spent on this project, we were able to propose a first pipeline for predicting the remaning demand in the future. Although the deep learning approach failed (and more time and computation power would coorect its problems), the classical ML approach seemed to give quite good results.
