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

from wxPython.wx        import *

[DIALOG, CANCELBUTTON, FLAGVALUESTATICTEXT, FLAGVALUETEXTCTRL, SAVEBUTTON 
] = map(lambda _init_ctrls: wxNewId(), range(5))

class FlagToolDialog(wxDialog):
    """
    This class presents the user with a graphical means to sets the current
    flag value.
    """

    def CreateDialogContents(self, prnt):
        """
        Create all the contents of the dialog.
        """

        wxDialog.__init__(self, id=DIALOG, parent=prnt, title='Flag')
        
        self.flagValueStaticText = wxStaticText(id=FLAGVALUESTATICTEXT,
            label='Value:', parent=self)
            
        self.flagValueTextCtrl = wxTextCtrl(id=FLAGVALUETEXTCTRL,
            parent=self, value='0')
        self.flagValueTextCtrl.SetToolTipString('Enter a flag value to be assigned to flagged data points')
        
        self.saveButton = wxButton(id=SAVEBUTTON, label='Save', parent=self, 
            size=wxSize(75, 23))
        EVT_BUTTON(self.saveButton, SAVEBUTTON, self.OnSaveButton)
            
        self.cancelButton = wxButton(id=CANCELBUTTON, label='Cancel', 
            parent=self, size=wxSize(75, 23))
        EVT_BUTTON(self.cancelButton, CANCELBUTTON, self.OnCancelButton)

    def CreateSizer(self):
        """
        Fix up the dialog contents so that it displays well on any platform.
        """

        sizer = wxGridSizer(rows = 2, cols = 2, hgap = 2, vgap = 5)
        sizer.AddMany([(self.flagValueStaticText, 0, wxALIGN_CENTER),
                       (self.flagValueTextCtrl,   0, wxEXPAND),
                       (self.saveButton,        0, wxALIGN_CENTER),
                       (self.cancelButton,      0, wxALIGN_CENTER)])

        sizerBorder = wxBoxSizer(wxHORIZONTAL)
        sizerBorder.Add(sizer, 1, wxEXPAND | wxALL, 10)

        self.SetSizer(sizerBorder)
        self.SetAutoLayout(True)
        self.Fit()

    def __init__(self, parent):
        "Constructor for FlagToolDialog."

        self.CreateDialogContents(parent)
        self.CreateSizer()

    def OnSaveButton(self, event):
        """
        This method is invoked when the save button is pressed on the
        FlagToolDialog object.  wxID_OK indicates to the object invoking the
        dialog that the user wishes to change the information.
        """

        self.EndModal(wxID_OK)

    def OnCancelButton(self, event):
        """
        This method is invoked when the cancel button is pressed on the
        FlagToolDialog object.  wxID_CANCEL indicates to the object invoking
        the dialog that the user does not wish to change any information.
        """

        self.EndModal(wxID_CANCEL)

    def GetFlagValue(self):
        "Gets the current flag value."

        return int(self.flagValueTextCtrl.GetValue())

    def SetFlagValue(self, value):
        "Sets the current flag value."

        self.flagValueTextCtrl.SetValue(str(value))

# The piece of code below enables a FlagToolDialog to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    class MyApp(wxApp):
        def OnInit(self):
            dialog = FlagToolDialog(None)
            dialog.ShowModal()
            self.SetTopWindow(dialog)
            return True
    app = MyApp(0)
