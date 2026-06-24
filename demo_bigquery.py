"""
dlt BigQuery destination example.

Setup:
    uv add "dlt[bigquery]" pydantic

Credentials (choose one):

Option A — secrets.toml (.dlt/secrets.toml):
    [destination.bigquery.credentials]
    project_id = "your-project-id"
    private_key = "-----BEGIN RSA PRIVATE KEY-----\n..."
    client_email = "your-sa@your-project.iam.gserviceaccount.com"

Option B — env var (JSON string of service account key):
    export DESTINATION__BIGQUERY__CREDENTIALS='{"type":"service_account","project_id":...}'

Option C — Application Default Credentials (gcloud auth application-default login):
    No config needed, dlt picks up ADC automatically.
"""

from typing import Literal, Optional

import dlt
from pydantic import BaseModel

from dlt.common.pipeline import LoadInfo


class User(BaseModel):
    id: int
    name: str
    role: Literal["admin", "viewer", "editor"]
    email: Optional[str] = None


# Passing the pydantic model as `columns=` makes dlt validate every row against it
# and infer the table schema (types, nullability) from the model.
# `schema_contract={"data_type": "freeze"}` raises if an incoming value can't be
# coerced to the declared type instead of silently evolving the schema.
@dlt.resource(
    write_disposition="replace",
    table_name="users",
    columns=User,
    schema_contract={"data_type": "freeze"},
)
def users():
    records = [
        {"id": 1, "name": "Alice", "role": "admin", "email": "alice@example.com"},
        {"id": 2, "name": "Bob",   "role": "viewer", "email": "bob@example.com"},
        {"id": 3, "name": "Carol", "role": "editor", "email": "carol@example.com"},
        {"id": 4, "name": "Mark", "role": "viewer", "email": "mark@example.com"},
    ]
    for record in records:
        yield record


@dlt.source
def my_source():
    return users()


def table_schema_changed_list(load_info: LoadInfo):
    results = []
    # Iterate over each package in the load_info object
    for package in load_info.load_packages:
        # Iterate over each table in the schema_update of the current package
        for table_name, table in package.schema_update.items():
            # Iterate over each column in the current table
            for column_name, column in table["columns"].items():
                results.append(
                    f"Table updated: {table_name}: Column changed: {column_name}: {column['data_type']}"
                )
    return results


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="bigquery_demo",
        destination="bigquery",
        dataset_name="temporary",
    )

    load_info = pipeline.run(my_source())
    print(load_info)
    print(table_schema_changed_list(load_info))

