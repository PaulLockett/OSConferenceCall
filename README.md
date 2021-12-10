# OSConferenceCall

This is the final project for Paul Lockett and Dominic Ducre's 
Operating Systems class 341.

It is a simple program that allows the user to create a virtual
conference call server. with the ability to share video, audio,
and text.

To run the program, you must first install the following:
- Python 3.9
- anything in the requirements.txt file

First, you must run the server.py file.

this will ask for an ip address to run the server on. You can
run the server on any ip address you want but it defaults to
the local private ip address.

Note: If you are running the server on the local private ip
address, you must run the server on the same machine as the
client.

once you have choses an ip address, a dialog will pop up with
a button to start the server.

pressing the button will start the server and the server will
run until you press the "close the server" button or end the
program.

Second, you must run the client.py file.

The client will ask for an ip address to connect to. You can
connect to any ip address that a server is running on.

Then the client will ask for a username. This is the name that
the client will use to identify itself in the chat.

lastly, a dialog will pop up with a button to connect to the
server.

once coonnected, the client will be able to send messages in
the chat, share video, audio, and disconnect from the server.

if you want to try out the program, you can run the client.py
and connect to my server at the ip address: 


I used the following links to help me with the project:
- https://www.youtube.com/watch?v=sopNW98CRag&t=1014s
- https://www.youtube.com/watch?v=bJOvYgSqrOs&t=559s

