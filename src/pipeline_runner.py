from src.data_loader import load_csv
from src.data_cleaner import clean_data
from src.data_validator import validate_data
from src.data_transformer import transform_data
from src.config_loader import load_config
from src.logger import setup_logger
from src.save_data import save_to_csv
from src.sql_uploader import upload_to_sqlserver
import pandas as pd


logger = setup_logger()

def run_pipeline():
    try:
        config = load_config()
        df = load_csv(config['csv_path'])
        cleaned_df = clean_data(df)
        
        validate_data(cleaned_df)
        
        save_to_csv(cleaned_df, config['output_path'])
        
        transformed_df = transform_data(cleaned_df)
        
        save_to_csv(transformed_df, config['transformed_output_path'])
        
        df = pd.read_csv("output/DOHMH_New_York_City_Restaurant_Inspection_T.csv")
        upload_to_sqlserver(df)

        print(transformed_df.head())
        logger.info("Pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise
