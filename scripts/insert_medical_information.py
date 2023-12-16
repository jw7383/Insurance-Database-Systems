import pandas as pd
import psycopg2
import os

def yes_no_to_boolean(value):
    return True if value == 'Yes' else False if value == 'No' else None

def yes_no_to_boolean_other(value):
    return True if value == 'Yes' else False if value == 'No' else False

csv_file_path = 'data/CVD_cleaned.csv'
df = pd.read_csv(csv_file_path)

boolean_columns = ['Exercise', 'Heart_Disease', 'Skin_Cancer', 'Other_Cancer', 'Depression', 'Arthritis', 'Smoking_History']
for column in boolean_columns:
    df[column] = df[column].apply(yes_no_to_boolean)
    
other_boolean_columns = ['Diabetes']
for column in other_boolean_columns:
    df[column] = df[column].apply(yes_no_to_boolean_other)

df['Sex'] = df['Sex'].map({'Female': 'F', 'Male': 'M'})

host = 'insurance-database-1.c3o2kc84k6xe.us-east-1.rds.amazonaws.com'
dbname = 'postgres'
user = 'postgres'
password = os.getenv('DB_PASSWORD') 
port = '5432'

if not password:
    raise ValueError("No password provided for the database.")

conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
cur = conn.cursor()

insert_stmt = """
INSERT INTO medical_information (
    GeneralHealth, Checkup, Exercise, HeartDisease, SkinCancer, OtherCancer,
    Depression, Diabetes, Arthritis, Sex, AgeCategory, Height, Weight, BMI,
    SmokingHistory, AlcoholConsumption, FruitConsumption, GreenVegetablesConsumption,
    FriedPotatoConsumption
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in df.iterrows():
    cur.execute(insert_stmt, (
        row['General_Health'], row['Checkup'], row['Exercise'], row['Heart_Disease'], 
        row['Skin_Cancer'], row['Other_Cancer'], row['Depression'], row['Diabetes'], 
        row['Arthritis'], row['Sex'], row['Age_Category'], row['Height_(cm)'], row['Weight_(kg)'], 
        row['BMI'], row['Smoking_History'], row['Alcohol_Consumption'], row['Fruit_Consumption'], 
        row['Green_Vegetables_Consumption'], row['FriedPotato_Consumption']
    ))

conn.commit()

cur.close()
conn.close()

print("Data inserted successfully.")