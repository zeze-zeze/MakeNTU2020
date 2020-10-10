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
        print(sended)
        self.ser.write(sended)
        print('sended!')

    def req(self):
        for i in range(2):
            res = requests.get('http://140.113.68.171:35000/replyiot?id={}'.format(i))
            self.send(res.text)

iot = IOT()
while True:
    iot.req()
    time.sleep(2)
