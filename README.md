# Insurance-Database-Systems
DS-GA 2433: Database Systems Final Project

## Summary

This project contains the full stack for a health insurance company. The goal of this application is to provide quotes for the health insurance plans that the company offers after a customer provides some personal and medical information. The stack includes a public webpage that a customer uses to request their quotes. The stack also includes a backend data lake, which utilizes many cloud services from AWS. Data is also stored in AWS that is used to keep track of the customers as well as to store data used for training models that generate the requested quotes.

## Project Reproduction Steps

### Local Machine
Run `pip install -r requirements.txt` to install all necessary libraries.

First, I obtained the medical information data from [Kaggle](https://www.kaggle.com/datasets/alphiree/cardiovascular-diseases-risk-prediction-dataset/data).

I then created a Postgres database in AWS, and with environment variable `DB_PASSWORD` set, I ran `python scripts/create_tables.py` to create the tables I need in the database.

I then inserted the medical information I needed for data science training, by running `python scripts/insert_medical_information.py`.

I also inserted product information into the Postgres database, by setting up pgAdmin and running inside psql `INSERT INTO products VALUES (1, 'Bronze Plan', 'Health', 100), (2, 'Silver Plan', 'Health', 200), (3, 'Gold Plan', 'Health', 400);`.

### Back end
I set up my ETL pipeline using AWS Glue. The script for the ETL job is located [here](aws/medical-info-etl.py). The ETL extracts the data from the `medical_information` table from the Postgres Database, transforms it by selecting all the data, and loads it into S3, which is the data lake for the insurance company.

I then use AWS Sagemaker to load the data from S3, preprocess, train, and test two logistic regression models to predict risk of heart disease and diabetes given medical information.
The code that was run in AWS Sagemaker is located in [this Jupyter notebook](aws/medical-info-log-reg.ipynb). The models are then saved to S3.

I also set up an AWS API Gateway under the endpoint `https://w7f1cr100a.execute-api.us-east-1.amazonaws.com/v1`, which has 4 routes:

1. `POST /customers`, which inserts customer information into the Postgres database.
2. `POST /medical-information`, which inserts medical information into the Postgres database.
3. `POST /calculate-risk`, which calculates the customer's risk of developing heart disease and diabetes using the trained models.
4. `POST /calculate-premium`, which calculates the premiums for each product plan in the Postgres database.

Each endpoint is configured to trigger a lambda. All the lambda code are located [here](aws/lambda/). Note that to get the lambdas working in AWS, I had to download the package binaries needed for each Lambda and uploaded them to a Lambda layer. The zip files exist locally but are excluded from Github.

## Front end
I set up the front end of my application using Streamlit. My medical questionnaire uses questions from the 2015 [The Behavioral Risk Factor Surveillance System (BRFSS)](https://www.cdc.gov/brfss/annual_data/2015/pdf/codebook15_llcp.pdf), which is the nation’s premier system of health-related telephone surveys that collect state data about U.S. residents regarding their health-related risk behaviors, chronic health conditions, and use of preventive services, given that is the source data for the Kaggle dataset. 

To run the app locally, run `streamlit run app.py`.

The front end of my application connects to the back end of my application via the API Gateway.

To access the public version of the app, navigate to https://jason-insurance-company.streamlit.app/