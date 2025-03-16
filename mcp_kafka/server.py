import logging
import os

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mcp_kafka.config import KafkaMCPConfiguration
from mcp_kafka.service import (KafkaBurrowMCPService, KafkaConnectMCPService,
                               KafkaCruiseControlMCPService, KafkaMCPService)

MCP_SERVER_NAME = "mcp-kafka"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(MCP_SERVER_NAME)
load_dotenv()
dependencies = [
    "python-dotenv",
    "uvicorn",
    "confluent-kafka",
    "requests"
]

mcp_server = FastMCP(MCP_SERVER_NAME, dependencies=dependencies)


config = KafkaMCPConfiguration()
config.kafka_client_configuration = {
    'bootstrap.servers': os.environ.get("KAFKA_BOOTSTRAP_SERVERS", None),
    'auto.offset.reset': 'earliest'
}
config.kafka_connect_api_url = os.environ.get("KAFKA_CONNECT_API_URL", None)
config.kafka_burrow_api_url = os.environ.get("KAFKA_BURROW_API_URL", None)
config.kafka_cruise_control_api_url = os.environ.get("KAFKA_CRUISE_CONTROL_API_URL", None)


@mcp_server.tool("Describe cluster")
def describe_kafka_cluster() -> dict:
    if config.kafka_client_configuration["bootstrap.servers"] is None:
        return {}

    admin_client = AdminClient(conf=config.kafka_client_configuration, logger=logger)
    api = KafkaMCPService(admin_client)
    return api.describe_cluster()

@mcp_server.tool("List topics")
def list_kafka_topics() -> dict:
    if config.kafka_client_configuration["bootstrap.servers"] is None:
        return {}

    admin_client = AdminClient(conf=config.kafka_client_configuration, logger=logger)
    api = KafkaMCPService(admin_client)
    return api.describe_topics()

@mcp_server.tool("List & describe consumer groups")
def list_kafka_consumer_groups() -> dict:
    if config.kafka_client_configuration["bootstrap.servers"] is None:
        return {}

    admin_client = AdminClient(conf=config.kafka_client_configuration, logger=logger)
    api = KafkaMCPService(admin_client)
    return api.describe_consumer_groups()

@mcp_server.tool("Publish message to Kafka topic")
def produce_kafka_message(topic: str, message: str) -> str:
    if config.kafka_client_configuration["bootstrap.servers"] is None:
        return ""

    producer = Producer(config.kafka_client_configuration)
    return KafkaMCPService(producer_client=producer).produce(topic, message)

@mcp_server.tool("Read messages from Kafka topic")
def consume_kafka_messages(topic: str, num_messages: int = 1, consumer_group: str = None) -> list:
    if config.kafka_client_configuration["bootstrap.servers"] is None:
        return []

    if consumer_group is not None:
        config.kafka_client_configuration['group.id'] = consumer_group

    consumer = Consumer(config.kafka_client_configuration)
    results = KafkaMCPService(consumer_client=consumer).consume(topic, num_messages, consumer_group)
    consumer.close()
    return results

@mcp_server.tool("Describe Connect connectors")
def list_kafka_connect_connectors() -> dict:
    if config.kafka_connect_api_url is None:
        return {}

    api = KafkaConnectMCPService(api_url=config.kafka_connect_api_url)
    return api.describe_connectors()

@mcp_server.tool("Describe Burrow group status")
def describe_burrow_consumer_group_status() -> dict:
    if config.kafka_burrow_api_url is None:
        return {}

    api = KafkaBurrowMCPService(api_url=config.kafka_burrow_api_url)
    return api.describe_consumer_group_status()

@mcp_server.tool("Get Cruise Control (CC) status")
def get_cruise_control_status() -> dict:
    if config.kafka_cruise_control_api_url is None:
        return {}

    api = KafkaCruiseControlMCPService(api_url=config.kafka_cruise_control_api_url)
    return api.get_status()


if __name__ == '__main__':
    mcp_server.run()