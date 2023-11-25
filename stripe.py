import json
import mysql.connector
from datetime import datetime

# Fungsi untuk mendapatkan data dari file JSON lokal
def get_stripe_data():
    try:
        with open('stripe.json', 'r') as file:
            data = json.load(file)
        return data.get('data', [])
    except FileNotFoundError:
        print("File stripe.json not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

# Fungsi untuk menyimpan data ke dalam database MySQL
def save_to_mysql(data):
    if not isinstance(data, list):
        print("Invalid data format. Expected a list.")
        return

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="MyFundation"
    )
    cursor = connection.cursor()

    for transaction in data:
        if not isinstance(transaction, dict):
            print(f"Invalid transaction format: {transaction}. Skipping.")
            continue

        # Ubah pengambilan nilai sesuai dengan kebutuhan Anda
        transaction_id = transaction.get('id')
        amount = int(transaction.get('amount'))
        created = int(transaction.get('created'))
        currency = transaction.get('currency')

        # Sesuaikan nama kolom dan nilai sesuai dengan tabel Anda
        insert_query = "INSERT INTO data_stripe (id, amount, created, currency) VALUES (%s, %s, %s, %s)"
        values = (transaction_id, amount, created, currency)

        cursor.execute(insert_query, values)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    stripe_data = get_stripe_data()
    
    if stripe_data:
        save_to_mysql(stripe_data)
        print("Data from JSON file has been successfully saved to MySQL.")
    else:
        print("Unable to retrieve valid data from JSON file.")
