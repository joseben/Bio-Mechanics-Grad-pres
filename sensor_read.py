import serial
import time
import numpy as np

def conversion(values):
    c=4.448
    v1,v2,v3,v4 = values
    
    x1=(0.7454*np.exp(0.0073*v1))*c

    x2= (0.6981*np.exp(0.0072*v2))*c

    x3= (0.5177*np.exp(0.0076*v3))*c

    x4= (0.6861*np.exp(0.0074*v4))*c
    #print()
    #print(x3)

    values= x1,x2,x3,x4
    return values

class readSensor:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.last_positions = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        self.last_values = [0, 0, 0, 0]  # Store last known values
        self.setup_serial()

    def setup_serial(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1.0
            )
            time.sleep(2)  # Wait for Arduino reset
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            raise

    def parse_encoder_message(self, message):
        try:
            values = message.strip(';').split(',')
            raw_values = []
            for value in values:
                raw_values.append(int(value[1:]))
            return raw_values
        except:
            return None


    def Readsens(self):
        """Returns raw sensor values as an array [s1, s2, s3, s4]"""
        if self.ser is None or not self.ser.is_open:
            raise Exception("Serial port not open")

        if self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                values = self.parse_encoder_message(line)
                values = conversion(values)
                if values:
                    self.last_values = values  # Update last known values
                    return values

        return self.last_values

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def __del__(self):
        self.close()
