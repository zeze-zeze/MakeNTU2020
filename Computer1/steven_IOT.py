import serial
import requests
import time

class IOT():
    def __init__(self):
        COM_PORT = 'COM6'
        BAUD_RATES = '9600'
        self.ser = serial.Serial(COM_PORT, BAUD_RATES)

    def send(self, sended):
        sended = sended.encode()
        self.ser.write(sended)
        print(self.ser.readline())
        print(sended, 'sended!')

    def req(self, index):
        res = requests.get('http://140.113.68.171:35000/replyiot?id={}'.format(index))
        self.send(res.text)

iot = IOT()
while True:
    #iot.send('0,10')
    #iot.req(0)
    #time.sleep(1)
    #iot.req(1)
    iot.req('1,0')
    time.sleep(1)
