import logging
import os

def setup_logger(log_file='logs/pipeline.log'):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
    full_log_path = os.path.join(base_dir, log_file)

    # Truncate the file each time the logger is initialized
    os.makedirs(os.path.dirname(full_log_path), exist_ok=True)
    with open(full_log_path, 'w'):
        pass

    logging.basicConfig(
        filename=full_log_path,
        filemode='a',
        format='%(asctime)s | %(levelname)s | %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)
