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

import json
import requests
import sys
import time

#known_node = input("please input the IP of a known node e.g. '8.8.8.8' ")
def get_ip_address():
    url = 'https://api.ipify.org'
    try:
        response = requests.get(url)
        ip = response.text
        return ip
    except requests.HTTPError as error:
        print(f"there was an error with resolving your ip {error}")
    except Exception as err:
        print(f"there was an error {err}")
 
print(get_ip_address())

def main():
    action = input("Check new messages: 'n', Send a message 's', Download the chain 'c', Quit 'q'")
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

    else:
        print("Not a valid option, please try again")

local_host = "127.0.0.1:5000"
print(f"{local_host}/mine")

def check_messages():
    my_messages = []
    my_node = {"new_node": get_ip_address()}
    #requests.post(f"http://{local_host}/register", json=my_node)
    headers = {'Accept': 'application/json'}
    request = requests.get(f"http://{local_host}/chain", headers=headers)
    chain = json.loads(request.content)
    for block in chain:
        block_dict = json.loads(block)
        if block_dict["content"] and block_dict["content"][0]["recipient"] == "me":
            my_messages.append(block)

    print(my_messages)


def send_message():
    pass


def get_chain():
    pass




while True:
    main()