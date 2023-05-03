from core.service.prediction_service import predict_stress_level
from core.service.opensearch_service import create_doc
import sys
sys.path.append("")


def data_automation(key):
    key = str(key).encode('utf-8')
    from kafka import KafkaConsumer
    from datetime import datetime
    import sys
    sys.path.append("")
    from core.service.config_service import read_config
    from core.service.identifier_generation_service import generate_hash_uid
    config = read_config()

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

                count += 1
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


# if __name__ == "__main__":
#     data_automation('user1')
