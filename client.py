import socket
import time
from multiprocessing import cpu_count, Queue, Process, Value, Manager
from xml.etree import ElementTree as etree

packet_separator = '\x00'


def reader(host, port, queue, packets_count):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((host, port))
    accumulated = ''
    i = 0
    while True:
        data = sck.recv(1024)
        #time.sleep(.5)
        if not data:
            break
        packets = data.split(packet_separator)
        packets[0] = accumulated + packets[0]
        packets, accumulated = packets[:-1], packets[-1]
        for packet in packets:
            queue.put((i, packet))
            i += 1
        time.sleep(.05)
    packets_count.value = i
    sck.close()


def parse(queue, packets_count, packets_dict, _id):
    while True:
        if not queue.empty():
            i, data = queue.get()
            time.sleep(.5)
            packets_dict[i] = etree.fromstring(data)
            print 'process {} parsed {}'.format(_id, i)
        else:
            if packets_count.value > 0:
                break


def process(packet):
    xml = etree.tostring(packet)
    print '== RECEIVED =='
    print xml


def serve(host, port):
    queue = Queue()
    manager = Manager()
    packets_dict = manager.dict()
    packets_count = Value('i', 0)

    reader_process = Process(target=reader, args=(host, port, queue, packets_count))
    reader_process.start()

    cpu_c = cpu_count()
    pool = [Process(target=parse, args=(queue, packets_count, packets_dict, i)) for i in range(cpu_c)]
    for p in pool:
        p.start()

    i = 0
    while True:
        while packets_dict.get(i, None) is None:
            time.sleep(.05)
        process(packets_dict[i])
        i += 1

        if i == packets_count.value > 0:
            break

    reader_process.join()
    for p in pool:
        p.join()


if __name__ == '__main__':
    start_time = time.time()
    serve('127.0.0.1', 33333)
    print '== {} seconds =='.format(time.time() - start_time)
