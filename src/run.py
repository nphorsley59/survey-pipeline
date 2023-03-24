"""
Ingest and transform point count data. Use flags to control behavior; use -p for a
production run and -t for a test (read-only) run.
"""


import sys
import time
from typing import Optional


from app.adapters.storage import get_storage
from app.compilers import factory_compile_point_counts
from app.ingestors import factory_ingest_point_counts, factory_ingest_species_names
from app.transformers import factory_transform_point_counts
from config import logger


class PointCountRunner:
    """Class to run ingestion and transformation for point count data."""

    def __init__(self, mode: str, storage: Optional = None):
        """Initialize PointCountRunner instance.

        Args:
            mode (str): Run mode; use -p for a production run and -t for a test
                (read-only) run.
            storage: Storage adapter to write to.
        """
        self.mode = mode
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
        logger.info(f'[START ] run() (Module: Point Count, Mode: {self.mode})')
        start = time.time()
        match self.mode:
            case '-p':
                self.point_count_etl(storage=self.storage)
            case '-t':
                result = self.point_count_etl()
                print(result.sample(5))
            case _:
                raise ValueError("Invalid run() mode.")
        logger.info(f'[DONE  ] run() (Module: Point Count, '
                    f'Runtime: {time.time() - start}s')


def factory_point_count_runner(mode: str, storage: Optional = None):
    """Factory to run ingestion and transformation for point count data.

    Args:
        mode (str): Run mode; use -p for a production run and -t for a test
            (read-only) run.
        storage: Storage adapter to write to.
    """
    logger.info('[INIT] factory_point_count_runner()')
    storage = storage or get_storage()
    runner = PointCountRunner(mode=mode, storage=storage)
    logger.info('[PRIMED] factory_point_count_runner()')
    return runner


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_mode = sys.argv[1]
    else:
        run_mode = '-t'
    factory_runner = factory_point_count_runner(mode=run_mode)
    factory_runner.run()
