from socket import socket, AF_INET, SOCK_STREAM

packet_separator = '\x00'


def server(host, port, packets_count=500):
	sockobj = socket(AF_INET, SOCK_STREAM) 
	sockobj.bind((host, port)) 
	sockobj.listen(5) 
	while True: 
	    connection, address = sockobj.accept()
	    for i in range(packets_count):
	        connection.send(b'<my_tag tag_value="{}">{}</my_tag>{}'.format(i, i, packet_separator))
	    connection.close()


if __name__ == '__main__':
    server('127.0.0.1', 33333)
