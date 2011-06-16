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
# along with this program; if not, write to the Free Software Foundation,
# Inc., 675 Mass Ave Cambridge, MA 02139, USA.
#
# Correspondence concerning GBT software should be addressed as follows:
#     GBT Operations
#     National Radio Astronomy Observatory
#     P. O. Box 2
#     Green Bank, WV 24944-0002 USA

import wx

class ShellOptions(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.InitGUI()

    def InitGUI(self):
        self.autoComplete = wx.CheckBox(self, -1, "Auto-Complete")
        self.callTipShow  = wx.CheckBox(self, -1, "Show Call Tips")
        self.wordWrap     = wx.CheckBox(self, -1, "Word Wrap")

        box = wx.BoxSizer(wx.VERTICAL)
        box.AddSizer(self.autoComplete, 1, wx.EXPAND)
        box.AddSizer(self.callTipShow,  1, wx.EXPAND)
        box.AddSizer(self.wordWrap,     1, wx.EXPAND)

        self.SetSizer(box)
        self.SetAutoLayout(1)
        self.Fit()

    def GetAutoComplete(self):
        return self.autoComplete.GetValue()

    def SetAutoComplete(self, state):
        self.autoComplete.SetValue(state)

    def GetCallTipShow(self):
        return self.callTipShow.GetValue()

    def SetCallTipShow(self, state):
        self.callTipShow.SetValue(state)

    def GetWordWrap(self):
        return self.wordWrap.GetValue()

    def SetWordWrap(self, state):
        self.wordWrap.SetValue(state)

class OptionsDialog(wx.Dialog):

    def __init__(self, parent, mode):
        wx.Dialog.__init__(self, parent, -1, "Options")
        self.InitGUI()

    def InitGUI(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.AddSizer(self.InitNotebook(), 0, wx.EXPAND)
        box.AddSpacer((10, 10))
        box.AddSizer(self.InitButtons(),  0, wx.CENTER)

        self.SetSizer(box)
        self.SetAutoLayout(1)
        self.Fit()

    def InitNotebook(self):
        self.notebook = wx.Notebook(self, -1)

        self.shellOptions = ShellOptions(self.notebook, -1)
        self.notebook.AddPage(self.shellOptions, "Command Line Options", select = True)

        self.notebook.Fit()

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.notebook, 0, wx.EXPAND)

        return box

    def InitButtons(self):
        self.ok = wx.Button(self, wx.ID_OK, "OK")
        self.ok.SetToolTipString("Apply changes and exit dialog.")

        self.cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.cancel.SetToolTipString("Ignore changes and exit dialog.")

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.ok,     0, wx.CENTER)
        box.Add(self.cancel, 0, wx.CENTER)

        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOK)        

        return box

    def OnOK(self, event):
        wx.Dialog.EndModal(self, wx.ID_OK)

    def GetAutoComplete(self):
        return self.shellOptions.GetAutoComplete()

    def SetAutoComplete(self, state):
        self.shellOptions.SetAutoComplete(state)

    def GetCallTipShow(self):
        return self.shellOptions.GetCallTipShow()

    def SetCallTipShow(self, state):
        self.shellOptions.SetCallTipShow(state)

    def GetWordWrap(self):
        return self.shellOptions.GetWordWrap()

    def SetWordWrap(self, state):
        self.shellOptions.SetWordWrap(state)

# The piece of code below enables this dialog to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            dialog = OptionsDialog(None, "Options")
            self.SetTopWindow(dialog)
            dialog.ShowModal()
            dialog.Destroy()
            return True
    app = MyApp(0)
