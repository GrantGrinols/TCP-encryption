import socket;
import threading;
import json;

import rsa;

jsonFile = open("IPAddress.json")
ipaddress = json.load(jsonFile)
ADDRESS = ipaddress["Address"]
publickey, privatekey = rsa.newkeys(1024)
publicpartner = None

choice1 = input("Do you want do host (1) or connect (2): ")
choice2 = input("Unencrypted (1) or Encrypted(2): ")



def sendMessage(c):
    while True:
        message = input("")
        c.send(message.encode())
def sendEncryptedMessage(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), publicpartner))

def recieveMessage(c):
    while True:
        print("Partner: " + c.recv(1024).decode())
def recieveEncryptedMessage(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(2034), privatekey).decode())

if(choice2=="1"):
    if choice1 == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ADDRESS, 9999))
        server.listen()
        client, _ = server.accept()
        print("Listening...")
    elif choice1 =="2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ADDRESS, 9999))
        print("Send messages now: ")
    else:
        exit()
    threading.Thread(target=sendMessage, args=(client,)).start()
    threading.Thread(target=recieveMessage, args=(client,)).start()

if(choice2=="2"):
    if choice1 == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ADDRESS, 9999))
        print("Listening...")
        server.listen()
        client, _ = server.accept()
        client.send(publickey.save_pkcs1("PEM"))
        publicpartner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        print("Connected with host")
        
    elif choice1 =="2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ADDRESS, 9999))
        publicpartner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(publickey.save_pkcs1("PEM"))
        print("Send messages now: ")
    else:
        exit()
    threading.Thread(target=sendEncryptedMessage, args=(client,)).start()
    threading.Thread(target=recieveEncryptedMessage, args=(client,)).start()
