"""DeMe decenteralized messaging using Blockchain
Copyright (C) 2023  https://github.com/luvchurchill

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

from cryptography.fernet import Fernet
import json
import os
import rsa
import requests
import sys
import time


# known_node = input("please input the IP of a known node e.g. '8.8.8.8' ")
def get_ip_address():
    url = "https://api.ipify.org"
    try:
        response = requests.get(url)
        ip = response.text
        return ip
    except requests.HTTPError as error:
        print(f"there was an error with resolving your ip {error}")
    except Exception as err:
        print(f"there was an error {err}")



def main():
    action = input(
        "Check new messages: 'n', Send a message 's', Download the chain 'c', Mine a block 'm' Quit 'q': "
    )
    if "q" in action:
        print("Exiting DeMe")
        time.sleep(1)
        exit(0)
    elif "n" in action:
        check_messages()

    elif "s" in action:
        send_message()

    elif "c" in action:
        get_chain()

    elif "m" in action:
        mine()

    else:
        print("Not a valid option, please try again")


local_host = "127.0.0.1:5000"


def check_messages():
    """Check for new messages"""
    my_messages = []
    headers = {"Accept": "application/json"}
    my_node = {"new_node": get_ip_address()}
    known_nodes = requests.post(
        f"http://{local_host}/register", json=my_node, headers=headers
    )
    #print(known_nodes.json()) for debugging
    request = requests.get(f"http://{local_host}/chain", headers=headers)
    chain = json.loads(request.content)
    for block in chain:
        block_dict = block
        if block_dict["content"] and block_dict["content"][0]["recipient"] == "me":
            my_messages.append(block)

    print(my_messages)


def send_message():
    """Sends a new message"""
    encryption_managment()
    sender_public = load_keys("mine")[0]
    recipient_public = load_keys(input("Please input the file path of the recipients public key: "))
    message, fernet_key = fernet_encrypt()
    encrypted_key = encrypt_rsa(fernet_key, recipient_public)
    tx = {"sender": sender_public, "recipient": recipient_public, "message": message, "key": encrypted_key}
    json_tx = json.dumps(tx, sort_keys=True)
    request = requests.post(f"http://{local_host}/new", json=json_tx)
    respone = request.json()
    print(respone)


def get_chain():
    """Gets the entire chain"""
    headers = {"Accept": "application/json"}
    request = requests.get(f"http://{local_host}/chain", headers=headers)
    print(request.json())


def mine():
    """Mines a new block"""
    headers = {"Accept": "application/json"}
    request = requests.get(f"http://{local_host}/mine", headers=headers)
    print(request.json())


def encryption_managment():
    has_keys = input("do you already have keys saved? ('y', 'n') ")
    if has_keys == 'n':
        generate_keys()



def generate_keys():
    try:
            os.mkdir("keys")
    except:
            print("it seems you already have a 'keys' subdirectory ")
    public_key, private_key = rsa.newkeys(2048)
    with open("keys/public.pem", "wb") as p:
        p.write(public_key.save_pkcs1("PEM"))

    with open("keys/private.pem", "wb") as p:
        p.write(private_key.save_pkcs1("PEM"))


def load_keys(file_path):
    if file_path == "mine":
        with open("keys/public.pem", "rb") as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())

        with open("keys/private.pem", "rb") as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return public_key, private_key
    else:
        with open(str(file_path), "rb") as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        return public_key



def encrypt_rsa(plaintext, key):
    return rsa.encrypt(plaintext.encode("ascii"), key)


def decrypt_rsa(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode("ascii")
    except:
        return False
    
def fernet_encrypt():
    fernet_key = Fernet.generate_key()
    message = input("Type the message you want to send: ")
    fernet = Fernet(fernet_key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted, fernet_key

def fernet_decrypt(key, message):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(message)
    return decrypted.decode()




while True:
    main()
