import serial


class PrologixDevice:
    def __init__(self, port):
        self.port = port
        self.open = False 

    def __repr__(self):
        return "Prologix Device at port {} is open: {}".format(self.port, self.open)

    def __enter__(self):
        self.connection = serial.Serial(self.port ,9600, timeout=.5)
        self.setup_connection()
        self.open = True
        return self

    def setup_connection(self):
        self.raw_write("++rst")
        self.raw_write("++mode 1")
        self.raw_write("++eoi 1")
        self.raw_write("++eos 1")
        self.raw_write("++auto 0")

    def raw_write(self, command):
        if isinstance(command, str):
            command = command.encode()
        self.connection.write(command + b"\n")
        

    def write(self, device_id, command):
        self.raw_write("++addr {}".format(int(device_id)))
        self.raw_write(command)

    def read(self, device_id, length = 1024):
        self.raw_write("++addr {}".format(int(device_id)))
        self.raw_write("++read eoi")
        return self.connection.read(1024).decode().strip("\n \r")
        
    def query(self, device_id, command ,response_length = 1024):
        self.write(device_id, command)
        return self.read(device_id, length=response_length)

    def __exit__(self, *args):
        self.connection.close()
        self.open = False
