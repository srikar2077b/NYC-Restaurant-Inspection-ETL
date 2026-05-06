import pandas as pd
from src.logger import setup_logger

logger = setup_logger()

def load_csv(path):
    try:
        df = pd.read_csv(path)
        logger.info(f"CSV loaded successfully from {path}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except Exception as e:
        logger.error(f"Failed to load CSV: {e}")
        raise
