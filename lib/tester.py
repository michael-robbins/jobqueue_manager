#
#
#
class TestManager():
    """
    My dodgy method of testing before I integrate Unit Tests :)
    """

    config_file = '/home/michael/Development/Projects/jobqueue_manager/default.conf'
    db_file     = '/home/michael/Development/Projects/jobqueue_manager/manager.db'
    db_schema   = '/home/michael/Development/Projects/jobqueue_manager/schema.sqlite3.sql'
    log_file    = '/tmp/{0}.log'

    #
    #
    #
    def get_test_logger(self, log_name):
        import os
        from logger import Logger

        log_file = '/tmp/{0}.log'.format(log_name)

        if os.path.exists(log_file):
            os.remove(log_file)

        return Logger(log_name, log_file).get_logger()


    #
    #
    #
    def reset_db_schema(self, db_schema, logger=None):
        import os
        os.system('cat ' + db_schema + ' | sqlite3 ' + self.db_file)

        if logger:
            logger.debug('Reset DB Schema to ' + self.db_schema)


    #
    #
    #
    def dump_log(self, log_file):
        with open(log_file, 'r') as f:
            print(f.read())


    #
    #
    #
    def test_Logger(self):
        # Setup
        test_name = 'manager_Logger'
        logger = self.get_test_logger(test_name)

        # Testing
        logger.error('ERROR')
        logger.warning('WARNING')
        logger.info('INFO')
        logger.debug('DEBUG')

        try:
            logger.zomg('ZOMG')
            raise Exception("logger.zomg should not exist")
        except Exception:
            pass

        # Print Results
        self.dump_log(self.log_file.format(test_name))


    #
    #
    #
    def test_DBManager(self):
        # Setup
        test_name = 'manager_DBManager'
        logger = self.get_test_logger(test_name)

        from config import ConfigManager
        config = ConfigManager(self.config_file).get_config()

        from db import SQLite3_DBManager
        db_manager = SQLite3_DBManager(config['MANAGER'], logger)

        self.reset_db_schema(self.db_schema, logger)

        # Testing
        logger.debug('Opened connection and reset schema')
        cursor = db_manager.get_cursor()

        if cursor:
            SQL = db_manager.get_sql_cmds(['all_jobs'])
            cursor.execute(SQL['all_jobs'])
            for i,job in enumerate(cursor.fetchall()):
                logger.info("Job {0}: {1}".format(i,job))
        else:
            logger.error("Unable to open cursor")

        # Print Results
        self.dump_log(self.log_file.format(test_name))


    #
    #
    #
    def test_JobManager(self):
        # Setup
        test_name = 'manager_JobManager'
        logger = self.get_test_logger(test_name)

        from config import ConfigManager
        config = ConfigManager(self.config_file).get_config()

        from db import SQLite3_DBManager
        db_manager = SQLite3_DBManager(config['MANAGER'], logger)

        self.reset_db_schema(self.db_schema, logger)

        from jobs import JobManager
        job_manager = JobManager(db_manager, logger)

        # Testing
        if job_manager.is_alive():
            job = job_manager.get_next_job()

            if job:
                logger.info('Before:'    + str(job))
                job.report_started()
                logger.info('Started: '  + str(job))
                job.report_complete()
                logger.info('Complete: ' + str(job))

            job = job_manager.get_next_job()

            if job:
                logger.info('Next: ' + str(job))
            else:
                logger.info('No more jobs!')

        # Print Results
        self.dump_log(self.log_file.format(test_name))

    #
    #
    #
    def test_JobQueueManager(self):
        # Setup
        test_name = 'manager_JobQueueManager'
        logger = self.get_test_logger(test_name)

        from manager import JobQueueManager
        jqm = JobQueueManager(self.config_file, False, False)

        # Testing
        jqm.start()

        # Print Results
        self.dump_log(self.log_file.format(test_name))


#
#
#
if __name__ == '__main__':
    """
    Run through all test_*'s we have created
    """

    tester = TestManager()

    # Run through the test cases we have so far
    # (no way of dynamically figuring out what we have coded so far)
    # (maybe something like getattr on self.test_* ?
    tester.test_Logger()
    tester.test_DBManager()
    tester.test_JobManager()
    tester.test_JobQueueManager()
    #tester.test_SyncManager() # Not written yet
