from configparser import ConfigParser

class Configuration:
    """
    The Configuration class is used to parse the *.ini formatted file containing the 
    PostgreSQL database configuration data.  As such the format of the file should 
    be as follows:
        [<section name>]
        host=<name of server>
        port=<port # of service>
        user=<postgres user account>
        password=<postgres user account password>
        database=<name of the application database>
    """
    def parse(self, filename, section):        
        # Set a configuration variable
        configuration = {}
        
        # Create an instance of the ConfigParser and read in the (.ini formatted) filename
        parser = ConfigParser()
        parser.read(filename)
        
        # Check if section exists
        if parser.has_section(section):
            parameters = parser.items(section)
            
            # Loop through the parameters to build the configuration
            for parameter in parameters:
                configuration[parameter[0]] = parameter[1]

            host = configuration['host']
            port = configuration['port']
            user = configuration['user']
            password = configuration['password']
            database = configuration['database']
            
            return f"{section}://{user}:{password}@{host}:{port}/{database}"
        else:
            raise Exception(f"Section '{section}' not found in '{filename}'.")