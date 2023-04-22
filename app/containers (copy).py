"""Containers module."""
import boto3
from dependency_injector import containers, providers
from .src.services import instance_data, instance_actions


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    session = providers.Resource(
        boto3.session.Session
    )

    ec2_client = providers.Resource(
        session.provided.client.call(),
        service_name='ec2',
        region_name=instance_data.REGION_NAME
    )

    instance_data = providers.Singleton(
        instance_data.InstanceData,
        ec2_client=ec2_client,
    )

    instance_actions = providers.Singleton(
        instance_actions.InstanceActions,
        ec2_client=ec2_client,
    )
