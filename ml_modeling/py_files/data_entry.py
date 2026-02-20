import pandas as pd
import psycopg2

# load the data
churn_data = pd.read_csv("data/no_label_churn_data.csv")

# connect to my PgAdmin
conn = psycopg2.connect(
    host="localhost",
    database="Bk_customer_churn",
    user="postgres",
    password="Proumd&25",
    port=5432
)

cur = conn.cursor()

# insert row by row
for _, row in churn_data.iterrows():
    cur.execute("""
        INSERT INTO new_customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cur.close()
conn.close()
