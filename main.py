import dlt
from dlt.sources.sql_database import sql_database

def load_tables_family_and_genome():

    # Create a dlt source that will load tables "family" and "genome"
    source = sql_database().with_resources("family", "genome")

    # only load rows whose "updated" value is greater than the last pipeline run
    source.family.apply_hints(incremental=dlt.sources.incremental("updated"))
    source.genome.apply_hints(write_disposition="replace") # replace the whole table on each run
    # Create a dlt pipeline object
    pipeline = dlt.pipeline(
        pipeline_name="sql_to_duckdb_pipeline", # Custom name for the pipeline
        destination="duckdb", # dlt destination to which the data will be loaded
        dataset_name="sql_to_duckdb_pipeline_data" # Custom name for the dataset created in the destination
    )

    # Run the pipeline
    load_info = pipeline.run(source, write_disposition="replace")

    # Pretty print load information
    print(load_info)

if __name__ == '__main__':
    load_tables_family_and_genome()
