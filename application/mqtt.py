
import paho.mqtt.client as mqtt
import dbtest
import json,arrow
import logger

class MqttHandler():
    def __init__(self):
        self.username = "sriramsv"
        self.password = "gooddeeds"
        self.server = "m11.cloudmqtt.com"
        self.port = 13993
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.server,self.port, keepalive=60, bind_address="")
        self.client.subscribe("#", qos=1)
        self.client.message_callback_add("location",self.on_location)

    def on_location(self,client, userdata, msg):
        data=json.loads(msg.payload)
        d={"User":data["User"],"State":data["State"],"Start":data["Timestamp"],"Startdate":arrow.get(data["Timestamp"]).datetime,"End":"None"}
        dbtest.update_prev_state(data)
        dbtest.write_location(d)


    def run(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.client.disconnect()


m=MqttHandler()
m.run()
