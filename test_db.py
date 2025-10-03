import mysql.connector

def test_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chatbot",
            port=3307
        )
        if conn.is_connected():
            print("✅ Connected to MySQL successfully!")
            conn.close()
        else:
            print("❌ Connection failed.")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
