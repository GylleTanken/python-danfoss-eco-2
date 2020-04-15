# python-danfoss-eco-2
A simple Python API for controlling Danfoss eco 2. I have developed it using a Raspberry Pi.

## Requirements
 - Python 3
 - bluepy (https://github.com/IanHarvey/bluepy)
 - xxtea (https://github.com/ifduyue/xxtea)
 - Linux (Since bluepy only runs on linux)

## Install
Clone the repository 
```
git clone https://github.com/GylleTanken/python-danfoss-eco-2.git
cd python-danfoss-eco-2
python3 setup.py install 
```
If it fails find a way to install each requirement (bluepy and xxtea).

## Example use
This will connect to the danfoss eco with the "mac" address "00:11:22:33:44:55" and encryption key "AABBCCDDEEFF112233445566778899AA" (hex values), print the device name, print the battery level, print the current temperature and set the temperature to 22 degrees celcius.
The code will automaticly connect to the devic and login in the 'with' statement, and automaticly disconnect in the end of the 'with' block.  
Currently the only supported pin code is 0000, which is the default.

```python
import DanfossEco2

thermostat = DanfossEco2.DanfossEco2("00:11:22:33:44:55", encryption_key= b'\xAA\xBB\xCC\xDD\xEE\xFF\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA')
with thermostat:
    print("Device name: " + thermostat.getDeviceName())
    print("Battery level: " + str(thermostat.getBattery()))
    print("Current temperature: " + str(thermostat.getTemperature()))
    thermostat.setTemperature(22)
```

Note: This code has not been tested.

## Getting the encyption key.
To get the encryption key, it is probably easiest to use a mobile phone app like nRF Connect https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Connect-for-mobile. But any software which can read a characteristic with a given UUID.
This is the procedure to read the encyption key
 - Press the button on the DanfossEco2 (The button with a clock symbol)
 - Connect to the device
 - Read the characteristic with the UUID: "1002000B-2749-0001-0000-00805F9B042F"
   - This is only available when the button has been pressed.
   - The characteristic is part of the service with the UUID: "10020000-2749-0001-0000-00805F9B042F"
 - You should now have the encryption key.

## Thanks
Thanks to https://github.com/dsltip/Danfoss-BLE for doing a lot of the hard work, especially figuring out how to get the encyption key and which encryption method the device uses.

