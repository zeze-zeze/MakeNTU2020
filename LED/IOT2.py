import serial
import requests
import time

class IOT():
    def __init__(self):
        COM_PORT = 'COM3'
        BAUD_RATES = '115200'
        self.ser = serial.Serial(COM_PORT, BAUD_RATES)

    def send(self, sended):
        sended = sended.encode()
        self.ser.write(sended)
        print(sended, 'sended!')

    def req(self, index):
        res = requests.get('http://140.113.68.171:35000/replyiot?id={}'.format(index))
        self.send(res.text)

iot = IOT()
while True:
    iot.req(0)
    time.sleep(2)
    iot.req(1)
    time.sleep(2)
