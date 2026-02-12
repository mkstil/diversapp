from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # للسماح بالطلبات من تطبيق الهاتف

# إعداد الاتصال بقاعدة SQL Server
server =  'SQL5110.site4now.net'  # مثال: 'myserver.database.windows.net'
database =  'db_ac3d8b_mkstil1'
username =  'db_ac3d8b_mkstil1_admin'
password =  'Tijoment24'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# دالة لمثال قراءة البيانات
@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM Users")  # جدول Users كمثال
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({"id": row.id, "username": row.username, "email": row.email})
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

# دالة لمثال إدخال بيانات
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)