# House Price Prediction

# Description

Housing Prices Prediction is an essential element for an economy. Analysis of price ranges influence both sellers and buyers.Our project is mainly focused on prediction of prices against explanatory features that cover many aspects of houses. Also, this project creates a Linear Regression model to estimate the price of the house accurately with the given features.

# To Whom

['ImmoEliza'](https://immoelissa.be/) wants Belgium's House Prediction model to find and analyse the sales in Belgium.

# Objective

Be able to apply a linear regression in a real context & preprocess data for Machine Learning.

# How it Works?

We have collected the previously scraped, pre-processed  and analysed data. We again analysed the data for null values, how to handle categorical data, which features to be considered using Feature selection process etc. Once the final data is available, we have formatted by dividing into traning set and test set for machine to learn. Then, we tranined the model using machine learning algorithm which in this case is Linear Regression. 



<img src="https://github.com/FrancescoMariottini/Belgium-prices-prediction/blob/manasa/assets/images/flowchart.png" width="700" height="400">




1. Data Pre-processing and Cleaning
2. Feature Engineeing and Feature Selection
3. Linear Regression Model 
4. Evaluation
5. Inferences

#### Data Pre-processing and Cleaning"
Originally all object values were converted into numerical (through aggregated values) but then kept as object to allow easier filtering within "Feature Engineeing and Feature Selection" module.

##### Steps performed:
1. Aggregated parameter columns created for categorical values and for facades number (based on building subtype). 
2. Filling Not_a_Number with zeros
3. Outliers identification using Tukey fences due right-skewed distribution

Postcode was replaced by median price obtained from the official belgian statistics in a dedicated dataset (see data folder).

#### Feature Engineeing and Feature Selection

##### Steps performed:

1. Removed the features where the data was missing and irrelevant . 
2. Feature selection was done mostly using the Chi-squared contingency method which gives the list of features that are irrelevant for the model , and can be     
   removed from the dataframe. 
3. Utilising the pandas get_dummies class for one hot encoding on all the categorical columns to be used in the model.

#### Linear Regression Model application

We have started with ordinary least squares(OLS) using scikit's Linear Regression class on the dataset and observed that results are not so bad.Later tried applying polynomial regrssion using 5-fold cross-validation with degree 2 was better than linear regression (degree 1
) but was worse for degree 3 and higher. Then, we cleaned the data again with more features and applied polynomial regression with degree 2 itself. It is observed that for this dataset, simple linear regression is the best choise and we have applied.

#### Evaluation

Model evaluation is an essential part in machine learning process. It describes how well the model is performing in its predictions. Evaluation metrics changes according to the problem definition. The errors represents the variation of faults in its predictions. Thus, it becomes important to compare actual target with the predicted one. 

We have applied Regression metrics like Mean Absolute Error, Mean Squared Error, Mean Absolute Percentage Error and R-squared. R-squared is a statistical measure of how close the data to the fitted line. The higher the R-squared, the better the model fits the data. 


#### Inferences
1. Could have more real statistical data and new features like construction year.
2. Feature selection also plays important role in deciding the most prominent features to increase the accuracy.
3. Better correlation found using a subset but no time to explore.


#### Date of Completion:
24-11-2020


# Team:
* [Francesco](https://be.linkedin.com/in/francescomariottini)<br>
* [Joachim](https://www.linkedin.com/in/jokotek/)<br>
* [Ankita](linkedin.com/in/ankitahaldia)<br>
* [Manasa](linkedin.com/in/manasanoolu)

