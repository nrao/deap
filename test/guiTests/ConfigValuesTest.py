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

import sys

if __name__ == "__main__":
    sys.path[1:1] = ["..", "../../"]

from gui.framework import ConfigValues
import unittest

class ConfigValuesTest (unittest.TestCase):

    def setUp (self):
        
        self.NON_EXISTENT_FILENAME = "non_existent_file.conf"
        self.EXISTING_FILENAME = "existing_file.conf"
        
        self.NON_EXISTENT_SECTIONNAME = "NonExistentSectionName"
        self.EXISTING_SECTIONNAME = "ExistingSectionName"
        
        self.NON_EXISTENT_KEYNAME = "NonExistentKeyName"
        self.EXISTING_KEYNAME_FORMAT1 = "ExistingKeyName1"
        self.EXISTING_KEYNAME_FORMAT2 = "ExistingKeyName2"

        self.EXISTING_KEYNAME_BOOL = "SomeBoolValuedKey"
        self.EXISTING_KEYNAME_STRING = "SomeStringValuedKey"
        self.EXISTING_KEYNAME_INT = "SomeIntValuedKey"
        self.EXISTING_KEYNAME_INTNEG = "SomeNegativeIntValuedKey"
        self.EXISTING_KEYNAME_FLOAT = "SomeFloatValuedKey"
        
        self.EXISTING_KEY_VALUE1 = "ExistingKeyValue1"
        self.EXISTING_KEY_VALUE2 = "ExistingKeyValue2"
        
        self.EXISTING_KEY_BOOLVALUE = "True"
        self.EXISTING_KEY_STRINGVALUE = "Some string for String Validation"
        self.EXISTING_KEY_INTVALUE = "99"
        self.EXISTING_KEY_INTNEGVALUE = "-99"
        self.EXISTING_KEY_FLOATVALUE = "121.834"
        
        self.DEFAULT_VALUE_BOOL = True
        self.DEFAULT_VALUE_STRING = "StringDefaultValue"
        self.DEFAULT_VALUE_INT = 99
        self.DEFAULT_VALUE_FLOAT = 121.834
        
        self.DEFAULT_VALUE = "testDefaultValue"
        self.NO_DEFAULT_VALUE = "None"
        
        # Build the "existing" config values files
        testConfigValueFile = open (self.EXISTING_FILENAME, "w")
        
        testConfigValueFile.write("[" + self.EXISTING_SECTIONNAME + "]\n")

        testConfigValueFile.write(self.EXISTING_KEYNAME_FORMAT1 
                                  + " = " + self.EXISTING_KEY_VALUE1 + "\n")
        testConfigValueFile.write(self.EXISTING_KEYNAME_FORMAT2 
                                  + " : " + self.EXISTING_KEY_VALUE2 + "\n")
        testConfigValueFile.write(self.EXISTING_KEYNAME_BOOL 
                                  + " = " + self.EXISTING_KEY_BOOLVALUE + "\n")
        testConfigValueFile.write(self.EXISTING_KEYNAME_STRING 
                                  + " = " + self.EXISTING_KEY_STRINGVALUE + "\n")
        testConfigValueFile.write(self.EXISTING_KEYNAME_INT 
                                  + " = " + self.EXISTING_KEY_INTVALUE + "\n")
        testConfigValueFile.write(self.EXISTING_KEYNAME_INTNEG 
                                  + " = " + self.EXISTING_KEY_INTNEGVALUE + "\n")
        testConfigValueFile.write(self.EXISTING_KEYNAME_FLOAT 
                                  + " = " + self.EXISTING_KEY_FLOATVALUE + "\n")

        testConfigValueFile.close()
        
        
    def testNonExistentConfigValueFile (self):

        # Setup with file known that is known to be non-existent.
        tstCV = ConfigValues(self.NON_EXISTENT_FILENAME)
        tstCV.InitConfig()
        
        # With passed in default value
        resultDef = tstCV.GetOption (self.NON_EXISTENT_SECTIONNAME, 
                                     self.NON_EXISTENT_KEYNAME, 
                                     self.DEFAULT_VALUE)
        assert resultDef == self.DEFAULT_VALUE
        

    def testNonExistentConfigValueFileNoDefault (self):

        # Setup with file known that is known to be non-existent.
        tstCV = ConfigValues(self.NON_EXISTENT_FILENAME)
        tstCV.InitConfig()
        
        # With no passed in default value
        resultNoDef = tstCV.GetOption (self.NON_EXISTENT_SECTIONNAME, 
                                       self.NON_EXISTENT_KEYNAME)
        assert resultNoDef == self.NO_DEFAULT_VALUE

    
    def testHasSection (self):

        # Setup with file known to exist.
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # For non-existent section
        resultDef = tstCV.HasSection (self.NON_EXISTENT_SECTIONNAME)
        assert resultDef == False
        
        # For existing section
        resultDef = tstCV.HasSection (self.EXISTING_SECTIONNAME)
        assert resultDef == True


    def testNonExistentSection (self):

        # Setup with file known to exist.
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With passed in default value
        resultDef = tstCV.GetOption (self.NON_EXISTENT_SECTIONNAME, 
                                     self.NON_EXISTENT_KEYNAME, 
                                     self.DEFAULT_VALUE)
        assert resultDef == self.DEFAULT_VALUE
        

    def testNonExistentSectionNoDefault (self):

        # Setup with file known to exist.
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With no passed in default value
        resultNoDef = tstCV.GetOption (self.NON_EXISTENT_SECTIONNAME, 
                                       self.NON_EXISTENT_KEYNAME)
        assert resultNoDef == self.NO_DEFAULT_VALUE

    
    def testNonExistentKey (self):

        # Setup with file known to exist, with section known to exist.
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With passed in default value
        resultDef = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.NON_EXISTENT_KEYNAME, 
                                     self.DEFAULT_VALUE)
        assert resultDef == self.DEFAULT_VALUE
        

    def testNonExistentKeyNoDefault (self):

        # Setup with file known to exist, with section known to exist.
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With no passed in default value
        resultNoDef = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                       self.NON_EXISTENT_KEYNAME)
        assert resultNoDef == self.NO_DEFAULT_VALUE
        
    
    def testExistingKeyFormat1 (self):
        
        # Setup with file known to exist, with section and key known to exist.
        # Key-value pair format 1:  Key = Value
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With passed in default value
        resultDef = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_FORMAT1, 
                                     self.DEFAULT_VALUE)
        assert resultDef == self.EXISTING_KEY_VALUE1
        

    def testExistingKeyFormat1NoDefault (self):
        
        # Setup with file known to exist, with section and key known to exist.
        # Key-value pair format 1:  Key = Value
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With no passed in default value
        resultNoDef = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                       self.EXISTING_KEYNAME_FORMAT1)
        assert resultNoDef == self.EXISTING_KEY_VALUE1
        

    def testExistingKeyFormat2 (self):
        
        # Setup with file known to exist, with section and key known to exist.
        # Key-value pair format 2:  Key:Value
        tstCV = ConfigValues(self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With passed in default value
        resultDef = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_FORMAT2, 
                                     self.DEFAULT_VALUE)
        assert resultDef == self.EXISTING_KEY_VALUE2

        
    def testExistingKeyFormat2NoDefault (self):
        
        # Setup with file known to exist, with section and key known to exist.
        # Key-value pair format 2:  Key:Value
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # With no passed in default value
        resultNoDef = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                       self.EXISTING_KEYNAME_FORMAT2)
        assert resultNoDef == self.EXISTING_KEY_VALUE2


    def testIsBooleanOnBool (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultBool = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                      self.EXISTING_KEYNAME_BOOL)
        assert ConfigValues.isBoolean (resultBool) == True
        
    
    def testIsBooleanOnNonBool (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultBool = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                      self.EXISTING_KEYNAME_STRING)
        assert ConfigValues.isBoolean (resultBool) == False
        
    
    def testIsConstrainedStringExactPass (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultStr = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_STRING)
        
        assert ConfigValues.isConstrainedString (resultStr, 
                                                 self.EXISTING_KEY_STRINGVALUE) == True
        
    
    def testIsConstrainedStringExactFail (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultStr = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_STRING)
        
        assert ConfigValues.isConstrainedString (resultStr, 
                                                 list([self.EXISTING_KEY_STRINGVALUE 
                                                       + "junk"])) == False
        
    
    def testIsConstrainedStringContainsPass (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()

        # List of strings which CONTAINS the string to be tested.
        testStringValues = list(["sixOfOne", 
                                 self.EXISTING_KEY_STRINGVALUE, 
                                 "halfDozenOfTheOther"])

        resultStr = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_STRING)
        
        assert ConfigValues.isConstrainedString (resultStr, testStringValues) == True
        
    
    def testIsConstrainedStringContainsFail (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # List of strings which does NOT contain the string to be tested.
        testStringValues = list(["sixOfOne", "halfDozenOfTheOther"])

        resultStr = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_STRING)
        
        assert ConfigValues.isConstrainedString (resultStr, testStringValues) == False
        
    
    def testIsConstrainedNumberOnInt (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultInt = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                     self.EXISTING_KEYNAME_INT)
        
        assert ConfigValues.isConstrainedNumber (resultInt, int) == True
        
    
    def testIsConstrainedNumberOnFloat (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultFloat = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                       self.EXISTING_KEYNAME_FLOAT)
        
        assert ConfigValues.isConstrainedNumber (resultFloat, float) == True
        
    
    def testIsConstrainedNumberOnNegativeNumber (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultIntNeg = tstCV.GetOption (self.EXISTING_SECTIONNAME, 
                                        self.EXISTING_KEYNAME_INTNEG)
        
        assert ConfigValues.isConstrainedNumber (resultIntNeg, int) == False
        
    
    def testGetOptionWithValidationBoolOnBool (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultBool = tstCV.GetOptionWithValidation (self.EXISTING_SECTIONNAME, 
                                                    self.EXISTING_KEYNAME_BOOL,
                                                    True)
        
        assert resultBool == True
        
    
    def testGetOptionWithValidationBoolOnNonBool (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultBool = tstCV.GetOptionWithValidation (self.EXISTING_SECTIONNAME, 
                                                    self.EXISTING_KEYNAME_STRING,
                                                    False)
        
        assert resultBool == False    # resultBool should contain the DEFAULT value, in this case, False.
        
    
    def testGetOptionWithValidationStringOnExactPass (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultStr = tstCV.GetOptionWithValidation (self.EXISTING_SECTIONNAME, 
                                                   self.EXISTING_KEYNAME_STRING,
                                                   "StringDefaultValue",
                                                   list([self.EXISTING_KEY_STRINGVALUE]))
        
        assert resultStr == self.EXISTING_KEY_STRINGVALUE
        
    
    def testGetOptionWithValidationStringOnExactFail (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        resultStr = tstCV.GetOptionWithValidation (self.EXISTING_SECTIONNAME, 
                                                   self.EXISTING_KEYNAME_STRING,
                                                   "StringDefaultValue",
                                                   list([self.EXISTING_KEY_STRINGVALUE + "junk"]))
        
        assert resultStr == "StringDefaultValue"
        
    
    def testGetOptionWithValidationStringOnContainsPass (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()

        # List of strings which CONTAINS the string to be tested.
        testStringValues = list(["sixOfOne", 
                                 self.EXISTING_KEY_STRINGVALUE, 
                                 "halfDozenOfTheOther"])

        resultStr = tstCV.GetOptionWithValidation (self.EXISTING_SECTIONNAME, 
                                                   self.EXISTING_KEYNAME_STRING,
                                                   self.DEFAULT_VALUE_STRING,
                                                   testStringValues)
        
        assert resultStr == self.EXISTING_KEY_STRINGVALUE
        
    
    def testGetOptionWithValidationStringOnContainsFail (self):
        
        # Setup with file known to exist, with section and key known to exist.
        tstCV = ConfigValues (self.EXISTING_FILENAME)
        tstCV.InitConfig()
        
        # List of strings which does NOT contain the string to be tested.
        testStringValues = list(["sixOfOne",
                                 "halfDozenOfTheOther"])

        resultStr = tstCV.GetOptionWithValidation (self.EXISTING_SECTIONNAME, 
                                                   self.EXISTING_KEYNAME_STRING,
                                                   "StringDefaultValue",
                                                   testStringValues)
        
        assert resultStr == "StringDefaultValue"
        
    
def suite():
    """
    Returns a suite containing all the test cases in this module.
    It can be a good idea to put an identically named factory function
    like this in every test module. Such a naming convention allows
    automation of test discovery.
    """
    suite1 = unittest.makeSuite(ConfigValueTestCase)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.main()
