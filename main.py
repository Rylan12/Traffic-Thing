import paho.mqtt.client as MQTT

lights = []

def message_received(client, userdata, message):
    if "sensed" in message.topic:
        topic_info = message.topic.split("/")
        print("Sensed car at " + topic_info[2] + " going " + topic_info[3].upper())
        # Calculate

def publish_message(c):
    c.publish('traffic/light/01/n/state', 'green')


if __name__ == '__main__':
    c = MQTT.Client()
    c.connect('localhost', port=1883, keepalive=60)
    c.loop_start()
    c.on_message = message_received
    c.subscribe('traffic/#')
    i = 0
    while True:
        if i % 100000000 == 0:
            publish_message(c)
        i += 1
