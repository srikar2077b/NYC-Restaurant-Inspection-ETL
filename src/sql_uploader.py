from sqlalchemy import create_engine, text
from src.logger import setup_logger
from src.config_loader import load_config  # Load config from YAML

logger = setup_logger()

def upload_to_sqlserver(df):
    try:
        logger.info("[SQL UPLOAD] Starting upload process to SQL Server...")

        config = load_config()
        sql_config = config['sql_server']

        server = sql_config['server']
        database = sql_config['database']
        driver = sql_config['driver']
        table_name = sql_config['table_name']
        procedure_name = sql_config.get('procedure_name', 'CleanRestaurantInspectionData')  # Default if not set

        connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver.replace(' ', '+')}"
        engine = create_engine(connection_string, fast_executemany=True)

        # Truncate the table
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name}"))
            logger.info(f"[SQL UPLOAD] Existing data in table '{table_name}' truncated successfully.")

        # Upload the new data
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"[SQL UPLOAD] Data uploaded successfully to table '{table_name}' in database '{database}'.")

        # Run stored procedure to clean data
        with engine.connect() as conn:
            conn.execute(text(f"EXEC {procedure_name}"))
            logger.info(f"[SQL UPLOAD] Stored procedure '{procedure_name}' executed successfully.")

    except Exception as e:
        logger.error(f"[SQL UPLOAD] Upload failed: {e}")
        raise
