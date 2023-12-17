import json
import os
import boto3
import pandas as pd
import joblib

def lambda_handler(event, context):
    body = json.loads(event['body'])

    medical_data = {
        'generalhealth': [body.get('general_health')],
        'checkup': [body.get('checkup')],
        'exercise': [body.get('exercise')],
        'skincancer': [body.get('skin_cancer')],
        'othercancer': [body.get('other_cancer')],
        'depression': [body.get('depression')],
        'arthritis': [body.get('arthritis')],
        'sex': [body.get('sex')],
        'agecategory': [body.get('age_category')],
        'height': [body.get('height')],
        'weight': [body.get('weight')],
        'bmi': [body.get('bmi')],
        'smokinghistory': [body.get('smoking_history')],
        'alcoholconsumption': [body.get('alcohol_consumption')],
        'fruitconsumption': [body.get('fruit_consumption')],
        'greenvegetablesconsumption': [body.get('green_vegetables_consumption')],
        'friedpotatoconsumption': [body.get('fried_potato_consumption')]
    }
    df = pd.DataFrame.from_dict(medical_data)

    def yes_no_to_boolean(value):
        return True if value == 'Yes' else False if value == 'No' else None

    columns_to_convert = ['exercise', 'smokinghistory', 'skincancer', 'othercancer', 'depression', 'arthritis']

    for column in columns_to_convert:
        df[column] = df[column].apply(lambda x: yes_no_to_boolean(x))

    all_categories = {
        'generalhealth': ['Excellent', 'Fair', 'Good', 'Poor', 'Very Good'],
        'checkup': ['5 or more years ago', 'Never', 'Within the past 2 years', 'Within the past 5 years', 'Within the past year'],
        'sex': ['Female', 'Male'],
        'agecategory': ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
    }

    for column, categories in all_categories.items():
        dummies = pd.get_dummies(df[column], prefix=column)
        # Add missing columns with zeros
        for cat in categories:
            if f'{column}_{cat}' not in dummies:
                dummies[f'{column}_{cat}'] = 0
        df = df.drop(column, axis=1)
        df = pd.concat([df, dummies], axis=1)

    s3_client = boto3.client('s3')
    bucket = os.environ['S3_BUCKET_NAME']
    model_diabetes = load_model_from_s3(s3_client, bucket, 'model/model_diabetes.joblib')
    model_heart = load_model_from_s3(s3_client, bucket, 'model/model_heart.joblib')
    risk_diabetes = model_diabetes.predict_proba(df)[0, 1]
    risk_heart = model_heart.predict_proba(df)[0, 1]

    return {
        'statusCode': 200,
        'body': json.dumps({
            "risk_diabetes": risk_diabetes,
            "risk_heart": risk_heart
        })
    }

def load_model_from_s3(s3_client, bucket, model_key):
    # Load a model from S3
    with open('/tmp/model.joblib', 'wb') as f:
        s3_client.download_fileobj(bucket, model_key, f)
    return joblib.load('/tmp/model.joblib')