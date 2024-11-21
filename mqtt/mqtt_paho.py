from . import mqtt_client
from . import random
from . import time
from . import datetime, timedelta
from . import re


class mqtt_paho:
    def __init__(self):
        self.broker = None
        self.port = None
        self.username = None
        self.password = None
        self.client = None

        self.received_message = None

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.disconnect()

    def reset_client(self):
        self.client = None

    def set_mqtt_broker(self,broker):
        self.broker = str(broker)
        self.reset_client()
    
    def set_mqtt_port(self,port):
        try:
            self.port = int(port)
        except ValueError:
            print("Invalid port value")
        self.reset_client()
    
    def set_mqtt_username(self, username):
        self.username = str(username)
        self.reset_client()
    
    def set_mqtt_password(self, password):
        self.password = str(password)
        self.reset_client()
    
    def check_param(self):
        if None in (self.broker, self.port, self.username, self.password):
            return False
        return True

    def connect_mqtt(self):
        if not self.check_param():
            print("[INFO] Set mqtt details")
            return
        if self.client is None:
            def on_connect(client, userdata, flags, rc, properties=None):
                if rc == 0:
                    print("Connected to MQTT Broker!")
                else:
                    print(f"Failed to connect, return code {rc}\n")
            
            self.client = mqtt_client.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt_client.MQTTv5)
            self.client.username_pw_set(self.username, self.password)
            self.client.on_connect = on_connect
            self.client.connect(self.broker,self.port)
        
        return self.client
    
    def publish_message(self, topic, message):
        if self.client is None:
            self.client = self.connect_mqtt()

        timestamp = datetime.now().isoformat()  # Current time in ISO format
        return_date = (datetime.now() + timedelta(days=5)).isoformat()  # Return date after 5 days

        # Set up user properties
        user_properties = [
            ("timestamp", timestamp),
            ("return_date", return_date)
        ]

        properties = mqtt_client.Properties(mqtt_client.PacketTypes.PUBLISH)
        properties.UserProperty = user_properties

        self.client.loop_start()
        result = self.client.publish(topic, message, qos=2, retain=True, properties=properties)
        self.client.loop_stop()

        if result[0] == 0:
            print(f"Successfully Registered books\n\n")
        else:
            print(f"Failed to Register books")
        time.sleep(0.1)
    
    def subscribe_to_topic(self, topic_name):
        if self.client is None:
            self.client = self.connect_mqtt()

        self.received_message = None


        def on_message(client, userdata, msg):
            self.received_message = msg.payload.decode()

        
        # Subscribe to the specified topic
        self.client.loop_start()
        self.client.subscribe(topic_name)
        self.client.on_message = on_message
        # Keep the client running indefinitely
        time.sleep(1)
        return (self.received_message)  
        

    def unsubscribe_from_topic(self, topic_name):
        self.client = self.connect_mqtt()
        result = self.client.unsubscribe(topic_name)

        if result[0] == 0:
            print(f"Successfully unsubscribed from topic `{topic_name}`")
        else:
            print(f"Failed to unsubscribe from topic `{topic_name}`")

    def disconnect(self):
        if self.client is not None:
            self.client.disconnect()
            print("Disconnected from MQTT Broker")

    def message_book_code(self,book_codes, issue_date, return_date):        
        messages = []
        
        for i, code in enumerate(book_codes):
            message = f"BookCode: {code}, IssueDate: {issue_date[i]}, ReturnDate: {return_date[i]}"
            messages.append(message)
        
        return messages

    def extract_book_details(self, message):
        # Regular expressions to match BookCode, IssueDate, and ReturnDate
        book_code_pattern = r"ESE\d{6}"
        issue_date_pattern = r"IssueDate: (\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})"
        return_date_pattern = r"ReturnDate: (\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})"

        # Extract details from the message
        book_ids = re.findall(book_code_pattern, message)
        issue_dates = re.findall(issue_date_pattern, message)
        return_dates = re.findall(return_date_pattern, message)

        return (book_ids, issue_dates, return_dates)