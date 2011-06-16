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

from AboutDialog import AboutDialog
from DEAPPanel   import DEAPPanel
from DEAPPyShell import DEAPPyShell
from framework   import *
import wx

class DEAPFrame(Frame):

    def __init__(self, parent, interpreter):
        Frame.__init__(self, parent, -1, "DEAP", size = (740, 580))

        self.interpreter = interpreter

        self.InitSplitter()
        self.ActivatePanel(self.plotPanel)
        self.SetStatusText("Welcome to DEAP!")

    def InitSplitter(self):
        self.splitter    = wx.SplitterWindow(self, -1)
        self.plotPanel   = self.InitPlotPanel(self.splitter)
        self.commandLine = self.InitCommandLine(self.splitter)

        self.GetInterpreter().SetCommandLine(self.commandLine)

        self.splitter.SplitHorizontally(self.plotPanel, self.commandLine, -150)
        self.splitter.SetMinimumPaneSize(20)

    def InitPlotPanel(self, parent):
        return DEAPPanel(parent, self.GetInterpreter().GetDocument())

    def InitCommandLine(self, parent):
        return DEAPPyShell(parent, self.GetInterpreter())

    def InitHelpMenu(self):
        helpMnu = Frame.InitHelpMenu(self)

        wx.EVT_MENU(self, ID_HELP_ABOUT, self.OnAbout)
        return helpMnu

    def OnAbout(self, event):
        dialog = AboutDialog(self)
        dialog.ShowModal()

    def OnExit(self, event):
        "Handles for exit event."
        self.commandLine.Close()
        self.Close()
        self.Destroy()

    def GetInterpreter(self):
        return self.interpreter

    def SetHistory(self, history):
        self.commandLine.SetHistory(history)

    def GetHistory(self):
        return self.commandLine.GetHistory()

    def OpenFile(self, file):
        self.plotPanel.OpenFile(file)
