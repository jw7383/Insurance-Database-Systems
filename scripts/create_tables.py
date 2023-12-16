import psycopg2
import os

host = 'insurance-database-1.c3o2kc84k6xe.us-east-1.rds.amazonaws.com'
dbname = 'postgres'
user = 'postgres'
password = os.getenv('DB_PASSWORD')
port = '5432'

if not password:
    raise ValueError("No password provided for the database.")

conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
cur = conn.cursor()

commands = (
    """
    CREATE TABLE PRODUCTS (
        productId SERIAL PRIMARY KEY,
        productName VARCHAR(255),
        lineOfBusiness VARCHAR(255),
        basePrice INT
    )
    """,
        """
    CREATE TABLE ACCOUNTS (
        accountId SERIAL PRIMARY KEY,
        accountName VARCHAR(255),
        productId INT REFERENCES PRODUCTS(productId)
    )
    """,
    """
    CREATE TABLE CUSTOMERS (
        customerId SERIAL PRIMARY KEY,
        name VARCHAR(255),
        dob DATE,
        address VARCHAR(255),
        accountId INT REFERENCES ACCOUNTS(accountId)
    )
    """,
    """
    CREATE TABLE MEDICAL_INFORMATION (
        recordId SERIAL PRIMARY KEY,
        customerId INT REFERENCES CUSTOMERS(customerId),
        GeneralHealth VARCHAR(255),
        Checkup VARCHAR(255),
        Exercise BOOLEAN,
        HeartDisease BOOLEAN,
        SkinCancer BOOLEAN,
        OtherCancer BOOLEAN,
        Depression BOOLEAN,
        Diabetes BOOLEAN,
        Arthritis BOOLEAN,
        Sex VARCHAR(50),
        AgeCategory VARCHAR(255),
        Height INT,
        Weight FLOAT,
        BMI FLOAT,
        SmokingHistory BOOLEAN,
        AlcoholConsumption INT,
        FruitConsumption INT,
        GreenVegetablesConsumption INT,
        FriedPotatoConsumption INT
    )
    """
)

for command in commands:
    cur.execute(command)

conn.commit()

cur.close()
conn.close()
