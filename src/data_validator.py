import pandas as pd
from src.logger import setup_logger
import os
from datetime import datetime

logger = setup_logger()

def validate_data(df):
    logger.info("[VALIDATION] Starting data validation checks")

    try:
        # 1. Check for missing values in critical columns
        critical_cols = ['RES_ID', 'RES_NAME', 'BORO', 'ZIPCODE', 'VIOLATION_CODE', 'INSPECTION_DATE']
        for col in critical_cols:
            missing = df[col].isna().sum()
            logger.info(f"[VALIDATION] Missing values in '{col}': {missing}")

        # 2. Check data types
        expected_types = {
            'ZIPCODE': 'int64',
            'INSPECTION_DATE': 'datetime64[ns]',
            'RES_ID': 'int64'
        }
        for col, expected_type in expected_types.items():
            if col in df.columns:
                actual_type = df[col].dtype
                if str(actual_type) != expected_type:
                    logger.warning(f"[VALIDATION] Column {col} is {actual_type}, expected {expected_type}")
                else:
                    logger.info(f"[VALIDATION] Column {col} type is valid: {actual_type}")

        # 3. Check for valid 'BORO'
        valid_boros = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']
        invalid_boros = df[~df['BORO'].isin(valid_boros)]
        logger.info(f"[VALIDATION] Invalid BORO values: {len(invalid_boros)}")

        # 4. Check for valid GRADE values (if exists)
        if 'GRADE' in df.columns:
            valid_grades = ['A', 'B', 'C', 'P', 'Z', 'Not Yet Graded']
            invalid_grades = df[~df['GRADE'].isin(valid_grades)]
            logger.info(f"[VALIDATION] Invalid GRADE values: {len(invalid_grades)}")

        # 5. Check ZIPCODE range
        if 'ZIPCODE' in df.columns:
            out_of_range = df[~df['ZIPCODE'].between(10001, 11697)]
            logger.info(f"[VALIDATION] ZIPCODEs out of NYC range: {len(out_of_range)}")

        logger.info("[VALIDATION] Data validation checks completed successfully.")

    except Exception as e:
        logger.error(f"[VALIDATION] Validation failed: {e}")
        raise