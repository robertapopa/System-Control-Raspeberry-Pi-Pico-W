from mfrc522 import MFRC522 
import utime
from machine import Pin
import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

lock =Pin(28,Pin.OUT)
GLed =Pin(19,Pin.OUT)
buzzer = Pin(27, Pin.OUT)
RLed =Pin(18,Pin.OUT)

lock.value(1)
buzzer.value(0)
RLed.value(0)
GLed.value(0)

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

keyPad =[['1', '2', '3'],
               ['4', '5', '6'],
               ['7', '8', '9'],
               ['*', '0', '#']]

rowPins = [15,14,13,12]
colPins = [11,10,9]

colValue = []
rowValue = []

password = []
setPassword = ['1','2','3','4']   
 
for i in range(0, 4):  
    rowValue.append(Pin(rowPins[i], Pin.OUT))
    rowValue[i].value(1)
for i in range(0, 3):  
    colValue.append(Pin(colPins[i], Pin.IN, Pin.PULL_DOWN))
    colValue[i].value(0)


def checkKeyPress():
    for row in range(4):  
        for col in range(3): 
            rowValue[row].high()
            if colValue[col].value() == 1:
                print("Tastă apasată:", keyPad[row][col])
                key_press = keyPad[row][col]
                utime.sleep(0.3)
                password.append(key_press)
            if len(password) == 4:
                checkPassword(password)
                for x in range(0, 4):
                    password.pop() 
        rowValue[row].low()


failed_attempts = 0  
max_attempts = 3  

def checkPassword(password):
    global failed_attempts
    RLed.value(0)  
    if password == setPassword:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Acces Deblocat!")
        lock.value(0)  
        GLed.value(1)  
        utime.sleep(2)
        lock.value(1)  
        lcd.clear()
        lcd.putstr("Card sau pin:")
        GLed.value(0)  
        failed_attempts = 0  
    else:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Acces Respins!")
        buzzer.value(1)
        RLed.value(1)  
        utime.sleep(2)
        buzzer.value(0)
        RLed.value(0)  
        lcd.clear()
        lcd.putstr("PIN Incorect")
        lcd.move_to(0, 1)
        lcd.putstr("Incearca din nou")
        utime.sleep(2)
        lcd.clear()
        lcd.putstr("Introduceti")
        lcd.move_to(0, 1)
        lcd.putstr("parola:")
        failed_attempts += 1
        if failed_attempts >= max_attempts:
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Prea multe")
            lcd.move_to(0, 1)
            lcd.putstr("pin-uri gresite!")
            utime.sleep(2)
            machine.reset()  


print("Introduceți parola:")

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
                  
rc522 = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

lcd.clear()
lcd.move_to(0,0)
lcd.putstr("Proiect")  
utime.sleep(3)
lcd.clear()
lcd.putstr("Card sau pin:")

while True:
    checkKeyPress()
    (stat, tag_type) = rc522.request(rc522.REQALL)

    if stat == rc522.OK:
        (status, raw_uid) = rc522.SelectTagSN()
        if stat == rc522.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            # print("Card detectat! Adresa: {}".format(rfid_data))

            if rfid_data == "739cd1aa":
                
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr("RFID corect")
                lcd.move_to(0, 1)
                lcd.putstr("Deblocat!")
                lock.value(0)
                GLed.value(1)
                utime.sleep(5)
                lcd.clear()
                lcd.putstr("Card sau pin:")
                lock.value(1)
                GLed.value(0)
                               
                            
            else:
                
                lcd.move_to(0,0)
                lcd.clear()
                lcd.putstr("RFID gresit")
                lcd.move_to(0, 1)
                lcd.putstr("Respins!")
                buzzer.value(1)
                RLed.value(1)
                utime.sleep(3)
                lcd.clear()
                lcd.putstr("Card sau pin:")
                buzzer.value(0)
                RLed.value(0)