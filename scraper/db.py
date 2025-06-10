from __future__ import annotations

import contextlib
import typing as t

import boto3
from botocore.exceptions import WaiterError
from mypy_boto3_dynamodb.service_resource import Table


@contextlib.contextmanager
def rankings_table(season: str, week: str) -> t.Iterator[Table]:
    """Set up a weekly rankings table in DynamoDB to store player ranks and points.

    The table will be created in DynamoDB with the name ``ff_{season}_{week}``.

    :param season: current season (i.e., ``2025``)
    :param week: current week (i.e., ``week_1``)
    """
    # Configure / create the weekly rankings table in DynamoDB
    table_name = f"ff_{season}_{week}"
    client = boto3.client("dynamodb")
    waiter = client.get_waiter("table_exists")
    try:
        # Check if table exists
        waiter.wait(
            TableName=table_name,
            WaiterConfig={
                "Delay": 0,
                "MaxAttempts": 1,
            },
        )
    except WaiterError:
        # If not, create it
        client.create_table(
            AttributeDefinitions=[
                {
                    "AttributeName": "name",
                    "AttributeType": "S",
                },
            ],
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "name",
                    "KeyType": "HASH",
                },
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        waiter.wait(TableName=table_name, WaiterConfig={"Delay": 5, "MaxAttempts": 25})

    # Yield the weekly rankings table
    resource = boto3.resource("dynamodb")
    yield resource.Table(table_name)

    # Close DynamoDB client
    client.close()
