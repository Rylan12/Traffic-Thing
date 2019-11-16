import os
from time import sleep
import led
import paho.mqtt.client as MQTT

c = MQTT.Client()


def message_received(client, userdata, message):
    if 'state' in message.topic:
        payload = message.payload.decode('UTF-8')
        print('Message Received: ' + payload)
        if payload == 'ns':
            print('Switching N/S to green and E/W to red')
            led.control('green', 'on')
            led.control('red', 'off')
        elif payload == 'ew':
            print('Switching E/W to green and N/S to red')
            led.control('red', 'on')
            led.control('green', 'off')
    elif 'sensor' in message.topic:
        publish_message(message.payload.decode('UTF-8'))


def publish_message(direction):
    print('Car sensed in direction: ' + direction)
    c.publish('traffic/light/0/' + direction + '/sensed', None, qos=2, retain=True)


if __name__ == '__main__':
    c.connect('localhost', keepalive=60)
    c.loop_start()
    c.on_message = message_received
    c.subscribe([('traffic/light/+/state', 2), ('traffic/sensor', 2)])
    print('Intersection Manager')
    while True:
        pass
