"""
This script is used to run pipeline tasks.
"""


from typing import Optional


from app.adapters.storage import get_storage
from app.compilers import factory_compile_point_counts
from app.ingestors import factory_ingest_point_counts, factory_ingest_species_names
from app.transformers import factory_transform_point_counts
from config import logger


def run(storage: Optional = None):
    """Run full ETL pipeline."""
    storage = storage or get_storage()
    logger.info('[INIT] run()')
    factory_ingest_species_names(storage=storage).ingest()
    ingested_point_counts = factory_ingest_point_counts(storage=storage)
    for count in ingested_point_counts:
        count.ingest()
    factory_compile_point_counts(storage=storage).compile()
    factory_transform_point_counts(storage=storage).transform()
    logger.info('[DONE] run()')


if __name__ == '__main__':
    run()
