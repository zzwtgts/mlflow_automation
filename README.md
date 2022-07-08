# PROJECT INFORMATION

Classification Algorithm:         v1.0                                                  

Creation:                  04/22/2022                  

Author:                    Zheng Zhu                 


# DESCRIPTION

we present python code for training and deploying machine learning model.


# REQUIREMENTS

python3

numPy

sciPy

pandas

scikit-learn

featuretools

pickle

xgboost

json

requests

flask

seaborn

matplotlib


# USAGE

To train model and serialize the model into pickle file:

python3 main.py
 
To deploy the model on a server and make it available as a REST API in the form of a web:

python3 api.py

The client sends a request to the server, and then waits for a response before sending another request:

python3 request.py
