import pandas as pd
from src.logger import setup_logger

logger = setup_logger()

def transform_data(df):
    logger.info("[TRANSFORMATION] Starting data transformation pipeline...")
    logger.info(f"[TRANSFORMATION] Input DataFrame shape before transformation: {df.shape}")

    try:
        # 1. Standardize GRADE values
        if 'GRADE' in df.columns:
            df['GRADE'] = df['GRADE'].astype(str).str.upper().replace(
                ['NAN', 'NA', 'NONE', '', 'NULL'], 'NOT GRADED'
            )
            df['GRADE'] = df['GRADE'].fillna('NOT GRADED')
            logger.info("[TRANSFORMATION] Standardized GRADE values.")
    except Exception as e:
        logger.error(f"[TRANSFORMATION] Error standardizing GRADE values: {e}")
        raise

    try:
        # 2. Extract temporal features from INSPECTION_DATE
        if 'INSPECTION_DATE' in df.columns:
            df['INSPECTION_YEAR'] = df['INSPECTION_DATE'].dt.year
            df['INSPECTION_MONTH'] = df['INSPECTION_DATE'].dt.month
            df['INSPECTION_DAY'] = df['INSPECTION_DATE'].dt.day
            df['INSPECTION_WEEK_NUMBER'] = df['INSPECTION_DATE'].dt.isocalendar().week
            logger.info("[TRANSFORMATION] Extracted temporal features from INSPECTION_DATE.")
    except Exception as e:
        logger.error(f"[TRANSFORMATION] Error extracting temporal features: {e}")
        raise

    try:
        # 3. Categorize SCORE into risk levels
        if 'SCORE' in df.columns:
            def categorize(score):
                try:
                    score = float(score)
                    if score <= 13:
                        return 'Low Risk'
                    elif score <= 27:
                        return 'Medium Risk'
                    else:
                        return 'High Risk'
                except:
                    return 'Unknown'

            df['RISK_CATEGORY'] = df['SCORE'].apply(categorize)
            logger.info("[TRANSFORMATION] Categorized SCORE into RISK_CATEGORY.")
    except Exception as e:
        logger.error(f"[TRANSFORMATION] Error categorizing SCORE: {e}")
        raise

    try:
        # 4. Combine address fields
        for col in ['BUILDING', 'STREET', 'ZIPCODE']:
            if col not in df.columns:
                df[col] = ""
        df['FULL_ADDRESS'] = df['BUILDING'].astype(str).str.strip() + ", " + \
                             df['STREET'].astype(str).str.strip() + ", " + \
                             df['ZIPCODE'].astype(str).str.zfill(5)
        logger.info("[TRANSFORMATION] Combined BUILDING, STREET, ZIPCODE into FULL_ADDRESS.")
    except Exception as e:
        logger.error(f"[TRANSFORMATION] Error creating FULL_ADDRESS: {e}")
        raise

    logger.info(f"[TRANSFORMATION] Data transformation completed. Output shape: {df.shape}")
    return df
