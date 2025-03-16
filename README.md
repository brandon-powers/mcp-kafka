# Overview

**`mcp-kafka`** is a server-side implementation of the **[model context protocol (MCP)](https://spec.modelcontextprotocol.io/specification/2024-11-05/)** for **[Apache Kafka](https://github.com/apache/kafka)**. It allows language models (LLM/SLM) to reliably interact with Kafka & its ecosystem, including **[Kafka Connect](https://github.com/apache/kafka/tree/trunk/connect)**, **[Burrow](https://github.com/linkedin/Burrow)**, & **[Cruise Control](https://github.com/linkedin/cruise-control)**.

**NOTE:** This is a WIP, changes/potential errors are expected.

## Features

The server supports capabilities based on the [core Kafka APIs](https://kafka.apache.org/documentation/#api), excluding Streams (for now), along with the [Burrow](https://github.com/linkedin/Burrow/wiki/HTTP-Endpoint) & [Cruise Control](https://github.com/linkedin/cruise-control/wiki/rest-apis) REST APIs.

TODO
- [ ] Use `asyncio` and `aiohttp`.
- [ ] Set env config values in the data class.
- [ ] Finish admin/consumer/producer API support.
- [ ] Support Burrow API.
- [ ] Support CC API.
- [ ] Service + integration tests.
- [ ] Publish to PyPI (`uv pip install mcp-kafka`)
- [ ] Test Dockerfile & push to Dockerhub (`docker pull bkpowers/mcp-kafka`)
- [ ] Usage/config/deployment options + demo in README.
- [ ] Consider Strimzi/kcctl integrations.
- [ ] Prompts with auto-complete support for certain resources/tools.

### MCP Capabilities

#### Tools

##### Kafka
- `consume`
- `produce`
- `describe_kafka_cluster`
- `describe_kafka_topics`
- `describe_kafka_consumer_groups`
- `describe_kafka_delegation_tokens`
- `describe_kafka_log_dirs`
- `describe_kafka_configs`
- `describe_kafka_acls`

##### Kafka Connect
- `get_kafka_connect_cluster_info`
- `get_kafka_connect_config`
- `get_kafka_connect_connectors`
- `get_kafka_connect_connector_plugins`
- `get_kafka_connect_loggers`

##### Burrow
- `burrow_healthcheck`
- `burrow_list_clusters`
- `burrow_describe_cluster`
- `burrow_list_consumers_with_group_detail`
- `burrow_list_topics`
- `burrow_check_consumer_group_status`

##### Cruise Control
- `cruise_control_get_state`
- `cruise_control_get_kafka_cluster_load`
- `cruise_control_get_partition_resource_utilization_and_load`
- `cruise_control_get_partition_and_replica_state`
- `cruise_control_get_optimization_proposals`
- `cruise_control_get_user_request_result`

#### Resources

- topic, connector, consumer group

#### Prompts

## Usage / Configuration

1. Claude Desktop
2. Cursor
3. Windsurf
4. Langchain MCP adapter
5. Azure OpenAI

### Environment Variables

Supported APIs are (currently) enabled by the presence of their specific environment variable. If none are present, the server responds as empty. If 1 or more variables are present, then the respective tools are also present.

* `KAFKA_BOOTSTRAP_SERVERS`: Kafka Admin, Consumer, Producer APIs
* `KAFKA_CONNECT_API_URL`: Kafka Connect API
* `KAFKA_BURROW_API_URL`: Burrow API
* `KAFKA_CRUISE_CONTROL_API_URL`: Cruise Control API

