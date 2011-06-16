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

import os
import wx

[DIALOG, CLOSEBUTTON, DEAPSTATICTEXT, DESCRIPSTATICTEXT, NRAOBITMAP
] = map(lambda _init_ctrls: wx.NewId(), range(5))

class AboutDialog(wx.Dialog):
    """
    Dialog used to convey application origination information to the user.
    """

    def CreateDialogContents(self, prnt):
        """
        Create all the contents of the dialog.
        """
        
        wx.Dialog.__init__(self, id=DIALOG, parent=prnt, title='About')

        self.versionStaticText = wx.StaticText(id=DEAPSTATICTEXT,
              label='DEAP v. 2.0', parent=self)
        self.versionStaticText.SetSize(self.versionStaticText.GetAdjustedBestSize())

        self.descripStaticText = wx.StaticText(id=DESCRIPSTATICTEXT,
              label='Created at the NRAO', parent=self)
        self.descripStaticText.SetSize(self.descripStaticText.GetAdjustedBestSize())

        if os.environ.has_key("DEAP"):
            root = os.environ["DEAP"]
        else:
            root = '.'

        self.nraoBitmap = wx.StaticBitmap(id=NRAOBITMAP, 
              bitmap=wx.Bitmap(root + '/gui/images/NRAO.bmp'), parent=self,
              size=wx.Size(50,50))
        self.nraoBitmap.SetSize(self.nraoBitmap.GetAdjustedBestSize())

        self.closeButton = wx.Button(id=CLOSEBUTTON, label='Close', parent=self,
              size=wx.Size(75, 23))
        self.closeButton.SetToolTipString('Close About window')
        wx.EVT_BUTTON(self.closeButton, CLOSEBUTTON, self.OnCloseButton)

    def CreateSizer(self):
        """
        Fix up the dialog contents so that it displays well on any platform.
        """

        sizer1 = wx.GridSizer(rows = 2, cols = 1, hgap = 0, vgap = 2)
        sizer1.AddMany([(self.versionStaticText,    0, wx.ALIGN_CENTER),
                        (self.descripStaticText, 0, wx.ALIGN_CENTER)])

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.closeButton, 1, wx.EXPAND | wx.ALL, 10)

        sizer3 = wx.GridSizer(rows = 2, cols = 1, hgap = 0, vgap = 2)
        sizer3.AddMany([(sizer1,          0, wx.ALIGN_CENTER),
                        (self.nraoBitmap, 0, wx.ALIGN_CENTER),
                        (sizer2,          0, wx.ALIGN_CENTER)])

        sizerBorder = wx.BoxSizer(wx.HORIZONTAL)
        sizerBorder.Add(sizer3, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizerBorder)
        self.SetAutoLayout(True)
        self.Fit()

    def __init__(self, parent):
        "Constructor for AboutDialog."
 
        self.CreateDialogContents(parent)
        self.CreateSizer()

    def OnCloseButton(self, event):
        """
        This method is invoked when the user clicks on the Close button.
        It simply exits the About dialog.
        """

        self.EndModal(wx.ID_OK)

# The piece of code below enables an AboutDialog to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            dialog = AboutDialog(None)
            self.SetTopWindow(dialog)
            dialog.ShowModal()
            dialog.Destroy()
            return True
    app = MyApp(0)
