# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
#
# Free Software Foundation, Inc.,
# 675 Mass Ave
# Cambridge, MA 02139, USA

"""
GUI framework and application for use with Python unit testing framework.
Execute tests written using the framework provided by the 'unittest' module.

Further information is available in the bundled documentation, and from

  http://pyunit.sourceforge.net/

Copyright (c) 1999, 2000, 2001 Steve Purcell
This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

wxUnit GUI Copyright (c) 2003 Eric Sessoms
"""

import string
import sys
import traceback
import unittest
import wx

ID_START      = 101
ID_HELP       = 102
ID_ABOUT      = 103
ID_CLOSE      = 104

ID_ERROR_LIST = 201

HELP_TEXT="""\
Enter the name of a callable object which, when called, will return a
TestCase or TestSuite. Click 'start', and the test thus produced will be run.

Double click on an error in the listbox to see more information about it,
including the stack trace.

For more information, visit
http://pyunit.sourceforge.net/
or see the bundled documentation
"""

ABOUT_TEXT="""\
PyUnit unit testing framework.

For more information, visit
http://pyunit.sourceforge.net/

Copyright (c) 2000 Steve Purcell
<stephen_purcell@yahoo.com>

wxUnit GUI Copyright (c) 2003 Eric Sessoms
<eric@sonic-weasel.org>
"""


class GUITestResult(unittest.TestResult):
    """A TestResult that makes callbacks to its associated GUI TestRunner.
    Used by BaseGUITestRunner. Need not be created directly.
    """
    def __init__(self, callback):
        unittest.TestResult.__init__(self)
        self.callback = callback

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.callback.notifyTestErrored(test, err)

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.callback.notifyTestFailed(test, err)

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        self.callback.notifyTestFinished(test)

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.callback.notifyTestStarted(test)


class RollbackImporter:
    """This tricky little class is used to make sure that modules under test
    will be reloaded the next time they are imported.
    """
    def __init__(self):
        self.previousModules = sys.modules.copy()
        
    def rollbackImports(self):
        for modname in sys.modules.keys():
            if not self.previousModules.has_key(modname):
                # Force reload when modname next imported
                del(sys.modules[modname])


class BaseGUITestRunner:
    """Subclass this class to create a GUI TestRunner that uses a specific
    windowing toolkit. The class takes care of running tests in the correct
    manner, and making callbacks to the derived class to obtain information
    or signal that events have occurred.
    """
    def __init__(self, *args, **kwargs):
        self.currentResult = None
        self.running = 0
        self.__rollbackImporter = None
        apply(self.initGUI, args, kwargs)

    def getSelectedTestName(self):
        "Override to return the name of the test selected to be run"
        pass

    def errorDialog(self, title, message):
        "Override to display an error arising from GUI usage"
        pass

    def runClicked(self):
        "To be called in response to user choosing to run a test"
        if self.running: return
        testName = self.getSelectedTestName()
        if not testName:
            self.errorDialog("Test name entry", "You must enter a test name")
            return
        if self.__rollbackImporter:
            self.__rollbackImporter.rollbackImports()
        self.__rollbackImporter = RollbackImporter()
        try:
            test = unittest.defaultTestLoader.loadTestsFromName(testName)
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            apply(traceback.print_exception,sys.exc_info())
            self.errorDialog("Unable to run test '%s'" % testName,
                             "Error loading specified test: %s, %s" % \
                             (exc_type, exc_value))
            return
        self.currentResult = GUITestResult(self)
        self.totalTests = test.countTestCases()
        self.running = 1
        self.notifyRunning()
        test.run(self.currentResult)
        self.running = 0
        self.notifyStopped()

    def stopClicked(self):
        "To be called in response to user stopping the running of a test"
        if self.currentResult:
            self.currentResult.stop()

    # Required callbacks

    def notifyRunning(self):
        "Override to set GUI in 'running' mode, enabling 'stop' button etc."
        pass

    def notifyStopped(self):
        "Override to set GUI in 'stopped' mode, enabling 'run' button etc."
        pass

    def notifyTestFailed(self, test, err):
        "Override to indicate that a test has just failed"
        pass

    def notifyTestErrored(self, test, err):
        "Override to indicate that a test has just errored"
        pass

    def notifyTestStarted(self, test):
        "Override to indicate that a test is about to run"
        pass

    def notifyTestFinished(self, test):
        """Override to indicate that a test has finished (it may already have
           failed or errored)"""
        pass


class RunDialog(wx.Dialog, BaseGUITestRunner):

    def __init__(self, parent, testSuite):
        wx.Dialog.__init__(self, parent, -1, "wxUnit (PyUnit for wxPython)")
        BaseGUITestRunner.__init__(self, testSuite)

    def initGUI(self, testSuite):
        self.status = wx.StatusBar(self, -1, 0)

        box = wx.BoxSizer(wx.VERTICAL)
        box.AddSizer(self.InitTestName(), 0, wx.EXPAND)
        box.AddSizer(self.InitInfo(),     1, wx.EXPAND)
        box.Add(self.status, 0, wx.EXPAND)
        self.SetSizer(box)
        self.SetAutoLayout(TRUE)
        self.testName.SetValue(testSuite)
        self.Fit()

    def InitTestName(self):
        self.testName = wx.TextCtrl(self, -1)
        self.startBtn = wx.Button(self, ID_START, "Start")

        static = wx.StaticBox(self, -1, "Test Name")
        inner  = wx.StaticBoxSizer(static, wx.HORIZONTAL)
        inner.Add(wx.StaticText(self, -1, "Enter test name:"), 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER)
        inner.Add(self.testName, 1)

        outer  = wx.BoxSizer(wx.HORIZONTAL)
        outer.AddSizer(inner, 1)
        outer.Add(self.startBtn, 0, wx.ALIGN_CENTER)

        EVT_BUTTON(self, ID_START, self.OnStart)

        return outer

    def OnStart(self, event):
        if self.startBtn.GetLabel() == "Start": self.runClicked()
        else:                                   self.stopClicked()

    def InitInfo(self):
        inner = wx.BoxSizer(wx.VERTICAL)
        inner.AddSizer(self.InitProgress(), 0, wx.EXPAND)
        inner.AddSizer(self.InitDetail(),   1, wx.EXPAND)

        outer = wx.BoxSizer(wx.HORIZONTAL)
        outer.AddSizer(inner, 1, wx.EXPAND)
        outer.AddSizer(self.InitButtons(), 0, wx.ALIGN_BOTTOM)
        return outer

    def InitProgress(self):
        self.progressBar = wx.Gauge(self, -1, 100, style = wx.GA_HORIZONTAL | wx.GA_PROGRESSBAR)

        static = wx.StaticBox(self, -1, "Progress")
        box    = wx.StaticBoxSizer(static, wx.VERTICAL)
        box.Add(self.progressBar, 0, wx.EXPAND)
        box.AddSizer(self.InitLabels())
        return box

    def InitLabels(self):
        self.runCount       = wx.StaticText(self, -1, "", size = (30, 10))
        self.failureCount   = wx.StaticText(self, -1, "", size = (30, 10))
        self.errorCount     = wx.StaticText(self, -1, "", size = (30, 10))
        self.remainingCount = wx.StaticText(self, -1, "", size = (30, 10))
        for label in (self.runCount, self.failureCount, self.errorCount, self.remainingCount):
            label.SetForegroundColour(wx.BLUE);

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(wx.StaticText(self, -1, "Run:"), 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER)
        box.Add(self.runCount, 1, wx.EXPAND)
        box.Add(wx.StaticText(self, -1, "Failures:"), 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER)
        box.Add(self.failureCount, 1, wx.EXPAND)
        box.Add(wx.StaticText(self, -1, "Errors:"), 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER)
        box.Add(self.errorCount, 1, wx.EXPAND)
        box.Add(wx.StaticText(self, -1, "Remaining:"), 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER)
        box.Add(self.remainingCount, 1, wx.EXPAND)
        return box

    def InitDetail(self):
        self.errorInfo = []
        self.errorList = wx.ListBox(self, ID_ERROR_LIST)

        static = wx.StaticBox(self, -1, "Failures and Errors")
        box    = wx.StaticBoxSizer(static, wx.VERTICAL)
        box.Add(self.errorList, 1, wx.EXPAND)

        EVT_LISTBOX_DCLICK(self, ID_ERROR_LIST, self.OnErrorClick)

        return box

    def OnErrorClick(self, event):
        selection = self.errorList.GetSelection()
        if selection < 0:
            return

        txt = self.errorList.GetString(selection)
        test, error = self.errorInfo[selection]

        tracebackLines = apply(traceback.format_exception, error + (10,))
        tracebackText  = string.join(tracebackLines, "")

        msgBox = wx.MessageDialog(self, str(test) + tracebackText, txt)
        msgBox.ShowModal()

    def InitButtons(self):
        help  = wx.Button(self, ID_HELP,  "Help")
        about = wx.Button(self, ID_ABOUT, "About")
        close = wx.Button(self, ID_CLOSE, "Close")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(help)
        box.Add(about)
        box.Add(close)

        EVT_BUTTON(self, ID_HELP,  self.OnHelp)
        EVT_BUTTON(self, ID_ABOUT, self.OnAbout)
        EVT_BUTTON(self, ID_CLOSE, self.OnClose)
        
        return box

    def OnHelp(self, event):
        msgBox = wx.MessageDialog(self, HELP_TEXT, "wxUnit Help")
        msgBox.ShowModal()

    def OnAbout(self, event):
        msgBox = wx.MessageDialog(self, ABOUT_TEXT, "About wxUnit")
        msgBox.ShowModal()

    def OnClose(self, event):
        self.Close()

    def getSelectedTestName(self):
        return self.testName.GetValue()

    def errorDialog(self, title, message):
        dlg = wx.MessageDialog(self, message, title)
        dlg.ShowModal()

    def notifyRunning(self):
        self.SetRunCount(0)
        self.SetFailureCount(0)
        self.SetErrorCount(0)
        self.SetRemainingCount(self.totalTests)
        self.errorInfo = []
        self.errorList.Clear()
        self.startBtn.SetLabel("Stop")
        self.startBtn.Disable()
        self.progressBar.SetRange(self.totalTests)
        self.progressBar.SetValue(0)

    def notifyStopped(self):
        self.startBtn.SetLabel("Start")
        self.startBtn.Enable(TRUE)
        self.SetStatusText("Idle")

    def notifyTestStarted(self, test):
        self.SetStatusText(str(test))
        while wx.GetApp().Pending(): wx.GetApp().Dispatch()

    def notifyTestFailed(self, test, err):
        self.IncrementCount(self.failureCount)
        self.errorInfo.append((test, err))
        self.errorList.Append("Failure: %s" % test)

    def notifyTestErrored(self, test, err):
        self.IncrementCount(self.errorCount)
        self.errorInfo.append((test, err))
        self.errorList.Append("Error: %s" % test)
        self.SetErrorCount(self.GetErrorCount() + 1)

    def notifyTestFinished(self, test):
        self.IncrementCount(self.runCount)
        self.DecrementCount(self.remainingCount)
        if len(self.errorInfo) == 0: self.progressBar.SetForegroundColour(wx.GREEN)
        else:                        self.progressBar.SetForegroundColour(wx.RED)
        self.progressBar.SetValue(self.GetRunCount())

    def SetStatusText(self, text):
        self.status.SetStatusText(text)

    def SetRunCount(self, count):
        self.SetCount(self.runCount, count)

    def GetRunCount(self):
        return self.GetCount(self.runCount)

    def SetFailureCount(self, count):
        self.SetCount(self.failureCount, count)

    def GetFailureCount(self):
        return self.GetCount(self.failureCount)

    def SetErrorCount(self, count):
        self.SetCount(self.errorCount, count)

    def GetErrorCount(self):
        return self.GetCount(self.errorCount)

    def SetRemainingCount(self, count):
        self.SetCount(self.remainingCount, count)

    def GetRemainingCount(self, count):
        return self.GetCount(self.remainingCount)

    def IncrementCount(self, label):
        self.SetCount(label, self.GetCount(label) + 1)

    def DecrementCount(self, label):
        self.SetCount(label, self.GetCount(label) - 1)

    def SetCount(self, label, count):
        label.SetLabel(str(count))

    def GetCount(self, label):
        return int(label.GetLabel())


class RunApp(wx.App):

    def OnInit(self):
        self.frame = RunDialog(None, initialTestName)
        self.frame.Show(TRUE)
        self.SetTopWindow(self.frame)
        return TRUE


def main(initialTestName=""):
    app = RunApp()
    app.MainLoop()


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
