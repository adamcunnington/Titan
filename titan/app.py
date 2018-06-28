import json
import uuid

from azure.mgmt import containerinstance, resource
from azure.mgmt.containerinstance import models
from msrestazure import azure_active_directory
import flask


def get_id_token():
    return "Bearer %s" % flask.request.headers.get("X-MS-TOKEN-AAD-ID-TOKEN", "")


def get_security_context():
    # TODO: ENABLE THIS ONCE LIVE and delete the below. credentials = azure_active_directory.MSIAuthentication()
    # TODO: Enable this subscription_id = next(resource.SubscriptionClient(credentials).subscriptions.list())
    config = flask.current_app.config
    from azure.common.credentials import ServicePrincipalCredentials
    credentials = ServicePrincipalCredentials(client_id=config["TITAN_AZURE_CLIENT_ID"],
                                              secret=config["TITAN_AZURE_CLIENT_SECRET"],
                                              tenant=config["TITAN_AZURE_TENANT_ID"])
    return credentials, config["TITAN_AZURE_SUBSCRIPTION_ID"]


def list_blobs(service, container, prefix):
    marker = None
    while marker != "":
        response = service.list_blobs(container, prefix=prefix, marker=marker)
        marker = response.next_marker
        for blob in response:
            yield blob


def execute(details):
    config = flask.current_app.config
    container_name = config["TITAN_AZURE_CONTAINER_NAME"]
    launch_container(
        resource_group_name=config["TITAN_AZURE_CONTAINER_RSG_NAME"],
        container_group_prefix=container_name,
        os_type=config["TITAN_AZURE_CONTAINER_OS_TYPE"],
        location=config["TITAN_AZURE_CONTAINER_LOCATION"],
        container_name=container_name,
        image_name=config["TITAN_AZURE_CONTAINER_IMAGE_NAME"],
        image_registry_credentials=models.ImageRegistryCredential(config["TITAN_AZURE_CONTAINER_REGISTRY_SERVER"],
                                                                  config["TITAN_AZURE_CONTAINER_REGISTRY_USERNAME"],
                                                                  config["TITAN_AZURE_CONTAINER_REGISTRY_PASSWORD"]),
        memory_in_gb=config["TITAN_AZURE_CONTAINER_RAM_GB"],
        cpu_count=config["TITAN_AZURE_CONTAINER_CPU_COUNT"],
        configuration=details
    )


def format_execution(rows):
    arbitrary_row = rows[0]
    scheduled_execution_key = arbitrary_row["ScheduledExecutionKey"]
    prefix = "Scheduled" if scheduled_execution_key is not None else ""
    acquires = {}
    details = {
        "execution": {
            "ScheduledExecutionKey": scheduled_execution_key,
            "ExecutionClientName": arbitrary_row["%sExecutionClientName" % prefix],
            "ExecutionDataSourceName": arbitrary_row["%sExecutionDataSourceName" % prefix],
            "ExecutionDataSetName": arbitrary_row["%sExecutionDataSetName" % prefix],
            "ExecutionLoadDate": arbitrary_row["%sExecutionLoadDate" % prefix],
            "ExecutionUser": arbitrary_row["%sExecutionUser" % prefix],
            "AcquireProgramKey": arbitrary_row["AcquireProgramKey"]
        },
        "acquires": [],
        "extract": {
            "ExtractDestination": arbitrary_row["%sExtractDestination"  % prefix],
            "Options": {}
        } if arbitrary_row["%sExtractKey" % prefix] is not None else {}
    }
    for row in rows:
        acquire_key = row["%sAcquireKey" % prefix]
        if acquire_key is not None:
            acquire = acquires.get(acquire_key)
            if acquire is None:
                acquires[acquire_key] = {"Options": {}}
            acquire_option_name = row.get("%sAcquireOptionName" % prefix)
            if acquire_option_name is not None:
                acquire["Options"][acquire_option_name] = row["%sAcquireOptionValue" % prefix]
        extract_option_name = row.get("%sExtractOptionName" % prefix)
        if extract_option_name is not None:
            details["extract"]["Options"][extract_option_name] = row["%sExtractOptionValue" % prefix]
    details["acquires"].extend(acquires.values())
    return details


def launch_container(resource_group_name, container_group_prefix, os_type, location, container_name, image_name,
                     image_registry_credentials, memory_in_gb, cpu_count, configuration):
    container_group_name = "%s_%s" % (container_group_prefix, uuid.uuid4())
    configuration["execution"]["ExecutionContainerGroupName"] = container_group_name
    flask.current_app.logger.info("Preparing to launch container; %s" % container_group_name)
    resources = models.ResourceRequirements(requests=models.ResourceRequests(memory_in_gb=memory_in_gb, cpu=cpu_count))
    container = models.Container(name=container_name, image=image_name, resources=resources, command=["execute"],
                                 environment_variables=[models.EnvironmentVariable("TITAN_STDIN",
                                                                                   json.dumps(configuration))])
    container_group = models.ContainerGroup(containers=[container], os_type=os_type, location=location,
                                            restart_policy="Never",
                                            image_registry_credentials=[image_registry_credentials])
    credentials, subscription_id = get_security_context()
    client = containerinstance.ContainerInstanceManagementClient(credentials, subscription_id)
    client.container_groups.create_or_update(resource_group_name, container_group_name, container_group)
