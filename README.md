# Restaurant_Rating_Prediction

The Objective of this project is to predict the ratings of the restaurants.

# A little explanation of dataset :
```
1.The dataset which im using here is zomato dataset of Bangalore city
2.Bangalore city is the IT capital of india, So most of the people in bangalore will dont have time to
cook the food for themselves.
3.So their is high demand for the restaurants.
4.Restaurants which are newly established and connect with zomato cannot compete with the restaurants which are already established and have good market value.
5.Considering the above problem i need to find some features which has effect on the ratings.
6.So that i can create a UI which gives the newly restaurants as well as old restaurants a chance to 
serve their customers based on their ratings.
```
# Installation Requirements:

```
1. pandas
2. numpy
3. flask
4. matplotlib
5. seaborn
6. evidently
7. gunicorn
```
# Tools used:

```
1. Vs code
2. Jupyter Notebook
3. GitHub
4. Heroku
5. Docker
```
# Flow of Pipeline


```
1.Data Ingestion
2.Data Validation
3.Data Transformation
4.Model Training 
5.Model evaluation
6.Model push
```


## Data Ingestion of zomato:
```
Steps:
1. Ingest the data into our local system by url.
2. The data file is zip file
3. Extracting the zip file, contains zomato.csv file within it.
4. Saving the data in the raw format.
5. Splitting the data into train and test by StratifiedShuffle split technique.
6. Saving the data into ingested dir, naming them as train and test.
```

## Data Validation of zomato:
```
Steps :

1.Doing EDA (Exploratory Data Analysis)
2.Outliers check
3.Data Drift check
4.Checking dtypes of each column
5.Checking NaN values
6.Schema validation
7.Column name check
8.Describing the numerical and categorical data
9.Knowing mean,median mode of the data
10.Visualizing the data
11.Finding Co-relation of each column
12.Knowing Independent features and dependent or target feature.
```

## Data Tranformation of zomato:
```
Steps:

1.Doing Feature Engineering
2.Filling NaN values
3.Removig Outliers
4.Removing unrelated features
5.Adding features 
6.Changing the dtypes of the data according to it.
7.Creating Pipeline of numerical and categorical features
8.Creating a data transformer object
9.Serializing the object into a file to automate the feature engineering
10.Storing the object file into a specific directory..
```

## Model Training of zomato:
```
Steps:

1.Initializing the models
2.Making comparison of the models
3.Perform Hyper-parameter tuning by GridSearchCV 
4.Selecting the best model based upon desired accuracy
5.Creating a model object
6.Serializing the model object into a file.
7.Storing the file into a specific directory
```

## Model Evaluation of zomato:
```
Steps:

1.At this stage we again train a new model
2.We compare the training model with the best model which is already in production
3.We conclude the training model as best model only when it is better than the already trained model.
4.If not we consider the old model as best model
5.Store the best model in specific directory after serializing the model. 
```

## Model Push:
```
Steps:

1.We maintain a best model which is used for prediction 
```

