import os
import datetime
import subprocess
import configparser
import logging
from pathlib import Path

logging.Config(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backup.log"),
        logging.StreamHandler()
    ]
)

class DatabaseBackup:
    DEFAULT_CONFIG = {
        'Database': {
            'host': 'localhost',
            'port': '3306',
            'user': 'root',
            'password': '',
            'database': 'bank_system'
        },
        'Backup': {
            'directory': 'backups',
            'retention_days': '7'
        }
    }
    
    def __init__(self, config_file="db_config.ini"):
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_file):
            self._create_default_config(config_file)
        
        self.config.read(config_file)
        
        self.db_settings = {key: self.config.get('Database', key, fallback=value) 
                           for key, value in self.DEFAULT_CONFIG['Database'].items()}
        
        self.backup_dir = self.config.get('Backup', 'directory', 
                                         fallback=self.DEFAULT_CONFIG['Backup']['directory'])
        self.backup_retention = int(self.config.get('Backup', 'retention_days', 
                                                  fallback=self.DEFAULT_CONFIG['Backup']['retention_days']))
        
        Path(self.backup_dir).mkdir(exist_ok=True)
    
    def _create_default_config(self, config_file):
        self.config.read_dict(self.DEFAULT_CONFIG)
        
        with open(config_file, 'w') as f:
            self.config.write(f)
        
        logging.info(f"Created default configuration file: {config_file}")
    
    def create_backup(self):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{self.backup_dir}/{self.db_settings['database']}_{timestamp}.sql"
            
            cmd = [
                'mysqldump',
                f"--host={self.db_settings['host']}",
                f"--port={self.db_settings['port']}",
                f"--user={self.db_settings['user']}",
                f"--databases", self.db_settings['database'],
                "--routines",
                "--triggers",
                "--events",
                "--single-transaction"
            ]
            
            if self.db_settings['password']:
                cmd.append(f"--password={self.db_settings['password']}")
            
            with open(backup_filename, 'w') as output_file:
                logging.info(f"Starting database backup to {backup_filename}")
                subprocess.run(cmd, stdout=output_file, check=True)
            
            logging.info(f"Database backup completed successfully: {backup_filename}")
            return backup_filename
        
        except Exception as e:
            logging.error(f"Backup failed: {str(e)}")
            return None
    
    def cleanup_old_backups(self):
        try:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.backup_retention)
            count = 0
            
            for backup_file in Path(self.backup_dir).glob(f"{self.db_settings['database']}_*.sql"):
                try:
                    file_date_str = backup_file.stem.split('_', 1)[1]
                    file_date = datetime.datetime.strptime(file_date_str, "%Y%m%d_%H%M%S")
                    
                    if file_date < cutoff_date:
                        backup_file.unlink()
                        count += 1
                        logging.info(f"Deleted old backup: {backup_file}")
                except (ValueError, IndexError):
                    logging.warning(f"Could not parse date from filename: {backup_file}")
            
            logging.info(f"Cleanup complete. Deleted {count} old backup(s).")
        
        except Exception as e:
            logging.error(f"Cleanup failed: {str(e)}")


if __name__ == "__main__":
    backup = DatabaseBackup()
    backup_file = backup.create_backup()
    
    if backup_file:
        backup.cleanup_old_backups()
        print(f"Backup completed successfully: {backup_file}")
    else:
        print("Backup failed. Check the log file for details.")