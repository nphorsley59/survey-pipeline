"""
Used to run pipeline.
"""


from app.adapters.storage import get_storage
from app.ingestors import factory_ingest_point_counts, factory_ingest_species_map
from config import logger


def run():
    logger.info('[INIT] run()')
    factory_ingest_species_map(storage_adapter=get_storage()).ingest()
    ingested_point_counts = factory_ingest_point_counts(storage_adapter=get_storage())
    for count in ingested_point_counts:
        count.ingest()
    logger.info('[DONE] run()')


if __name__ == '__main__':
    run()
