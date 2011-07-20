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

# File Edit View [ ... your menus here ... ] Tools Help
ID_FILE_MENU   =  0
ID_EDIT_MENU   =  1
ID_VIEW_MENU   =  2
ID_TOOLS_MENU  = -2
ID_HELP_MENU   = -1

[
    ID_FILE_OPEN
  , ID_FILE_CLOSE
  , ID_FILE_SAVE
  , ID_FILE_SAVE_AS
  , ID_FILE_SAVE_ALL
  , ID_FILE_PRINT
  , ID_FILE_PAGESETUP
  , ID_FILE_PPREVIEW
  , ID_FILE_EXIT
] = [wx.NewId() for i in range(9)]

[
    ID_EDIT_UNDO
  , ID_EDIT_REDO
  , ID_EDIT_CUT
  , ID_EDIT_COPY
  , ID_EDIT_PASTE
  , ID_EDIT_DELETE
  , ID_EDIT_SELECT_ALL
  , ID_EDIT_CLEAR
] = [wx.NewId() for i in range(8)]

[
    ID_VIEW_TOOLBAR
  , ID_VIEW_STATUSBAR
  , ID_VIEW_FULLSCREEN
] = [wx.NewId() for i in range(3)]

[
    ID_TOOLS_PLOTEDIT,
    ID_TOOLS_OPTIONS
] = [wx.NewId() for i in range(2)]

[
    ID_HELP_SELF_TEST
  , ID_HELP_ABOUT
] = [wx.NewId() for i in range(2)]

class Frame(wx.Frame):
    """
    Plays host to panels by allowing them to customize the interface
    in activation and deactivation.
    """

    def __init__(self, parent, id, title, pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        
        # Keep a record of dynamic connections for later disconnection.
        self.connections = []
        
        # Initialize menus and toolbars.
        self.InitFrame()

        # Keep track of the currently active panel for later deactivation.
        self.panel = None
        
    def Connect(self, id, lastId, eventType, function):
        "Override the default in order to cache event connections."
        self.connections.append((id, lastId, eventType))
        wx.Frame.Connect(self, id, lastId, eventType, function)
        
    def ActivatePanel(self, panel):
        "Make a new panel active within this site."
        
        # Catch case where previously active panel was not explicitly deactivated.
        if self.GetPanel() is not None:
            self.DeactivatePanel()
            
        # Give the new panel a chance to make any necessary customizations.
        self.SetPanel(panel)
        if self.GetPanel() is not None:
            self.GetPanel().ActivateSite(self)
            
    def DeactivatePanel(self):
        "Remove an existing panel from active service."
        
        # Give the panel a chance to do its own cleanup.
        if self.GetPanel() is not None:
            self.GetPanel().DeactivateSite()
        self.SetPanel(None)

        # But don't take any chances on getting left in a bad state.  Do our own clean-up.
        self.InitFrame()
        
    def InitFrame(self):
        "The easiest way to clean-up is just to re-initialize everything."

        # Disconnect any dynamic event connections.
        for t in self.connections:
            apply(self.Disconnect, t)

        # Proceed with standard initialization.
        self.InitMenus()
        self.InitToolBar()
        self.InitStatusBar()

    def GetPanel(self):
        "Return the currently active panel."
        return self.panel

    def SetPanel(self, panel):
        "Define the currently active panel."
        self.panel = panel

    def GetFrame(self):
        "Return the hosting frame."
        return self

    def GetMenu(self, id):
        "Return the specified menu."
        return self.GetMenuBar().GetMenu(id)

    def InitStatusBar(self):
        isShown = 1
        if self.GetStatusBar() is not None:
            sb = self.GetStatusBar()
            isShown = sb.IsShown()
            self.SetStatusBar(None)
            sb.Destroy()
        self.CreateStatusBar()
        self.GetStatusBar().Show(isShown)

    def InitToolBar(self):
        isShown = 1
        if self.GetToolBar() is not None:
            tb = self.GetToolBar()
            isShown = tb.IsShown()
            self.SetToolBar(None)
            tb.Destroy()
        self.CreateToolBar()
        self.GetToolBar().SetToolBitmapSize((23,25))
        self.GetToolBar().Show(isShown)
        self.GetToolBar().AddTool(bitmap=wx.Bitmap(self.GetImagePath('Open.bmp')), id=ID_FILE_OPEN, isToggle=False, shortHelpString='Open')
        self.GetToolBar().AddTool(bitmap=wx.Bitmap(self.GetImagePath('Save.bmp')), id=ID_FILE_SAVE, isToggle=False, shortHelpString='Save')
        self.GetToolBar().Realize()

    def InitMenus(self):
        if self.GetMenuBar() is not None:
            mb = self.GetMenuBar()
            self.SetMenuBar(None)
            mb.Destroy()
        menuBar = wx.MenuBar()
        menuBar.Append(self.InitFileMenu(),   "&File")
        menuBar.Append(self.InitEditMenu(),   "&Edit")
        menuBar.Append(self.InitViewMenu(),   "&View")
        menuBar.Append(self.InitToolsMenu(),  "&Tools")
        menuBar.Append(self.InitHelpMenu(),   "&Help")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU_OPEN(self, self.UpdateMenus)

    def InitFileMenu(self):        
        fileMnu = wx.Menu()
        fileMnu.Append(ID_FILE_OPEN, "&Open...\tCtrl+O", "Open a file.")
        fileMnu.Append(ID_FILE_CLOSE, "&Close\tCtrl+W", "Close the current window.")
        fileMnu.AppendSeparator()
        fileMnu.Append(ID_FILE_SAVE, "&Save\tCtrl+S", "Save the current window.")
        fileMnu.Append(ID_FILE_SAVE_AS, "Save As...", "Save the current window to a new file.")
        fileMnu.Append(ID_FILE_SAVE_ALL, "Save &All", "Save all open windows.")
        fileMnu.AppendSeparator()
        fileMnu.Append(ID_FILE_PAGESETUP, 'Page Setup...',
            'Modify the print settings current plot')
        fileMnu.Append(ID_FILE_PPREVIEW, 'Print Pre&view...',
            'Preview the print version of the current plot')
        fileMnu.Append(ID_FILE_PRINT, '&Print...\tCtrl+P', 'Print the current plot')
        fileMnu.AppendSeparator()
        fileMnu.Append(ID_FILE_EXIT, "E&xit\tCtrl+Q", "Quit the application.")

        wx.EVT_MENU(self, ID_FILE_EXIT, self.OnExit)
        return fileMnu

    def InitEditMenu(self):    
        editMnu = wx.Menu()
        editMnu.Append(ID_EDIT_UNDO,       "&Undo\tCtrl+Z")
        editMnu.Append(ID_EDIT_REDO,       "&Redo\tCtrl+Y")
        editMnu.AppendSeparator()
        editMnu.Append(ID_EDIT_CUT,        "Cu&t\tCtrl+X")
        editMnu.Append(ID_EDIT_COPY,       "&Copy\tCtrl+C")
        editMnu.Append(ID_EDIT_PASTE,      "&Paste\tCtrl+V")
        editMnu.Append(ID_EDIT_DELETE,     "&Delete\tDel")
        editMnu.AppendSeparator()
        editMnu.Append(ID_EDIT_SELECT_ALL, "Select &All\tCtrl+A")
        editMnu.Append(ID_EDIT_CLEAR,      "Clear\tDel")
        return editMnu

    def InitViewMenu(self):
        viewMnu = wx.Menu()
        viewMnu.AppendCheckItem(ID_VIEW_TOOLBAR,    "&Toolbar")
        viewMnu.AppendCheckItem(ID_VIEW_STATUSBAR,  "Status &Bar")
        viewMnu.AppendSeparator()
        viewMnu.AppendCheckItem(ID_VIEW_FULLSCREEN, "&Full Screen")

        wx.EVT_MENU(self, ID_VIEW_TOOLBAR,    self.OnToolBar)
        wx.EVT_MENU(self, ID_VIEW_STATUSBAR,  self.OnStatusBar)
        wx.EVT_MENU(self, ID_VIEW_FULLSCREEN, self.OnFullScreen)
        return viewMnu

    def InitToolsMenu(self):    
        toolsMnu = wx.Menu()
        toolsMnu.Append(ID_TOOLS_PLOTEDIT,       "&Edit Plot...")
        toolsMnu.Append(ID_TOOLS_OPTIONS,        "&Options...")
        return toolsMnu

    def InitHelpMenu(self):        
        helpMnu = wx.Menu()
        helpMnu.Append(ID_HELP_SELF_TEST,        "&Self Test...")
        helpMnu.AppendSeparator()
        helpMnu.Append(ID_HELP_ABOUT,            "&About...")
        return helpMnu

    def UpdateMenus(self, event):
        "Give hosted panels the opportunity to update menus dynamically as they are opened."
        self.UpdateFileMenu()
        self.UpdateEditMenu()
        self.UpdateViewMenu()
        self.UpdateToolsMenu()
        self.UpdateHelpMenu()
        if self.GetPanel() is not None:
            self.GetPanel().UpdateMenus()

    def UpdateFileMenu(self):
        for id in (ID_FILE_OPEN, ID_FILE_CLOSE, ID_FILE_SAVE, ID_FILE_SAVE_AS, ID_FILE_SAVE_ALL, ID_FILE_PRINT, ID_FILE_PPREVIEW, ID_FILE_PAGESETUP):
            self.GetMenuBar().Enable(id, 0)
        self.GetMenuBar().Enable(ID_FILE_EXIT, 1)

    def UpdateEditMenu(self):
        for id in (ID_EDIT_UNDO,  ID_EDIT_REDO,   ID_EDIT_CUT,        ID_EDIT_COPY,
                   ID_EDIT_PASTE, ID_EDIT_DELETE, ID_EDIT_SELECT_ALL, ID_EDIT_CLEAR):
            self.GetMenuBar().Enable(id, 0)

    def UpdateViewMenu(self):
        self.GetMenuBar().Check(ID_VIEW_TOOLBAR,    self.GetToolBar()   is not None and self.GetToolBar().IsShown())
        self.GetMenuBar().Check(ID_VIEW_STATUSBAR,  self.GetStatusBar() is not None and self.GetStatusBar().IsShown())
        self.GetMenuBar().Check(ID_VIEW_FULLSCREEN, self.IsFullScreen())

    def UpdateToolsMenu(self):
        self.GetMenuBar().Enable(ID_TOOLS_OPTIONS, 0)

    def UpdateHelpMenu(self):
        pass

    def OnExit(self, event):
        self.Close()

    def OnToolBar(self, event):
        toolBar = self.GetToolBar()
        if toolBar is not None:
            toolBar.Show(not toolBar.IsShown())
        self.SendSizeEvent()

    def OnStatusBar(self, event):
        statusBar = self.GetStatusBar()
        if statusBar is not None:
            statusBar.Show(not statusBar.IsShown())
        self.SendSizeEvent()

    def OnFullScreen(self, event):
        self.ShowFullScreen(not self.IsFullScreen()
                          , wx.FULLSCREEN_NOTOOLBAR | wx.FULLSCREEN_NOSTATUSBAR | wx.FULLSCREEN_NOBORDER | wx.FULLSCREEN_NOCAPTION)

    def GetImagePath(self, image):
        return self.GetPath("gui/images/" + image)

    def GetPath(self, path):
        root     = os.getcwd()
        if os.environ.has_key("DEAP"):
            root = os.environ["DEAP"]
        return os.path.normpath(os.path.join(root, path))

# The piece of code below enables a Frame to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            frame = Frame(None, -1, "Test")
            self.SetTopWindow(frame)
            frame.Show()
            return True
    app = MyApp(0)
    app.MainLoop()
