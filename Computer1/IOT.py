import serial

class IOT():
    def __init__(self):
        COM_PORT = 'COM4'
        BAUD_RATES = '9600'
        self.ser = serial.Serial(COM_PORT, BAUD_RATES)

    def send(self, id_, finished):
        sended = '{},{}'.format(id_, finished).encode()
        print(sended)
        self.ser.write(sended)
        print('sended!')
