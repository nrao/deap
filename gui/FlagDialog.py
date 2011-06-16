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
# You should have received a copy of the GNU General Public License along with# this program; if not, write to the
#
# Free Software Foundation, Inc.,
# 675 Mass Ave
# Cambridge, MA 02139, USA.

from wxPython.wx        import *

[DIALOG, CANCELBUTTON, FLAGCOLORCHOICE, FLAGCOLORSTATICTEXT, FLAGSHOWCHECKBOX, 
 FLAGVALUESTATICTEXT, FLAGVALUETEXTCTRL, SAVEBUTTON, 
] = map(lambda _init_ctrls: wxNewId(), range(8))

class FlagDialog(wxDialog):
    """
    This class presents the user with a graphical means to set flag properties.
    """

    def CreateDialogContents(self, prnt):
        """
        Create all the contents of the dialog.
        """

        wxDialog.__init__(self, id=DIALOG, parent=prnt, title='Flag Properties')
        
        self.flagValueStaticText = wxStaticText(id=FLAGVALUESTATICTEXT,
            label='Value:', parent=self)
            
        self.flagValueTextCtrl = wxTextCtrl(id=FLAGVALUETEXTCTRL,
            parent=self, value='0')
        self.flagValueTextCtrl.SetToolTipString('Enter a flag value to be assigned to flagged data points')
        
        self.flagColorStaticText = wxStaticText(id=FLAGCOLORSTATICTEXT,
            label='Color:', parent=self)
            
        self.flagColorChoice = wxChoice(id=FLAGCOLORCHOICE, parent=self,
            choices=['black', 'white', 'red', 'green', 'blue', 'cyan', 
                     'magenta', 'yellow', 'orange', 'green-yellow', 
                     'green-cyan', 'blue-cyan', 'blue-magenta', 'red-magenta', 
                     'dark gray', 'light gray'])
        self.flagColorChoice.SetStringSelection('red')
        self.flagColorChoice.SetToolTipString('Select a color for flags with the specified flag value')
 
        self.flagShowCheckBox = wxCheckBox(id=FLAGSHOWCHECKBOX, label='Show', 
            parent=self)
        self.flagShowCheckBox.SetValue(True)

        self.saveButton = wxButton(id=SAVEBUTTON, label='Save', parent=self)
        EVT_BUTTON(self.saveButton, SAVEBUTTON, self.OnSaveButton)

        self.cancelButton = wxButton(id=CANCELBUTTON,label='Cancel',parent=self)
        EVT_BUTTON(self.cancelButton, CANCELBUTTON, self.OnCancelButton)

    def CreateSizer(self):
        """
        Fix up the dialog contents so that it displays well on any platform.
        """

        sizer1 = wxGridSizer(rows = 2, cols = 2, hgap = 0, vgap = 2)
        sizer1.AddMany([(self.flagValueStaticText, 0, wxALIGN_CENTER),
                        (self.flagValueTextCtrl,   0, wxEXPAND),
                        (self.flagColorStaticText, 0, wxALIGN_CENTER),
                        (self.flagColorChoice,     0, wxEXPAND)])

        sizer2 = wxGridSizer(rows = 1, cols = 2, hgap = 5, vgap = 2)
        sizer2.AddMany([(self.saveButton,   0, wxALIGN_CENTER),
                        (self.cancelButton, 0, wxALIGN_CENTER)])

        sizer3 = wxFlexGridSizer(rows = 3, cols = 1, hgap = 5, vgap = 10)
        sizer3.AddMany([(sizer1,                0, wxALIGN_CENTER),
                        (self.flagShowCheckBox, 0, wxALIGN_CENTER),
                        (sizer2,                0, wxALIGN_CENTER)])

        sizerBorder = wxBoxSizer(wxHORIZONTAL)
        sizerBorder.Add(sizer3, 1, wxEXPAND | wxALL, 10)

        self.SetSizer(sizerBorder)
        self.SetAutoLayout(True)
        self.Fit()

    def __init__(self, parent):
        "Constructor for FlagDialog."

        self.CreateDialogContents(parent)
        self.CreateSizer()
        
    def OnSaveButton(self, event):
        """
        This method is invoked when the save button is pressed on the
        FlagDialog object.  wxID_OK indicates to the object invoking the
        dialog that the user wishes to change the information.
        """

        self.EndModal(wxID_OK)

    def OnCancelButton(self, event):
        """
        This method is invoked when the cancel button is pressed on the
        FlagDialog object.  wxID_CANCEL indicates to the object invoking the
        dialog that the user does not wish to change any information.
        """

        self.EndModal(wxID_CANCEL)

    def GetFlagValue(self):
        "Gets the current flag value."

        return int(self.flagValueTextCtrl.GetValue())

    def SetFlagValue(self, value):
        "Sets the current flag value."

        self.flagValueTextCtrl.SetValue(str(value))

    def GetFlagColor(self):
        "Gets the color associated with the current flag value."

        return self.flagColorChoice.GetSelection()

    def SetFlagColor(self, color):
        "Sets the color associated with the current flag value."

        self.flagColorChoice.SetSelection(color)

    def GetFlagShow(self):
        "Gets the display attribute assocaited with the current flag value."

        return self.flagShowCheckBox.GetValue()

    def SetFlagShow(self, show):
        "Sets the display attribute associated with the current flag value."

        self.flagShowCheckBox.SetValue(show)

# The piece of code below enables a FlagDialog to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    class MyApp(wxApp):
        def OnInit(self):
            dialog = FlagDialog(None)
            self.SetTopWindow(dialog)
            dialog.ShowModal()
            return True
    app = MyApp(0)
