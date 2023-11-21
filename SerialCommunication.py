import serial

from Constants import GET, SET, NEW


class Serial:
    def __init__(self, com, br, time_out=0.1):
        self.serial = serial.Serial(com, br)
        self.buffer = []
        self.disconnected = False

    def open(self):
        if not self.serial.isOpen():
            self.serial.open()
        self.serial.reset_input_buffer()

    def close(self):
        self.serial.close()

    def getNewData(self):
        try:

            lst = []
            if self.serial.in_waiting > 0:
                data = self.serial.read(self.serial.in_waiting)
                if data:
                    for d in data:
                        if chr(d) == '\r':
                            self.buffer.append(lst)
                        elif chr(d) == '\n':
                            break
                        lst.append(chr(d))
        except:
            if not self.disconnected:
                print("Disconnected")
                self.disconnected = True
                del self

    def getData(self):
        if len(self.buffer) > 0:
            data = self.buffer[0]
            self.buffer.pop(0)
            return data
        return 0

    def setData(self, data):
        self.serial.write(data.encode())
