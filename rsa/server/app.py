from flask import Flask, request, render_template
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os


app = Flask(__name__)
DEADBEEF_KEY_1 = os.getenv("DEADBEEF_KEY_1")
DEADBEEF_KEY_2 = os.getenv("DEADBEEF_KEY_2") 	

messages = {}
keys = {}
deadbeef_key = None

@app.before_first_request
def prepare_deadbeef():
	global deadbeef_key
	if DEADBEEF_KEY_1 and DEADBEEF_KEY_2:
		with open(DEADBEEF_KEY_1,'r') as key_file:
			print("[1/2] Reading keys...") 
			keys['deadbeef'] = RSA.importKey(key_file.read()).exportKey()
			print("[1/2] OK") 
		with open(DEADBEEF_KEY_2,'r') as key_file:
			print("[2/2] Reading keys...") 
			deadbeef_key     = RSA.importKey(key_file.read())
			print("[2/2] OK")
	if 'deadbeef' not in keys or deadbeef_key is None:
		print("Generating keys...")
		key = RSA.generate(2048)
		keys['deadbeef'] = key.public_key().export_key()
		print("[1/2] OK")
		deadbeef_key     = key
		print("[2/2] OK")

def handle_deadbeef(message):	
	resp = {}
	try:
		encoded_message = base64.decodebytes(message.encode('utf-8'))
		cipher = PKCS1_OAEP.new(deadbeef_key)
		decrypted = cipher.decrypt(encoded_message)
		resp['decrypted'] = decrypted.decode('utf-8')
		return resp, 200
	except Exception as e:
		resp['errors'] = str(e)
		return resp, 400

@app.route('/')
def index():
	return render_template('index.html', messages=messages)


@app.route('/message/<uid>', methods = ['GET','POST'])
def message(uid):

	if request.method == 'GET':

		if uid in messages:
			message, ip = messages[uid]
			return message
		else:
			return f'Nie ma wiadomości do: {uid}', 404

	elif request.method == 'POST':

		json = request.get_json()

		if json and 'message' in json:
			if uid == 'deadbeef':
				return handle_deadbeef(json['message'])
			else:
				messages[uid] = json['message'], request.remote_addr
				return f'Dodano wiadomość dla: {uid}', 200
		else:
			return 'Niepoprawne zapytanie', 400


@app.route('/key/<uid>', methods = ['GET','POST'])
def key(uid):

	if request.method == 'GET':

		if uid in keys:
			return keys[uid]
		else:
			return f'Nie ma klucza dla: {uid}', 404

	elif request.method == 'POST':

		if uid == 'deadbeef':
			return f'Nie można zmienić klucza', 403
		
		json = request.get_json()

		if json and 'key' in json:
			keys[uid] = json['key']
			return f'Dodano klucz dla: {uid}', 200
		else:
			return 'Niepoprawne zapytanie', 400
