import json
import psycopg2
import os

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    name = body.get('name')
    dob = body.get('dob')  # Expected in 'YYYY-MM-DD' format
    address = body.get('address')

    host = 'insurance-database-1.c3o2kc84k6xe.us-east-1.rds.amazonaws.com'
    dbname = 'postgres'
    user = 'postgres'
    password = os.getenv('DB_PASSWORD')
    port = '5432'

    insert_sql = """
    INSERT INTO CUSTOMERS (name, dob, address)
    VALUES (%s, %s, %s)
    """

    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port, sslmode='require')
        cur = conn.cursor()
        cur.execute(insert_sql, (name, dob, address))
        conn.commit()
        cur.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Customer information inserted successfully')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error inserting customer information')
        }