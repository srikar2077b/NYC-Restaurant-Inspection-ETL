import pandas as pd
from src.logger import setup_logger

logger = setup_logger()

def save_to_csv(df, output_path):
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Cleaned data saved successfully to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save data to CSV: {e}")
        raise
