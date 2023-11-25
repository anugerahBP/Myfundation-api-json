import json
import mysql.connector
from datetime import datetime

# Fungsi untuk mendapatkan data dari file JSON lokal
def get_billplz_data():
    try:
        with open('billplz.json', 'r') as file:
            data = json.load(file)
        return data.get('data', [])
    except FileNotFoundError:
        print("File billplz.json not found.")
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
        bill_id = transaction.get('BILL ID')
        payment_received = float(transaction.get('PAYMENT RECEIVED').replace(',', ''))  # Menghapus koma jika ada
        due_date_str = transaction.get('DUE DATE')
        due_date = datetime.strptime(due_date_str, '%d/%m/%y').strftime('%Y-%m-%d')
        currency = transaction.get('CURRENCY')

        # Sesuaikan nama kolom dan nilai sesuai dengan tabel Anda
        insert_query = "INSERT INTO data_billplz (bill_id, payment_received, due_date, currency) VALUES (%s, %s, %s, %s)"
        values = (bill_id, payment_received, due_date, currency)

        cursor.execute(insert_query, values)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    billplz_data = get_billplz_data()
    
    if billplz_data:
        save_to_mysql(billplz_data)
        print("Data from JSON file has been successfully saved to MySQL.")
    else:
        print("Unable to retrieve valid data from JSON file.")
