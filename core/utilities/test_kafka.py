from kafka import KafkaConsumer, KafkaProducer
from argparse import ArgumentParser

import sys
sys.path.append("")
from core.service.config_service import read_config
config = read_config()

parser = ArgumentParser()
parser.add_argument('-t','--topic', help="Topic name", default=config['KAFKA']['topic.name'])

args = vars(parser.parse_args())

def produce_data(topic, message):
    # create a Kafka producer instance
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    # produce a message to the topic
    # message = b'Hello, Kafka!'
    # message = str(3.14).encode('utf-8')
    print("sending message")
    producer.send(topic, key=b'secret1', value=message)
    print("done")

    # wait for any outstanding messages to be delivered and delivery reports received
    producer.flush()

    # close the producer instance
    producer.close()


def consume_data(topic):
    # Set up Kafka consumer
    consumer = KafkaConsumer(
        topic,                  # Topic name
        bootstrap_servers=['localhost:9092'],  # Kafka broker address
        auto_offset_reset='earliest',  # Start from the earliest available message
        enable_auto_commit=True,       # Commit offsets automatically
        group_id='my-group')           # Consumer group ID

    # Consume messages from the topic
    print("receiving message")
    for message in consumer:
        print(message.key, message.value)
        # yield {'key':message.key, 'message': message.value}


if __name__ == "__main__":
    # produce_data(topic=args['topic'])
    try:
        consume_data(topic=args['topic'])
    except KeyboardInterrupt:
        sys.exit(0)
