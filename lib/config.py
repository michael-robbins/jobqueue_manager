class ConfigManager():
    """
    Parses the JobQueue Manager config file returning a Config() object
    """

    DAEMON = 'DAEMON';

    default_config = {
        DAEMON : ['pid_file', 'log_name', 'log_file', 'working_dir', 'umask', 'sleep']
        }

    class Config():
        """
        Holds all the configuration sections
        """
        pass

    class Section():
        """
        Holds the configuration objects for a specific section
        """
        pass

    def bail_with(message):
        """
        Print the bail message and... bail!
        """
        
        print(message)

        from sys import exit
        exit(1)

    def __init__(self, config_file):
        """
        Parse config file and build a Config object
        """

        import configparser
        config_parser = configparser.ConfigParser()
       
        self.config = ConfigManager.Config()

        try:
            with open(config_file, 'r') as f:
                config_parser.read(config_file)
        except IOError as e:
            message = "ERROR: Something is wrong with the config file: {0}".format(config_file)
            bail_with(message)

        # Run through everything (post additional config additions) and check it all exists
        for section in self.default_config:
            if section not in config_parser.sections():
                message = "Config File is missing section: " + section
                bail_with(message)
            else:
                setattr(self.config, section, ConfigManager.Section())
                for option in self.default_config[section]:
                    if option not in config_parser.options(section):
                        message = "ERROR: Missing config {0} option {1}".format(section, option)
                        bail_with(message)
                    else:
                        setattr(
                                getattr(self.config, section)
                                , option
                                , config_parser[section][option])

    def get_config(self):
        """
        Return ConfigParser() object
        """
        if self.config:
            return self.config
        else:
            return None

if __name__ == '__main__':
    from tester import TestManager
    tester = TestManager()
    tester.test_ConfigManager()
