import pandas as pd
from src.logger import setup_logger
import re

logger = setup_logger()

def clean_data(df):
    logger.info("[CLEANING] Starting data cleaning pipeline...")
    logger.info(f"[CLEANING] Input DataFrame shape before cleaning: {df.shape}")

    try:
        # Step 1: Standardize column names
        df.columns = (
            df.columns.str.strip()
                      .str.lower()
                      .str.replace(" ", "_")
                      .str.replace(r"[^\w\s]", "", regex=True)
        )
        logger.info("[CLEANING] Standardized column names.")
    except Exception as e:
        logger.error(f"[CLEANING] Error standardizing column names: {e}")
        raise

    try:
        # Step 2: Drop fully empty rows
        initial_rows = len(df)
        df = df.dropna(how='all')
        logger.info(f"[CLEANING] Dropped {initial_rows - len(df)} fully empty rows. Shape: {df.shape}")
    except Exception as e:
        logger.error(f"[CLEANING] Error dropping fully empty rows: {e}")
        raise

    try:
        # Step 3: Convert date columns
        date_columns = ["inspection_date", "grade_date", "record_date"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        logger.info("[CLEANING] Converted date columns to datetime format.")
    except Exception as e:
        logger.error(f"[CLEANING] Error converting date columns: {e}")
        raise

    try:
        # Step 4: Drop duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        logger.info(f"Dropped {initial_rows - len(df)} duplicate rows. Shape: {df.shape}")
    except Exception as e:
        logger.error(f" [CLEANING] Error dropping duplicate rows: {e}")
        raise

    try:
        # Step 5: Trim whitespace in all string columns
        str_cols = df.select_dtypes(include='object').columns
        df = df.copy() 
        df[str_cols] = df[str_cols].astype(str).apply(lambda col: col.str.strip())
        logger.info("[CLEANING] Trimmed whitespace from string columns.")
    except Exception as e:
        logger.error(f"[CLEANING] Error trimming string columns: {e}")
        raise

    try:
        # Step 6: Capitalize all column names
        df.columns = [col.upper() for col in df.columns]
        logger.info("[CLEANING] Capitalized all column names.")
    except Exception as e:
        logger.error(f"[CLEANING] Error capitalizing column names: {e}")
        raise

    try:
        # Step 7: Rename specific columns
        df = df.rename(columns={
            'CAMIS': 'RES_ID',
            'DBA': 'RES_NAME',
            'PHONE': 'PHONE_NUMBER'
        })
        logger.info("[CLEANING] Renamed columns: CAMIS → RES_ID, DBA → RES_NAME, PHONE → PHONE_NUMBER")
    except Exception as e:
        logger.error(f"[CLEANING] Error renaming specific columns: {e}")
        raise

    try:
        # Step 8: Format phone numbers
        if 'PHONE_NUMBER' in df.columns:
            def format_number(num):
                if pd.isnull(num):
                    return None
                digits = re.sub(r'\D', '', str(num))
                if len(digits) == 10:
                    return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
                else:
                    return None

            df['PHONE_NUMBER'] = df['PHONE_NUMBER'].apply(format_number)
            logger.info("[CLEANING] Formatted phone numbers to US standard.")
    except Exception as e:
        logger.error(f"[CLEANING] Error formatting phone numbers: {e}")
        raise
    
    try:
        # Step 9: Drop invalid VIOLATION_CODE rows (null, dot, empty string, "nan", "none")
        if 'VIOLATION_CODE' in df.columns:
            initial_rows = len(df)
            df['VIOLATION_CODE'] = df['VIOLATION_CODE'].astype(str).str.strip().str.upper()
            invalid_values = ['', '.', 'NAN', 'NONE']
            df = df[~df['VIOLATION_CODE'].isin(invalid_values)]
            dropped_rows = initial_rows - len(df)
            logger.info(f"[CLEANING] Dropped {dropped_rows} rows with invalid VIOLATION_CODE values.")
    except Exception as e:
        logger.error(f"[CLEANING] Error cleaning VIOLATION_CODE column: {e}")
        raise
    
    try:
        # Step 10: Drop unwanted columns
        cols_to_drop = ['LATITUDE', 'LONGITUDE', 'COMMUNITY_BOARD', 'COUNCIL_DISTRICT',
                        'CENSUS_TRACT', 'BIN', 'BBL', 'NTA', 'LOCATION_POINT1']
        existing_cols = [col for col in cols_to_drop if col in df.columns]
        df = df.drop(columns=existing_cols)
        logger.info(f"[CLEANING] Dropped columns: {existing_cols}")
    except Exception as e:
        logger.error(f"[CLEANING] Error dropping unwanted columns: {e}")
        raise

    try:
        # Step 11: Fix ZIPCODE column
        if 'ZIPCODE' in df.columns:
            df['ZIPCODE'] = df['ZIPCODE'].astype(str).str[:5].str.zfill(5)
            df['ZIPCODE'] = pd.to_numeric(df['ZIPCODE'], errors='coerce').fillna(0).astype(int)
            logger.info("[CLEANING] Standardized ZIPCODE column to integer (5-digit).")
    except Exception as e:
        logger.error(f"[CLEANING] Error fixing ZIPCODE column: {e}")
        raise

    logger.info("[CLEANING] Data cleaning pipeline completed successfully.")
    return df