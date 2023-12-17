import json
import psycopg2
import os

def lambda_handler(event, context):
    body = json.loads(event['body'])

    general_health = body.get('general_health')
    checkup = body.get('checkup')
    exercise = body.get('exercise')
    skin_cancer = body.get('skin_cancer')
    other_cancer = body.get('other_cancer')
    depression = body.get('depression')
    arthritis = body.get('arthritis')
    sex = body.get('sex')
    age_category = body.get('age_category')
    height = body.get('height')
    weight = body.get('weight')
    bmi = body.get('bmi')
    smoking_history = body.get('smoking_history')
    alcohol_consumption = body.get('alcohol_consumption')
    fruit_consumption = body.get('fruit_consumption')
    green_vegetables_consumption = body.get('green_vegetables_consumption')
    fried_potato_consumption = body.get('fried_potato_consumption')

    host = 'insurance-database-1.c3o2kc84k6xe.us-east-1.rds.amazonaws.com'
    dbname = 'postgres'
    user = 'postgres'
    password = os.getenv('DB_PASSWORD')
    port = '5432'

    insert_sql = """
    INSERT INTO medical_information (
    GeneralHealth, Checkup, Exercise, SkinCancer, OtherCancer,
    Depression, Arthritis, Sex, AgeCategory, Height, Weight, BMI,
    SmokingHistory, AlcoholConsumption, FruitConsumption, GreenVegetablesConsumption,
    FriedPotatoConsumption
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port, sslmode='require')
        cur = conn.cursor()

        # Execute the insert statement
        cur.execute(insert_sql, (general_health, checkup, exercise, skin_cancer, other_cancer, depression, arthritis, sex, age_category, height, weight, bmi, smoking_history, alcohol_consumption, fruit_consumption, green_vegetables_consumption, fried_potato_consumption))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Medical information inserted successfully')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error inserting medical information')
        }