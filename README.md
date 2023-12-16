# Insurance-Database-Systems
DS-GA 2433: Database Systems Final Project

## Summary

## Project Reproduction Steps

### Local Machine
Run `pip install -r requirements.txt` to install all necessary libraries.

First, I obtained the medical information data from [Kaggle](https://www.kaggle.com/datasets/alphiree/cardiovascular-diseases-risk-prediction-dataset/data).

I then created a Postgres database in AWS, and with environment variable `DB_PASSWORD` set, I ran `python scripts/create_tables.py` to create the tables I need in the database.

I then inserted the medical information I needed for data science training, by running `python scripts/insert_medical_information.py`.

### AWS
I set up my ETL pipeline using AWS Glue. The script for the ETL job is located [here](aws/medical-info-etl.py).

The ETL extracts the data from the medical_information table from the Postgres Database, transforms it by selecting all the data, and loads into S3, which is the data lake for the insurance company.

I then use AWS Sagemaker to load the data from S3, preprocess, train, and test two logistic regression models to predict risk of heart disease and diabetes given medical information.
The code that was run in AWS Sagemaker is located in [this Jupyter notebook](aws/medical-info-log-reg.ipynb).