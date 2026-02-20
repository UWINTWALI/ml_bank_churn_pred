import csv
import random
import uuid
from faker import Faker
from datetime import datetime

# initialize faker for realistic names
fake = Faker()

def generate_customer_data(num_rows=100):
    """Generate synthetic customer data similar to the example"""
    
    # define possible values for categorical fields
    geographies = ['France', 'Spain', 'Germany']
    genders = ['Male', 'Female']
    surnames = []  # surnames will be generated dynamically
    
    data = []
    
    for i in range(1, num_rows + 1):
        # generate unique CustomerId: 10-digit number
        customer_id = random.randint(10000000, 99999999)
        
        # generate surnames
        surname = fake.last_name()
        
        # CreditScore: typically 300-850, with normal distribution
        credit_score = int(random.normalvariate(650, 100))
        credit_score = max(300, min(850, credit_score))
        
        # geography
        geography = random.choices(geographies, weights=[0.5, 0.3, 0.2])[0]
        
        # gender
        gender = random.choice(genders)
        
        # age: Normal distribution around 40
        age = int(random.normalvariate(40, 10))
        age = max(18, min(80, age))
        
        # tenure: Years with bank (0-10)
        tenure = random.randint(0, 10)
        
        # balance: many customers have 0 balance
        if random.random() < 0.4:  # 40% have 0 balance
            balance = 0.0
        else:
            balance = round(random.uniform(1000, 200000), 2)
        
        # NumOfProducts: Most have 1-2, some have more
        prob = random.random()
        if prob < 0.6:
            num_products = 1
        elif prob < 0.9:
            num_products = 2
        elif prob < 0.98:
            num_products = 3
        else:
            num_products = 4
        
        # HasCrCard: most customers have credit cards
        has_cr_card = 1 if random.random() < 0.7 else 0
        
        # IsActiveMember: about half are active
        is_active_member = 1 if random.random() < 0.5 else 0
        
        # EstimatedSalary: log normal distribution
        salary = random.lognormvariate(10.5, 0.8)
        salary = round(min(salary, 200000), 2)
        
        # create row
        row = [
            i,  # RowNumber
            customer_id,
            surname,
            credit_score,
            geography,
            gender,
            age,
            tenure,
            balance,
            num_products,
            has_cr_card,
            is_active_member,
            salary
        ]
        
        data.append(row)
    
    return data

def save_to_csv(data, filename='data/generated_customer_test_data.csv'):
    """Save generated data to CSV file format"""
    
    headers = [
        'RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography',
        'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
        'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
    ]
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Generated {len(data)} rows and saved to {filename}")

# generate and save data
data = generate_customer_data(5000)  # generate 500 rows
save_to_csv(data)