from confluent_kafka.admin import AdminClient

from mcp_kafka.service import KafkaMCPService

# Assume Kafka is running
KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'auto.offset.reset': 'earliest'
}

def test_describe_kafka_cluster():
    # TODO
    api = KafkaMCPService(admin_client=AdminClient(conf=KAFKA_CONFIG))
    assert isinstance(api.describe_cluster(), dict)