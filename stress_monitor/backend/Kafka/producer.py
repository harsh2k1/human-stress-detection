import json
from kafka import KafkaProducer
import sys
sys.path.append("")
from backend.services.config_service import read_config
config = read_config()


class Producer:
    def __init__(self, topic=config['KAFKA']['topic.name']) -> None:
        self.producer = KafkaProducer(bootstrap_servers=[f"{config['KAFKA']['producer.bootstrap.host']}:{config['KAFKA']['producer.bootstrap.port']}"],
                                      api_version=(3, 2, 1),
                                      value_serializer=lambda v: json.dumps(
            v).encode('utf-8'),
            acks='all',
            retries=3)
        self.topic = topic

    def send_msg(self, key, msg):
        key = json.dumps(key).encode('utf-8')
        print("sending message...")
        try:
            future = self.producer.send(self.topic, key=key, value=msg)
            # self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            # self.producer.close()
            return True
        except Exception as e:
            print(e)
            self.producer.close()
            return False
        except KeyboardInterrupt:
            self.producer.close()
            return

    def produce_from_csv(self,filepath, key=b'user1'):
        import pandas as pd

        df = pd.read_csv(filepath)
        data = df.iloc[:,0].to_list()
        count=0
        for val in data:
            if val>50:
                self.send_msg(key=key, msg=val)
                count += 1
        print(f"Dumped {count} values")

    def produce_from_vision(self):
        pass

    def produce_from_sensor(self):
        pass