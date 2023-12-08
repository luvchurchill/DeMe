# DeMe
#### Decentralized Messaging using Blockchain

This is my CS50x 2023 final project

-------------

[About the project](#about-the-project)

[installation](#installation)

[Usage](#usage)

[Consessions](#conssesions)

[Credits](#credits)

--------------

### About the project

DeMe is a blockchain based messaging app. The app is split into 2 programs; a Flask "server-side" node (app.py) and a "Client-side" program (client.py) which the user actually interacts with.

The node takes care of communicating with other nodes, mining blocks (which is pointless as of now, see [Consessions](#conssesions)) and validating the chain

the client takes care of encrypting the messages, checking the chain for new messages and translating the message into a well formed HTTP request and block

-----------

### Installation

this will cover installation on a Linux and Mac OS

open a terminal

first you must download the code:

```git clone https://github.com/luvchurchill/DeMe.git ```

then change into the project directory

```cd DeMe```

create a virtual enviornment (venv)

```python3 -m venv venv```

activate the venv

```source venv/bin/activate```

you should see that your terminal prompt now has ``(venv)`` before your name, like so

```(venv) johndoe@my-pc:-$``` 

now you can install all the required packages without them affecting the rest of your computer

```pip install -r requirements```

that's it! now everything is installed, to get out of the venv just type ```deactivate```

to use the program you the venv must be activated so just do ``source venv/bin/activate`` again

---------

### Usage

Make sure the venv is activated

first change into the src directory

```cd src```

You need both programs to run at once so first run app.py

```python3 app.py```

this will start talking a lot but you can disregard it unless something goes wrong, it can be useful for debugging.

now open another tab/terminal. make sure you are in the DeMe/src directory and run client.py

```python3 client.py```

the rest is pretty self-explantory but here's a couple things to keep in mind.

1) the first time you try to send a message python will create a "keys" subdirectory (in the src directory)
2) your public and private keys will be named `public.pem` and `private.pem` respectively
3) NEVER share private.pem with anyone, they can use it to decrypt all your messages
3) It is perfectly ok to share your public key (public.pem) with anyone
3) If you want to message someone you will need their public key, for convenience you can save it in the keys folder as `friends-name.pem` then when you send them a message and the program asks for the location of their key write `keys/friends-name.pem`
3) don't trust the encryption unless you read through the code and are ok with it (code is provided AS IS! see the license)
3) when program asks you if you already have keys, if you do yet you answer no, it will overwrite your old keys and you will have to share your public key again with your correspondents

----------------

#### Credits

I got the outline for the skeleton of a blockchain from 3 articles
[geeksforgeeks](https://www.geeksforgeeks.org/create-simple-blockchain-using-python/),
[active state](https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/), [dev](https://dev.to/envoy_/learn-blockchains-by-building-one-in-python-2kb3) and of course the [OG](https://nakamotoinstitute.org/bitcoin/).
 You can look at outline.txt to see what I incorporated from each

 [python.land](python.land), [python docs](https://docs.python.org/), [geeks for geeks](https://www.geeksforgeeks.org/) and many more

 Last but not least [Prof. David Malan](https://davidmalan.com/malan/)!