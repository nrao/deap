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
import os.path
import sys
import wx
import wx.html as html

class HtmlWindow(html.HtmlWindow):
    """
    The HtmlWindow class displays the user manual for DEAP.
    """

    def __init__(self, parent, id):
        "Constructor for HtmlWindow."

        html.HtmlWindow.__init__(self, parent, id, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        wx.EVT_SCROLLWIN(self, self.OnScroll)

    def OnScroll(self, event):
        "Handles scroll events."

        event.Skip()

    def OnLinkClicked(self, linkinfo):
        "Handles link selection events."

        # Virtuals in the base class have been renamed with base_ on the front.
        self.base_OnLinkClicked(linkinfo)

    def OnSetTitle(self, title):
        "Handles title setting events."

        self.base_OnSetTitle(title)

    def OnCellMouseHover(self, cell, x, y):
        "Handles mouse hovers over cell events."

        self.base_OnCellMouseHover(cell, x, y)

    def OnCellClicked(self, cell, x, y, evt):
        "Handles mouse click on cell events."

        self.base_OnCellClicked(cell, x, y, evt)

class HtmlPanel(wx.Panel):
    """
    The HtmlPanel is a container for the HtmlWindow and it also allows the
    user to open other HTML pages resident on the local machine.
    """

    def __init__(self, parent, frame, file):
        "Constructor for HtmlPanel."

        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.frame = frame
        self.file  = file
        self.cwd = os.path.split(sys.argv[0])[0]
        if not self.cwd:
            self.cwd = os.getcwd()
        if frame:
            self.titleBase = frame.GetTitle()

        self.html = HtmlWindow(self, -1)
        self.html.SetRelatedFrame(frame, self.titleBase + " -- %s")
        self.html.SetRelatedStatusBar(0)

        self.printer = html.HtmlEasyPrinting()
        buttonSizer  = self.CreateBrowserButtons()

        self.SetSizer(buttonSizer)
        self.SetAutoLayout(True)
        self.Fit()

        self.OnShowDefault(None)

    def CreateBrowserButtons(self):
        "Creates the browser buttons at the bottom of the frame."

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        # Basic HTML navigation buttons
        btn = wx.Button(self, -1, "Load File")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnLoadFile)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Load URL")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnLoadURL)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Back")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnBack)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Forward")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnForward)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Print")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnPrint)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "View Source")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnViewSource)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Close Window")
        btn.SetSize(btn.GetAdjustedBestSize())
        wx.EVT_BUTTON(self, btn.GetId(), self.OnCloseWindow)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.html, 1, wx.GROW)

        box.Add(subbox, 0, wx.GROW)

        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOk)

        return box

    def OnShowDefault(self, event):
        "Handles default HTML display events."

        page = self.file
        if page is None:
            return
        if page[:4] <> "http":
            root     = os.getcwd()
            if os.environ.has_key("DEAP"):
                root = os.environ["DEAP"]
            page = os.path.normpath(os.path.join(root, page))

        self.html.LoadPage(page)

    def OnLoadFile(self, event):
        "Handles HTML file load events."

        dlg = wx.FileDialog(self, wildcard = '*.htm*', style=wx.OPEN)
        if dlg.ShowModal():
            path = dlg.GetPath()
            self.html.LoadPage(path)
        dlg.Destroy()

    def OnLoadURL(self, event):
        "Handles URL load events."

        dlg = wx.TextEntryDialog(self, "Enter a URL")
        if dlg.ShowModal():
            url = dlg.GetValue()
            self.html.LoadPage(url)
        dlg.Destroy()

    def OnOk(self, event):
        "Handles OK button press events."

        pass

    def OnBack(self, event):
        """
        Handles events generated when the user wishes to return to the
        HTML previously viewed (undo).
        """

        if not self.html.HistoryBack():
            wx.MessageBox("No more items in history!")

    def OnForward(self, event):
        """
        Handles events generated when the user wishes to return to the
        HTML previously viewed (redo).
        """

        if not self.html.HistoryForward():
            wx.MessageBox("No more items in history!")

    def OnViewSource(self, event):
        """
        Handles requests from the user to view HTML source code for a
        particular HTML file.
        """

        source = self.html.GetParser().GetSource()
        dlg = wx.ScrolledMessageDialog(self, source, 'HTML Source')
        dlg.ShowModal()
        dlg.Destroy()

    def OnCloseWindow(self, event):
        "Closes the user manual window."

        self.Close()
        self.frame.Close()
        self.frame.Destroy()

    def OnPrint(self, event):
        "Handles print events."

        self.printer.PrintFile(self.html.GetOpenedPage())

class HtmlFrame(wx.Frame):
    """
    This class is a container for the UserManualPanel.
    """

    def _init_coll_status_bar_Fields(self, parent):
        "Initializes the status bar."

        parent.SetFieldsCount(1)
        parent.SetStatusText(text='Welcome to the DEAP User Help Pages!')
        parent.SetStatusWidths([-1])

    def __init__(self, prnt, frameTitle, file):
        "Constructor for HtmlFrame."

        wx.Frame.__init__(self, id=0, parent=prnt, size=wx.Size(640, 480),
              title=frameTitle)

        self.status_bar = wx.StatusBar(id=0,
              name='status_bar', parent=self, style=0)
        self._init_coll_status_bar_Fields(self.status_bar)
        self.SetStatusBar(self.status_bar)
        self.CreatePanel(file)

    def CreatePanel(self, file):
        self.panel = HtmlPanel(self, self, file)

# The piece of code below enables an HtmlFrame to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            frame = HtmlFrame(None)
            self.SetTopWindow(frame)
            frame.Show()
            return True
    app = MyApp(0)
    app.MainLoop()
