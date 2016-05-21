import socket
import time
from multiprocessing import Pool, cpu_count
from xml.etree import ElementTree as etree

packet_separator = '\x00'


def parse(data):
    time.sleep(.5)
    return etree.fromstring(data)


def process(packet):
    xml = etree.tostring(packet)
    print "== RECEIVED =="
    print xml


def serve(host, port):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((host, port))
    cpu_c = cpu_count()
    pool = Pool(processes=cpu_c)
    accumulated = ''
    while True:
        data = sck.recv(1024)
        #time.sleep(.5)
        if not data:
            break

        packets = data.split(packet_separator)
        packets[0] = accumulated + packets[0]
        packets, accumulated = packets[:-1], packets[-1]

        packets = pool.map(parse, packets)
        for packet in packets:
            process(packet)
    sck.close()

if __name__ == '__main__':
    start_time = time.time()
    serve('127.0.0.1', 33333)
    print '== {} seconds =='.format(time.time() - start_time)
    
