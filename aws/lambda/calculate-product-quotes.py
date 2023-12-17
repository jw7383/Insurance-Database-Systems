import json
import psycopg2
import os

def lambda_handler(event, context):
    body = json.loads(event['body'])

    risk_diabetes = body.get('risk_diabetes')
    risk_heart = body.get('risk_heart')

    host = 'insurance-database-1.c3o2kc84k6xe.us-east-1.rds.amazonaws.com'
    dbname = 'postgres'
    user = 'postgres'
    password = os.getenv('DB_PASSWORD')
    port = '5432'

    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT productId, productName, basePrice FROM PRODUCTS")
    products = cur.fetchall()

    premiums = []
    for product in products:
        productId, productName, basePrice = product
        premium = basePrice * (1 + risk_diabetes + risk_heart)
        premiums.append({
            'productId': productId,
            'productName': productName,
            'premium': premium
        })

    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(premiums)
    }