import configparser
import os

# Config here
class config():

    con = None

    config_dir = ".config"

    def __init__(self):

        self.con = configparser.ConfigParser()
        if (os.path.exists(self.config_dir)):

            self.con.read(self.config_dir)

        else:

            self.con['SERVER'] = {'email': '', 'smtp': '', 'port': '', 'username':'', 'password':''}
            with open(self.config_dir, 'w') as configfile:
                self.con.write(configfile)


    def get_email(self):
        try:
            return self.con["SERVER"]["email"]
        except KeyError as e:
            return None
        except:
            raise

    def get_smtp(self):
        try:
            return self.con["SERVER"]["smtp"]
        except KeyError as e:
            return None
        except:
            raise

    def get_port(self):
        try:
            return int(self.con["SERVER"]["port"])
        except KeyError as e:
            return None
        except:
            raise

    def get_username(self):
        try:
            return self.con["SERVER"]["username"]
        except KeyError as e:
            return None
        except:
            raise

    def get_password(self):
        try:
            return self.con["SERVER"]["password"]
        except KeyError as e:
            return None
        except:
            raise