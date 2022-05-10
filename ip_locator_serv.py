import requests
import json
import socket


"""Using page 168 from chapter 2.7 of Computer Networking, A Top Down Approach, adapted TCPserver.py
to implement a simple HTTP server. Additional resources used for python socket specific information from
'Socket programing HOWTO' docs pages: https://docs.python.org/3/howto/sockets.html

Instructions:
Ensure socket, request, and json libraries are installed in local system  and imported.
Copy get_external_ip() and get_ip_loc() functions from ip_locator to user service.
Assigned a local variable to return get_ip_loc() to.
Run ip_locator_serv.py then start your app.
Can be used continuously, no need to restart the ip_locator_serv
"""


#Port and IP to use for microservice pseudo Server
server_port = 18777                         #Can use any private combo of port and ip; must match ip_location.py
server_ip = '127.0.0.2'                     #Use 127.0.0.2 for localhost connections as 127.0.0.1 likely auto assigned already

def get_location(ext_ip):
    api = "http://ip-api.com/json/"         #Api for ip-api.com to return json location information
    api_query = api + ext_ip                #Combine user external ip with api address

    query = requests.get(api_query)         #Make get request
    parsed = query.json()
    parsed = json.dumps(parsed)             #Use to prevent byte errors when sending over sockets
    return parsed

#Setup for the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Base socket setup
server_socket.bind((server_ip, server_port))                            #Bind the port for the server to listen on
server_socket.listen(1)

#Using listen and accept from: https://docs.python.org/3/library/socket.html#socket.socket.accept
while True:
    connection_socket, addr = server_socket.accept()
    user_ext_ip = connection_socket.recv(1024).decode()         #Assign the receive ip info from user
    location_data = get_location(user_ext_ip)                   #Run get_location()
    connection_socket.send(location_data.encode())              #Send JSON data back to user and close connection
    connection_socket.close()                                   #Close current connection

