from core.service.config_service import read_config
import json
from kafka import KafkaProducer, KafkaConsumer

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
        print("sending message...")
        try:
            future = self.producer.send(self.topic, key=key, value=msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            self.producer.close()
            return True
        except Exception as e:
            print(e)
            self.producer.close()
            return False


class Consumer:
    def __init__(self, topic=config['KAFKA']['topic.name']) -> None:
        self.consumer = KafkaConsumer(
            bootstrap_servers=[f"{config['KAFKA']['producer.bootstrap.host']}:\
                                                         {config['KAFKA']['producer.bootstrap.port']}"],
            consumer_timeout_ms=60000,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('ascii')))

        self.topic = topic

    def listen(self):
        self.consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in self.consumer:
                if message is None or message.value is None:
                    print("Empty Queue")
                    return

                self.consumer.commit()
                print(message)
                yield {'key': message.key, 'message': message.value}
        except Exception as e:
            print(e)
            self.consumer.close()
            return None
        finally:
            self.consumer.close()

    def get_record_count(self):
        self.consumer.subscribe(self.topic)
        count = sum(1 for _ in self.consumer)
        print(count)
        return count
