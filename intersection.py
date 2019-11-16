import os
from time import sleep

import paho.mqtt.client as MQTT

c = MQTT.Client()


def message_received(client, userdata, message):
    if 'state' in message.topic:
        payload = message.payload.decode('UTF-8')
        print('Message Received: ' + payload)
        if payload == 'ns':
            print('Switching N/S to green and E/W to red')
            os.system('/opt/vc/bin/vcmailbox 0x00038041 8 8 130 1 >/dev/null')
        elif payload == 'ew':
            print('Switching E/W to green and N/S to red')
            os.system('/opt/vc/bin/vcmailbox 0x00038041 8 8 130 0 >/dev/null')
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
