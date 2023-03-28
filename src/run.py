"""
Ingest and transform point count data. Use flags to control behavior; use -p for a
production run and -t for a test (read-only) run.
"""

import time
from typing import Optional

from src.adapters.storage import get_storage
from src.compilers import factory_compile_point_counts
from src.ingestors import factory_ingest_point_counts, factory_ingest_species_names
from src.transformers import factory_transform_point_counts
from config import logger


class PointCountRunner:
    """Class to run ingestion and transformation for point count data."""

    def __init__(self, storage: Optional = None):
        """Initialize PointCountRunner instance.

        Args:
            storage: Storage adapter to write to;
        """
        self.storage = storage

    @staticmethod
    def point_count_etl(storage: Optional = None):
        """Run full point count ETL pipeline."""
        factory_ingest_species_names(storage=storage).ingest()
        ingested_point_counts = factory_ingest_point_counts(storage=storage)
        for count in ingested_point_counts:
            count.ingest()
        factory_compile_point_counts(storage=storage).compile()
        output = factory_transform_point_counts(storage=storage).transform()
        return output

    def run(self):
        """Run tasks."""
        logger.info(f'[START ] run() (Module: Point Count)')
        start = time.time()
        self.point_count_etl(storage=self.storage)
        logger.info(f'[DONE  ] run() (Module: Point Count, '
                    f'Runtime: {time.time() - start}s')


def factory(storage: str = None):
    """Factory to ingest and process point count data.

    Args:
        storage: Storage adapter to write results to; defaults to read-only.
    """
    storage = storage or get_storage()
    runner = PointCountRunner(storage=storage)

    return runner


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Ingest and process point count data")
    required = parser.add_argument_group('required_arguments')
    required.add_argument('-s', '--storage',
                          required=False, type=str,
                          help="String representation of storage adapter to use to "
                               "write results to file. Options -> 'local'; defaults "
                               "to read-only.")
    parser._action_groups.reverse()
    args = parser.parse_args()
    factory(storage=args.storage).run()
