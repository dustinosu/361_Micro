import socket
import requests

"""Using page 166 from chapter 2.7 of Computer Networking, A Top Down Approach, adapted TCPclient.py
to implement a simple GET request. Additional resources used for GET specific information from 'Socket programing
HOWTO' docs pages: https://docs.python.org/3/howto/sockets.html

Instructions:
Ensure socket, request, and json libraries are installed in local system  and imported.
Copy get_external_ip() and get_ip_loc() functions from ip_locator to user service.
Assigned a local variable to return get_ip_loc() to.
Run ip_locator_serv.py then start your app.
Can be used continuously, no need to restart the ip_locator_serv
"""

def get_external_ip():
    """
    Users likely using DHCP and local private address could cause issues for the location request.
    This function will return a user's externally facing public ip assigned in DHCP.
    """
    #API for external ip lookup: https://www.ipify.org/
    return requests.get('https://api.ipify.org').text

def get_ip_loc():
    HOST = '127.0.0.2'                                      #Adjust as necessary; match with ip_locator_serv
    PORT = 18777                                            #Adjust as necessary; match with ip_locator_serv

    #Setup socket to connect to local server
    user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Use get_external_ip to get the user's current DHCP; if not using DHCP should still work as expected
    ip_request = get_external_ip()

    try:
        user_socket.connect((HOST, PORT))
        user_socket.sendall(ip_request.encode())
        ip_location = user_socket.recv(1024).decode()

        return ip_location

    except Exception as e:
        print("Cannot connect to the server:", e)

#Assign returned location json data to a variable
user_location = get_ip_loc()
print(user_location)