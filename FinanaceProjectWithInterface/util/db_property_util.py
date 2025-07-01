import configparser

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)

        db_config = config['DEFAULT']
        return {
            'host': db_config['host'],
            'port': int(db_config['port']),
            'database': db_config['database'],
            'user': db_config['user'],
            'password': db_config['password']
        }
