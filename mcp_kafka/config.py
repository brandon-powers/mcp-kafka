import dataclasses
from typing import Any


@dataclasses.dataclass
class KafkaMCPConfiguration:
    kafka_client_configuration: dict[str, Any]
    kafka_connect_api_url: str
    kafka_burrow_api_url: str
    kafka_cruise_control_api_url: str


