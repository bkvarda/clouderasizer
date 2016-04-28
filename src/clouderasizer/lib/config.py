#Object to hold configuration
import ConfigParser, os
class Config:
    def __init__(self,config_file):
        Config = ConfigParser.ConfigParser()
        Config.read(config_file)
        self.logging_dir=Config.get('Directories','LoggingDirectory')
        self.temp_dir=Config.get('Directories','TempDirectory')
        self.output_dir=Config.get('Directories','OutputDirectory')
        self.cloudera_manager_name=Config.get('Cloudera','ClouderaManager')
        self.cloudera_cluster_name=Config.get('Cloudera','ClusterName')
        self.cloudera_username=Config.get('Cloudera','UserName')
        self.cloudera_password=Config.get('Cloudera','Password')
        self.checkDirectories()
    def checkDirectories(self):
        if not os.path.isdir(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.isdir(self.logging_dir):
            os.makedirs(self.logging_dir)
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
