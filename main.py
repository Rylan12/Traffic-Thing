import paho.mqtt.client as MQTT
from time import sleep
from traffic import *

c = MQTT.Client()

intersections = [
    Intersection(0, 0, 4, 0),
    Intersection(380, 0, 4, 1)
]

streets = [
    Street(35, intersections[0], intersections[1])
]

lights = {
    0: [Light('n', 'r'), Light('e', 'r'), Light('s', 'r'), Light('w', 'r')],
    1: [Light('n', 'r'), Light('e', 'r'), Light('s', 'r'), Light('w', 'r')]
}


def get_seconds_to_intersection(street):
    # return street.speedLimit * 5280 * 1000 / 3600 / street.length
    return street.length * 3600 / 5280 / street.speedLimit


def message_received(client, userdata, message):
    if "sensed" in message.topic:
        topic_info = message.topic.split("/")
        intersection = topic_info[2]
        direction = topic_info[3]
        time_til_destination = get_seconds_to_intersection(streets[0])
        print("Sensed car at " + intersection + " going " + direction.upper())
        print("It will take " + str(time_til_destination) + " seconds to get to intersection 2")
        sleep(time_til_destination)
        publish_message()


def publish_message():
    c.publish('traffic/light/01/n/state', 'green')


if __name__ == '__main__':
    c = MQTT.Client()
    c.connect('localhost', port=1883, keepalive=60)
    c.loop_start()
    c.on_message = message_received
    c.subscribe('traffic/#')
    while True:
        pass
