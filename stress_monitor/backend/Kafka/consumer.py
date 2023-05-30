from backend import read_config
import json
from kafka import KafkaConsumer

config = read_config()

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
    
    @staticmethod
    async def data_automation(key):
        key = json.dumps(key).encode('utf-8')
        from kafka import KafkaConsumer
        from datetime import datetime
        from backend import config, generate_hash_uid, create_doc, predict_stress_level
        

        consumer = KafkaConsumer(
            config['KAFKA']['topic.name'],
            bootstrap_servers=[
                f"{config['KAFKA']['producer.bootstrap.host']}:{config['KAFKA']['producer.bootstrap.port']}"],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group')

        # Consume messages from the topic
        print("receiving message")
        count = 0
        prev_data = {key: []}
        try:
            for message in consumer:

                if message.key == key:
                    print(key,': ', message.value)
                    count += 1
                    now = datetime.utcnow()
                    now = now.strftime("%Y-%m-%d %H:%M:%S")
                    record = {
                        "timestamp": now,
                        "userid": key.decode('ascii'),
                        "heartRate": float(message.value)
                    }
                    create_doc(_id=generate_hash_uid(str(record)),
                            body=record, _index=config['OPENSEARCH']['index'])

                    prev_data[key].append(float(message.value))

                    if count == 100:
                        stress_level = predict_stress_level(prev_data[key])
                        count = 0
                        prev_data[key] = []

                        now = datetime.utcnow()
                        now = now.strftime("%Y-%m-%d %H:%M:%S")

                        record = {
                            "timestamp": now,
                            "userid": key.decode('ascii'),
                            "stressLevel": float(stress_level)
                        }
                        create_doc(_id=generate_hash_uid(str(record)),
                                body=record, _index=config['OPENSEARCH']['index'])
                        print("Stress Indexed")

        except KeyboardInterrupt:
            return
