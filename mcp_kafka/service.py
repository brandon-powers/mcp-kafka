import requests


class KafkaMCPService:
    def __init__(self, admin_client=None, consumer_client=None, producer_client=None, request_timeout=10):
        self.admin_client = admin_client
        self.consumer_client = consumer_client
        self.producer_client = producer_client
        self.request_timeout = request_timeout

    def consume(self, topic, num_messages, consumer_group):
        self.consumer_client.subscribe([topic])

        messages = []
        for _ in range(num_messages):
            msg = self.consumer_client.poll(1.0)

            if msg is None:
                break

            messages.append(msg.value().decode('utf-8'))

        return messages

    def produce(self, topic, message):
        def delivery_report(err, msg):
            if err is not None:
                return f'Message delivery failed: {err}'
            else:
                return f'Message delivered to {msg.topic()} [{msg.partition()}]'

        self.producer_client.produce(topic, message.encode('utf-8'), callback=delivery_report)
        self.producer_client.flush()

        return f"Message published to topic '{topic}'"

    def describe_cluster(self):
        try:
            cluster_metadata = self.admin_client.describe_cluster().result(timeout=self.request_timeout)
        except TimeoutError as error:
            return {"error": f"Timed out: {error}"}
        except Exception as error:
            return {"error": f"Failed: {error}"}

        if cluster_metadata is None:
            return {}

        broker_metadata = []

        for broker in cluster_metadata.nodes:
            broker_metadata.append({
                "id": broker.id_string,
                "host": broker.host,
                "port": broker.port,
                "rack": broker.rack
            })

        return {
            "cluster_id": cluster_metadata.cluster_id,
            "controller": {
                "id": cluster_metadata.controller.id_string,
                "host": cluster_metadata.controller.host,
                "port": cluster_metadata.controller.port,
                "rack": cluster_metadata.controller.rack
            },
            "brokers": broker_metadata,
            "authorized_operations": cluster_metadata.authorized_operations
        }

    def describe_topics(self) -> dict:
        #self.admin_client.describe_topics()
        topics = self.admin_client.list_topics().result()
        return topics

    def describe_consumer_groups(self) -> dict:
        try:
            consumer_groups = self.admin_client.list_consumer_groups().result().valid
        except TimeoutError as error:
            return {"error": f"Timed out: {error}"}
        except Exception as error:
            return {"error": f"Failed: {error}"}

        group_ids = []
        consumer_group_description = {}

        for group in consumer_groups:
            group_ids.append(group.group_id)

            consumer_group_description[group.group_id] = {
                "group_id": group.group_id,
                "is_simple_consumer_group": group.is_simple_consumer_group,
                "state": group.state.name,
                "type": group.type.name
            }

        try:
            consumer_group_details = self.admin_client.describe_consumer_groups(
                group_ids=group_ids,
                include_authorized_operations=True
            )

            for gid, cgd in consumer_group_details.items():
                consumer_group_details[gid] = cgd.result()
        except TimeoutError as error:
            return {"error": f"Timed out: {error}"}
        except Exception as error:
            return {"error": f"Failed: {error}"}

        for group_id, details in consumer_group_details.items():
            consumer_group_description[group_id].update({
                "partition_assignor": details.partition_assignor,
                "group_coordinator": {
                    "id": details.coordinator.id_string,
                    "host": details.coordinator.host,
                    "port": details.coordinator.port,
                    "rack": details.coordinator.rack
                },
                #"assigned_topic_partition_members": cg_detail.members, # TODO list(MemberDescription)
                "authorized_operations": ",".join([acl.name for acl in details.authorized_operations])
            })

        return consumer_group_description

    def describe_delegation_tokens(self):
        pass

    def describe_log_dirs(self):
        pass

    def describe_configs(self):
        pass

    def describe_acls(self):
        pass


class KafkaConnectMCPService:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_cluster_info(self):
        pass

    def get_config(self):
        pass

    def get_connectors(self):
        return requests.get(self.api_url + "/connectors?expand_status=true&expand_info=true")

    def get_connector_plugins(self):
        pass

    def get_loggers(self):
        pass


class KafkaBurrowMCPService:
    def __init__(self, api_url):
        self.api_url = api_url

    def burrow_healthcheck(self):
        pass

    def list_clusters(self):
        pass

    def describe_cluster(self, cluster: str):
        pass

    def list_consumers_with_group_detail(self):
        pass

    def list_topics(self):
        pass

    def check_burrow_consumer_group_status(self, consumer_group_id):
        pass


class KafkaCruiseControlMCPService:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_cruise_control_state(self):
        pass

    def get_cluster_load(self):
        pass

    def get_partition_resource_utilization_and_load(self):
        pass

    def get_partition_and_replica_state(self):
        pass

    def get_optimization_proposals(self):
        pass

    def get_user_request_result(self):
        pass