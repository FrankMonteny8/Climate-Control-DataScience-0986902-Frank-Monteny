import Adafruit_DHT as DHT
import RPi.GPIO as GPIO
import time
import urllib.request
import requests

# set everuthing up 
running = True
sensor = DHT.DHT11
DHT11_pin = 4
MOTOR = 25
RAIN_SENSOR = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(MOTOR, GPIO.OUT)
GPIO.setup(RAIN_SENSOR, GPIO.IN)
p = GPIO.PWM(MOTOR, 50)
p.start(2.5)

def thingspeakPost(temp, humid):
    # create a url with temperature, humidity and the rain sensor
    temperature = temp
    humidity = humid
    URL="https://api.thingspeak.com/update?api_key="
    KEY="UGL7N292WW3OGDSJ"
    HEADER="&field1={}&field2={}&field3={}".format(temperature, humidity, GPIO.input(RAIN_SENSOR))
    new_URL=URL+KEY+HEADER
    data=urllib.request.urlopen(new_URL)

def openDoor():
    # go back to neutral
    p.ChangeDutyCycle(2.5)
    pass

def closeDoor():
    # rotate 90 degrees to the left
    p.ChangeDutyCycle(7.5)
    pass

def moveDoor(temperature, humidity):
    # flag is a flag wether the door should open or not
    # true means open and false means close

    # if humidity is between 70 and 90 percent open the door otherwise close the door
    if(humidity > 70):
        flag = True
    elif(humidity > 90):
        flag = False
        time.sleep(0.5)
    else:
        flag = False
        time.sleep(0.5)

    # if humidity is between 21 and 30 degrees Celsius open the door otherwise close the door
    if(temperature > 21):
        flag = True
        time.sleep(0.5)
    elif(temperature > 30):
        flag = False
        time.sleep(0.5)
    else:
        flag = False
        time.sleep(0.5)

    # if the Raspberry pi reads a 1 from RAIN_SENSOR its not raining so open the door
    if(GPIO.input(RAIN_SENSOR) == True):
        flag = True
        time.sleep(0.5)

    if(flag == True):
        openDoor()
    else:
        closeDoor()

def main():
    # As long as running is True keep checking humidity and temperature
    # And after that the RAIN_SENSOR
    # if humidity and temperature have a value print it and also for the rain sensor
    while running == True:
        humidity, temperature = DHT.read_retry(sensor, DHT11_pin)
        if humidity is not None and temperature is not None:
            print("Temperature={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
            thingspeakPost(temperature, humidity)
            moveDoor(temperature, humidity)
        else:
            print("Geen waardes")

        if GPIO.input(RAIN_SENSOR):
            print("Het regent niet")
        else:
            print("Het regent")

        
    
def destroy():
    #stop the motor and the door
    p.stop()
    
    # safely stop GPIO
    GPIO.cleanup() 

if __name__ == '__main__':
    try:
            main()
    #when 'Ctrl+C' is pressed, destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
    except Exception:
        destroy()

    

        
        
