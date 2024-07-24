import sqlite3
import socket

# データベースに接続し、カーソルを取得
conn = sqlite3.connect('IIC_base.db')
cursor = conn.cursor()

# テーブルの作成
cursor.execute('''CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Year INTEGER,
    Month INTEGER,
    user_Name TEXT,
    item_name TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT UNIQUE,
    price INTEGER
)''')

# 商品データの挿入
product_data = [
    ("chips-sio", 110),
    ("coffee-black", 90),
    ("coffee-latte", 120)
]
for data in product_data:
	cursor.execute("INSERT INTO product (item_name, price) VALUES (?, ?)", data)

# サーバーの設定
HOST = '192.168.151.44'
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
	server_socket.bind((HOST, PORT))
	server_socket.listen()
	print(f'Server listening on {HOST}:{PORT}')
	while True:
		conn2, addr = server_socket.accept()
		with conn2:
			print(f"Connected by {addr}")
			while True:
				data = conn2.recv(1024).decode()
				if not data:
					continue
				year, month, user, item = data.split()
				year = int(year)
				month = int(month)
				print(year ,month,user,item)
				cursor.execute("INSERT INTO user (Year, Month, user_Name, item_name) VALUES (?, ?, ?, ?)", (year, month, user, item))
				conn2.sendall(b"Data inserted")
				conn.commit()
				print("data in")
conn.closed()