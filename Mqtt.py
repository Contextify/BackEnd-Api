
import paho.mqtt.client as mqtt
import dbtest
import json
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
        #self.client.message_callback_add("sleep",self.on_sleep)

    def on_location(self,client, userdata, msg):
        print msg.topic+" "+str(msg.payload)
        data=json.loads(msg.payload)
        d={"User":data["User"],"State":data["State"],"Start":data["Timestamp"],"End":"None"}
        dbtest.update_prev_state(data)
        dbtest.write_location(d)

    def on_sleep(self,client,userdata,msg):
       print msg.topic+" "+str(msg.payload)
       data=json.loads(msg.payload)
       data["duration"]=data['Woke']-data['Sleep']
       dbtest.write_sleep(data)
       
    def run(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.client.disconnect()


m=MqttHandler()
m.run()