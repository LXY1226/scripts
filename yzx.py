import socket,os


def bytetoint(byte):
    return int(byte.hex(), 16)

fd = os.open('Record.csv', os.O_RDWR|os.O_CREAT)

with open('Record.zc', 'rb') as f:
    pos = 0
    tot = os.path.getsize('Record.zc')
    print('Processing %d records'%(tot/32))
    while pos < tot:
        data = f.read(32)
        pos = pos + 32
        p = 0
        for d in data[0:27]:
            p = p + d
        p = p % 256
        if data[0:3] != b'\xab\x00\x06':
            print('Invaild Header at %d, %s != ab0006' % (pos / 32, data[0:3].hex()))
        if p != data[27]:
            print('Invaild CRC at %d, %x != %s' % (pos/32, p, data[27:28].hex()))
        os.write(fd, ("%s,%s,%s,%s,%s,%s,%s\r" % (
            socket.ntohl(bytetoint(data[19:23])) / 1000, 
            socket.ntohl(bytetoint(data[3:7])) / 10000, 
            socket.ntohl(bytetoint(data[7:11])) / 10000, 
            socket.ntohl(bytetoint(data[11:15])) / 10000, 
            socket.ntohl(bytetoint(data[15:19])) / 10000, 
            socket.ntohl(bytetoint(data[23:27])) % 65536 / 1000, 
            int(socket.ntohl(bytetoint(data[23:27])) / 65536) / 10000)).encode())

os.close(fd)
