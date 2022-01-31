"""
Used to run pipeline.
"""


from app.ingestors import ingest_point_counts, ingest_species_mapping
from app.adapters.storage import get_storage
from config import logger


def run():
    logger.info('[INIT] run()')
    ingest_species_mapping(storage_adapter=get_storage()).ingest()
    ingested_point_counts = ingest_point_counts(storage_adapter=get_storage())
    for count in ingested_point_counts:
        count.ingest()
    logger.info('[DONE] run()')


if __name__ == '__main__':
    run()
