from threading import Timer
import paho.mqtt.client as MQTT
from traffic import *

c = MQTT.Client()

intersections = [
    [Intersection(0, 0, 4, 0), Intersection(380, 0, 4, 1), Intersection(1143, 0, 4, 2), Intersection(1747, 0, 4, 3)],
    [Intersection(0, 340, 4, 4), Intersection(380, 340, 4, 5), Intersection(1143, 340, 4, 6), Intersection(1747, 340, 4, 7)],
    [Intersection(0, 688, 4, 8), Intersection(380, 688, 4, 9), Intersection(1143, 688, 4, 10), Intersection(1747, 688, 4, 11)],
    [Intersection(0, 1099, 4, 12), Intersection(380, 1099, 4, 13), Intersection(1143, 1099, 4, 14), Intersection(1747, 1099, 4, 15)]
]


# streets = [
#     Street(35, intersections[0], intersections[1])
# ]

# lights = {
#     0: [Light('n', 'r'), Light('e', 'g'), Light('s', 'r'), Light('w', 'g')],
#     1: [Light('n', 'r'), Light('e', 'g'), Light('s', 'r'), Light('w', 'g')]
# }


def get_seconds_to_intersection(intersection1, intersection2, speed_limit):
    length = abs((intersection1.x - intersection2.x) + (intersection1.y - intersection2.y))
    return length * 3600 / 5280 / speed_limit


def message_received(client, userdata, message):
    if "sensed" in message.topic:
        topic_info = message.topic.split("/")
        direction = topic_info[3]
        intersection_number = int(topic_info[2])
        row = intersection_number // 4
        column = intersection_number % 4

        print('Sensed car at intersection ' + str(intersection_number) + '. Allowing through.')
        publish_message(intersection_number, direction)

        # Get target intersection
        if direction == "n" and row < 3:
            target_intersection_number = intersection_number + 4
        elif direction == "s" and row > 0:
            target_intersection_number = intersection_number - 4
        elif direction == "e" and column < 3:
            target_intersection_number = intersection_number + 1
        elif direction == "w" and column > 0:
            target_intersection_number = intersection_number - 1
        else:
            # tell light to switch
            return

        # get distance
        time_til_destination = get_seconds_to_intersection(intersections[row][column],
                                                           intersections[target_intersection_number // 4][
                                                               target_intersection_number % 4], 35)
        notifying_time = time_til_destination - 3 if time_til_destination - 3 > 0 else 0

        print("Sensed car at " + str(intersection_number) + " going " + direction.upper() + " to " + str(
            target_intersection_number))
        print("It will take " + str(time_til_destination) + " seconds to get to intersection " + str(target_intersection_number))
        print("Notifying intersection " + str(target_intersection_number) + " in " + str(notifying_time) + " seconds.")
        t = Timer(notifying_time, publish_message, [target_intersection_number, direction])
        t.start()


def publish_message(intersection, direction):
    if direction == 'e' or direction == 'w':
        direction = 'ew'
    else:
        direction = 'ns'
    c.publish('traffic/light/' + str(intersection) + '/state', str(direction), qos=2, retain=True)


if __name__ == '__main__':
    c.connect('localhost', port=50001, keepalive=60)
    c.loop_start()
    c.on_message = message_received
    c.subscribe('traffic/#', qos=2)
    for row in range(len(intersections)):
        for column in range(len(intersections[row])):
            publish_message(row * 4 + column, 'n')
    while True:
        pass
    # message_received("", "", "traffic/light/0/e/sensed")
