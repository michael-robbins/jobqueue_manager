#
#
#
class DBManager():
    """
    Generic DB functions in here, will be specialised per DB type (PostgreSQL, MySQL, SQLLite)
    """

    def __init__(self, config, logger):
        """
        Set up the connection string details
        """

        self.logger = logger

        for opt in self._required_db_opts:
            if opt in config:
                setattr(self, opt, config[opt])
            else:
                self.logger.error('You are missing the following config option: {0}'.format(opt))

    def get_sql_cmds(list_of_cmds):
        """
        return dict() of generic SQL commands
        """
        SQL                 = {}
        SQL['all_jobs']     = 'select * from job_queue'
        SQL['next_job']     = 'select * from job_queue where date_started is null ' + \
                                 'and date_completed is null order by date_queued asc limit 1'
        SQL['get_job']      = 'select * from job_queue where job_id = ?'
        SQL['start_job']    = 'update job_queue set date_started = now() where job_id = ?'
        SQL['finish_job']   = 'update job_queue set date_completed = now() where job_id = ?'

        return { i: SQL[i] for i in SQL if i in list_of_cmds }


#
#
#
class Postgres_DBManager(DBManager):
    """
    Postgres overload
    """

    import psycopg2

    def __init__(self, config, logger):
        """
        Set any psql specific stuff and bail to parent class
        """

        self._required_db_opts = ['db_type', 'db_host', 'db_port', 'db_name', 'db_user']
        DBManager.__init__(self, config, logger)

    def get_cursor(self):
        """
        Connect to DB and return cursor
        """

        try:
            print (self.connection_string)
            conn = psycopg2.connect(self.connection_string)
            return conn.cursor()
        except Exception as e:
            self.logger.error('Failed to connect to the DB: {0}'.format(e))
            return None
        return None
    
    def get_sql_cmds(self, list_of_cmds):
        """
        return dict() of PostgreSQL specific commands
        """
        SQL = DBManager.get_sql_cmds(list_of_cmds)

        # Provide any PostgreSQL specific command overrides here
        # SQL['foo'] = 'SELECT * FROM bar'

        return { i: SQL[i] for i in SQL if i in list_of_cmds }


#
#
#
class SQLite3_DBManager(DBManager):
    """
    SQLite3 overload
    """

    def __init__(self, config, logger):

        """
        Set any Sqlite3 specific stuff and bail to parent class
        """

        self._required_db_opts = ['db_type', 'db_name', 'db_file']
        DBManager.__init__(self, config, logger)


    def get_cursor(self):
        """
        Connect to DB and return cursor
        """

        import sqlite3
        return sqlite3.connect(self.db_file).cursor()

    def get_sql_cmds(self, list_of_cmds):
        """
        Return dict() of SQLite3 specific commands
        """
        SQL = DBManager.get_sql_cmds(list_of_cmds)

        # Provide any specific overrides below for SQLite3
        # SQL['foo'] = 'SELECT * FROM bar'
        
        return { i: SQL[i] for i in SQL if i in list_of_cmds }


#
#
#
if __name__ == '__main__':

    # Testing
    import os
    from logger import Logger

    log_file = '/tmp/db_test.log'

    if os.path.exists(log_file):
        os.remove(log_file)

    logger = Logger('db_test', log_file).get_logger()

    db_manager = SQLite3_DBManager(
            {
                'db_type': 'sqlite3'
                , 'db_name': 'jobmanager'
                , 'db_file': '/home/michael/Development/code/jobqueue_manager/manager.db'
                }
            , logger)

    logger.debug('Opened connection')
    c = db_manager.get_cursor()

    if c:
        c.execute("SELECT * FROM clients")
        print(c.fetchone()) 
    else:
        print("ERROR: Unable to open cursor")