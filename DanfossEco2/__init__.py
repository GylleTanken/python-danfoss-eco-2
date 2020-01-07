# Python module for control of Danfoss Eco 2
#
#


from bluepy import btle
import time
import xxtea
import sys

class DanfossEco2(btle.DefaultDelegate):

    pin_uuid = "10020001274900010000-00805F9B042F"
    temperature_uuid = "1002000527490001000000805F9B042F"
    device_name_uuid = "1002000627490001000000805F9B042F"
    battery_uuid = "2A19"

    max_send_time = 30
    max_connect_time = 40
    connected = False

    def __init__(self, mac="00:04:2F:C1:02:A2", encryption_key=b'\xA5\x7F\xF7\x6F\xE8\x6D\xA0\x65\x77\x91\x15\xC2\xA6\x7E\x4A\x92', pin=0000):
        self.mac = mac
        self.pin = pin
        self.key = encryption_key

        self.pin_handle = None
        self.temperature_handle = None
        self.device_name_handle = None
        self.battery_handle = None

        self.battery = 0
        self.name = ""
        self.current_temperature = 0
        self.set_temperature = 0

        btle.DefaultDelegate.__init__(self)
        self.connected = False

    def __del__(self):
        self.disconnect()


    def connect(self):
        self.disconnect()

        initial = time.time()
        connection_try_count = 0
        while True:
            if time.time() - initial >= self.max_connect_time:
                return False
            connection_try_count += 1
            if connection_try_count > 1:
                print("Trying to connect again. Try number: " + str(connection_try_count))
            try:
                self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)
            except:
                print("Could not connect to device with mac: " + self.mac)
                print("Error: ", sys.exc_info()[0])
                continue

            self.device.withDelegate(self)
            handles = self.device.getCharacteristics()
            for handle in handles:
                if handle.uuid == self.pin_uuid:
                    self.pin_handle = handle
                elif handle.uuid == self.temperature_uuid:
                    self.temperature_handle = handle
                elif handle.uuid == self.device_name_uuid:
                    self.device_name_handle = handle
                elif handle.uuid == self.battery_uuid:
                    self.battery_handle = handle
        
            if self.pin_handle == None or self.temperature_handle == None or self.device_name_handle == None or self.battery_handle == None:
                print("Could not find all handles")
                return False
            else:
                self.connected = True
                return True



    def disconnect(self):
        self.pin_handle = None
        self.temperature_handle = None
        self.device_name_handle = None
        self.battery_handle = None
        if hasattr(self, 'device'):
            self.device.disconnect()
        self.connected = False

    def login(self):
        if self.connected:
            return self.send_BLE_packet(self.pin_handle, b'\x00\x00\x00\x00')
        else:
            return False

    def getTemperature(self):
        if self.connected:
            data = self.read_encrypted_handle(self.temperature_handle)
            if data[1] != 0:
                self.current_temperature = data[1]/2
            self.set_temperature = data[0]/2
            return (self.set_temperature, self.current_temperature)
        else:
            return False

    def getBattery(self):
        if self.connected:
            data = self.battery_handle.read()
            self.battery = data[0]
            return self.battery
        else:
            return False

    def getDeviceName(self):
        if self.connected:
            data = self.read_encrypted_handle(self.device_name_handle)
            for i, char in enumerate(data):
                if char == 0:
                    data = data[:i]
                    break
            self.device_name = data.decode("utf-8")
            return self.device_name
        else:
            return False

    def setTemperature(self, temp):
        if self.connected:
            data = bytearray([round(temp*2)]) + bytearray(7)
            return self.send_encrypted_packet(self.temperature_handle, data)
        else:
            return False

    def update(self):
        self.connect()
        if self.connected:
            self.login()
            self.getDeviceName()
            self.getBattery()
            self.getTemperature()
            self.disconnect()
            return True
        else:
            return False

    def send_encrypted_packet(self, handle, unencrypted_data):
        return self.send_BLE_packet(handle, self.encrypt(unencrypted_data))

    def read_encrypted_handle(self, handle):
        return self.decrypt(handle.read())

    def send_BLE_packet(self, handle, data):
        initial = time.time()
        while True:
            if time.time() - initial >= self.max_send_time:
                return False
            try:
                return handle.write(bytes(data), withResponse=True)
            except:
                self.connect()

    def encrypt(self, data):
        return self.reverse_byte_order(xxtea.encrypt(bytes(self.reverse_byte_order(data)), self.key, padding=False))

    def decrypt(self, encrypted_data):
        return self.reverse_byte_order(xxtea.decrypt(bytes(self.reverse_byte_order(encrypted_data)), self.key, padding=False))

    def reverse_byte_order(self, data):
        ba_data = bytearray(data)
        l = len(ba_data)

        #padding
        padding = bytearray(0)
        if l%4 != 0:
            padding = bytearray(4 - (l%4))
        ba_data = ba_data + padding
        l = len(ba_data)

        # reversing
        for i in range(l >> 2):
            s = ba_data[i*4:(i+1)*4]
            s.reverse()
            ba_data[i*4:(i+1)*4] = s
        return ba_data
