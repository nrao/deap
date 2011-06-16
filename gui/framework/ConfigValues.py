# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details. 
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the
#
# Free Software Foundation, Inc.,
# 675 Mass Ave
# Cambridge, MA 02139, USA.

import ConfigParser

class ConfigValues:
    """
    Adds support for options and config files to a basic python
    application.
    """
    
    def __init__(self, configPath):
        """Initialize with configuration options file path."""
        self.configPath = configPath
            
    
    def InitConfig(self):
        """
        Initiate ConfigParser base class and read configuration
        file at <configPath>.
        """
        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str
        self.config.read(self.configPath)
        
    
    def GetOption(self, section, key = None, default = None):
        """
        Return option value.
        """
        if key is None:
            return self.config.options(section)
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return str(default)
    
    
    def GetOptionWithValidation (self, section, key = None, default = None, validValues = None ):
        """
        Return validated option value.
        """
        value = self.GetOption (section, key, default)
        if type(default) == str and self.isConstrainedString (value, validValues):
            return value
        elif type(default) == bool and self.isBoolean (value):
            return bool(value)
        elif type(default) in (int, float) and self.isConstrainedNumber (value, type(default)):
            return type(default)(value)
        else:
            return default
        
        
    def HasSection (self, section):
        """
        Return True or False if <section> exists or not.
        """
        if (self.config is not None):
            return self.config.has_section(section)
        else:
            return False
        
    
    @classmethod
    def isBoolean (cls, value):
        """
        Validated as Boolean if <value> is the string representation
        of True or False.
        """
        if value in ("True", "False"):
            return True
        else:
            return False
    
    
    @classmethod
    def isConstrainedString (cls, value, validValues):
        """
        Validated if <value> is one of the string values in <validValues>.
        """
        if value in validValues:
            return True
        else:
            return False
    
    
    @classmethod
    def isConstrainedNumber (cls, value, valueType):
        """
        Validated as a Number if <value> has a valueType() of Number,
        and is non-negative or has the requested <section>.
        """
        try:
            number = valueType(value)
        except:
            return False
    
        if number >= 0:
            return True
        else:
            return False
