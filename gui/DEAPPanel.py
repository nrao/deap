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
# Cambridge, MA 02139, USA.

from   framework        import *
from   OptionsDialog    import OptionsDialog
from   TutorialFrame    import TutorialFrame
from   UserManualFrame  import UserManualFrame
import os
import sys
import wx

[
    ID_TOOLBAR_USERMANUAL
  , ID_TOOLBAR_PRINT
  , ID_TOOLBAR_EXPORT
  , ID_TOOLBAR_UNDO
  , ID_TOOLBAR_UNFREEZE
  , ID_TOOLBAR_REDO
  , ID_TOOLBAR_UNZOOM
  , ID_TOOLBAR_ZOOM
  , ID_TOOLBAR_INFOTOOL
  , ID_TOOLBAR_ZOOMTOOL
  , ID_TOOLBAR_PANTOOL
  , ID_TOOLBAR_GRIDTOOL
] = map(lambda _init_coll_tool_bar_Tools: wx.NewId(), range(12))

[
    ID_FILE_EXPORT
  , ID_FILE_UNFREEZE
] = [wx.NewId() for i in range(2)]

[
    ID_TOOLS_INFO
  , ID_TOOLS_ZOOM
  , ID_TOOLS_PAN
  , ID_TOOLS_GRID
] = [wx.NewId() for i in range(4)]

[
    ID_VIEW_ZOOM
  , ID_VIEW_UNZOOM
  , ID_VIEW_ALL_PANELS
] = [wx.NewId() for i in range(3)]

[
    ID_HELP_MANUAL
  , ID_TUTORIAL
] = [wx.NewId() for i in range(2)]

class DEAPPanel(Panel):
    def __init__(self, parent, document):
        Panel.__init__(self, parent)

        self.document    = document
        self.historyFile = None

        self.InitPlot()

    def InitPlot(self):
        self.plotView = PlotView(self, -1)
        self.document.SetPlotter(self.plotView)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.plotView, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Fit()

    def ActivateSite(self, site):
        Panel.ActivateSite(self, site)
        self.ActivateMenus()
        self.ActivateToolBar()
        self.ActivateStatusBar()

        #self.GetDocument().GetCommandLine().push("matplotlib._pylab_helpers.Gcf.set_active(get_figure())")

    def ActivateMenus(self):
        self.ActivateFileMenu()
        self.ActivateEditMenu()
        self.ActivateViewMenu()
        self.ActivateToolsMenu()
        self.ActivateHelpMenu()

    def ActivateFileMenu(self):
        fileMnu = self.GetMenu(ID_FILE_MENU)
        filePos = fileMnu.GetMenuItemCount() - 1

        fileMnu.Insert(filePos, ID_FILE_EXPORT,   "&Export..."); filePos += 1
        fileMnu.Insert(filePos, ID_FILE_UNFREEZE, "Unfreeze");   filePos += 1
        fileMnu.InsertSeparator(filePos)

        wx.EVT_MENU(self.GetFrame(), ID_FILE_OPEN,      self.OnOpen)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_SAVE,      self.OnSave)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_SAVE_AS,   self.OnSaveAs)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_EXPORT,    self.OnExport)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_UNFREEZE,  self.OnUnfreeze)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_PPREVIEW,  self.OnPrintPreview)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_PRINT,     self.OnPrint)
        wx.EVT_MENU(self.GetFrame(), ID_FILE_PAGESETUP, self.OnPageSetup)

    def ActivateEditMenu(self):
        wx.EVT_MENU(self.GetFrame(), ID_EDIT_UNDO,  self.OnUndo)
        wx.EVT_MENU(self.GetFrame(), ID_EDIT_REDO,  self.OnRedo)
        wx.EVT_MENU(self.GetFrame(), ID_EDIT_CLEAR, self.OnClear)

    def ActivateViewMenu(self):
        viewMnu = self.GetMenu(ID_VIEW_MENU)
        viewMnu.Insert(0, ID_VIEW_ZOOM,   "Re&zoom")
        viewMnu.Insert(1, ID_VIEW_UNZOOM, "&Unzoom")
        viewMnu.InsertSeparator(2)
        viewMnu.InsertCheckItem(3, ID_VIEW_ALL_PANELS, "Display All Subplots")
        viewMnu.InsertSeparator(4)

        wx.EVT_MENU(self.GetFrame(), ID_VIEW_ZOOM,       self.OnZoom)
        wx.EVT_MENU(self.GetFrame(), ID_VIEW_UNZOOM,     self.OnUnzoom)
        wx.EVT_MENU(self.GetFrame(), ID_VIEW_ALL_PANELS, self.OnViewAllPanels)

    def ActivateToolsMenu(self):
        toolsMnu = self.GetMenu(self.GetMenuBar().GetMenuCount()+ID_TOOLS_MENU)
        toolsMnu.InsertCheckItem(0, ID_TOOLS_INFO, '&Info')
        toolsMnu.InsertCheckItem(1, ID_TOOLS_ZOOM, '&Zoom')
        toolsMnu.InsertCheckItem(2, ID_TOOLS_PAN,  '&Pan')
        toolsMnu.InsertCheckItem(3, ID_TOOLS_GRID, '&Grid')
        toolsMnu.InsertSeparator(4)

        wx.EVT_MENU(self.GetFrame(), ID_TOOLS_INFO, self.OnToolsInfo)
        wx.EVT_MENU(self.GetFrame(), ID_TOOLS_ZOOM, self.OnToolsZoom)
        wx.EVT_MENU(self.GetFrame(), ID_TOOLS_PAN,  self.OnToolsPan)
        wx.EVT_MENU(self.GetFrame(), ID_TOOLS_GRID, self.OnToolsGrid)

        wx.EVT_MENU(self.GetFrame(), ID_TOOLS_OPTIONS, self.OnOptions)

    def ActivateHelpMenu(self):
        helpMnu = self.GetMenu(self.GetMenuBar().GetMenuCount()+ID_HELP_MENU)
        helpPos = helpMnu.GetMenuItemCount() - 1
        helpMnu.Insert(helpPos, ID_HELP_MANUAL, "User &Manual")
        wx.EVT_MENU(self.GetFrame(), ID_HELP_MANUAL, self.OnUserManual)

        helpMnu = self.GetMenu(self.GetMenuBar().GetMenuCount()+ID_HELP_MENU)
        helpPos = helpMnu.GetMenuItemCount() - 1
        helpMnu.Insert(helpPos, ID_TUTORIAL, "&Tutorial")
        wx.EVT_MENU(self.GetFrame(), ID_TUTORIAL, self.OnTutorial)

    def ActivateToolBar(self):
        toolBar = self.GetToolBar()
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Print.bmp')),
              id=ID_TOOLBAR_PRINT, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Print.bmp')),
              shortHelpString='Print Plot')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Export.bmp')),
              id=ID_TOOLBAR_EXPORT, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Export.bmp')),
              shortHelpString='Export Plot')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Unfreeze.bmp')),
              id=ID_TOOLBAR_UNFREEZE, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Unfreeze.bmp')),
              shortHelpString='Unfreeze')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Undo.bmp')),
              id=ID_TOOLBAR_UNDO, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Undo.bmp')),
              shortHelpString='Undo')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Redo.bmp')),
              id=ID_TOOLBAR_REDO, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Redo.bmp')),
              shortHelpString='Redo')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Unzoom.bmp')),
              id=ID_TOOLBAR_UNZOOM, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Unzoom.bmp')),
              shortHelpString='Unzoom')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Zoom.bmp')),
              id=ID_TOOLBAR_ZOOM, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Zoom.bmp')),
              shortHelpString='Rezoom')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('InfoTool.bmp')),
              id=ID_TOOLBAR_INFOTOOL, isToggle=True,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('InfoTool.bmp')),
              shortHelpString='Info Tool')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('ZoomTool.bmp')),
              id=ID_TOOLBAR_ZOOMTOOL, isToggle=True,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('ZoomTool.bmp')),
              shortHelpString='Zoom Tool')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('PanTool.bmp')),
                  id=ID_TOOLBAR_PANTOOL, isToggle=True,
                  longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('PanTool.bmp')),
                  shortHelpString='Pan Tool')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('Grid.bmp')),
                id=ID_TOOLBAR_GRIDTOOL, isToggle=False,
                longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('Grid.bmp')),
                shortHelpString='Grid Tool')
        toolBar.AddTool(bitmap=wx.Bitmap(self.GetImagePath('UserManual.bmp')),
              id=ID_TOOLBAR_USERMANUAL, isToggle=False,
              longHelpString='', pushedBitmap=wx.Bitmap(self.GetImagePath('UserManual.bmp')),
              shortHelpString='User Manual')

        toolBar.ToggleTool(ID_TOOLBAR_INFOTOOL,  True)

        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_PRINT,     self.OnPrint)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_EXPORT,    self.OnExport)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_UNFREEZE,  self.OnUnfreeze)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_UNDO,      self.OnUndo)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_REDO,      self.OnRedo)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_UNZOOM,    self.OnUnzoom)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_ZOOM,      self.OnZoom)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_INFOTOOL,  self.OnToolsInfo)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_ZOOMTOOL,  self.OnToolsZoom)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_PANTOOL,   self.OnToolsPan)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_GRIDTOOL,  self.OnToolsGrid)
        wx.EVT_TOOL(self.GetFrame(), ID_TOOLBAR_USERMANUAL, self.OnUserManual)

        toolBar.Realize()

    def GetToolBar(self):
        if self.GetFrame() is not None:
            return self.GetFrame().GetToolBar()
        return None

    def ActivateStatusBar(self):
        pass

    def GetImagePath(self, image):
        return self.GetPath("gui/images/" + image)

    def GetPath(self, path):
        root = os.getcwd()
        if os.environ.has_key("DEAP"):
            root = os.environ["DEAP"]
        return os.path.normpath(os.path.join(root, path))

    def UpdateMenus(self):
        self.UpdateFileMenu()
        self.UpdateEditMenu()
        self.UpdateViewMenu()
        self.UpdateToolsMenu()
        self.UpdateHelpMenu()

    def UpdateFileMenu(self):
        self.GetMenuBar().Enable(ID_FILE_OPEN,    1)
        self.GetMenuBar().Enable(ID_FILE_SAVE,    1)
        self.GetMenuBar().Enable(ID_FILE_SAVE_AS, 1)
        self.GetMenuBar().Enable(ID_FILE_UNFREEZE,self.GetDocument().IsFrozen())
        self.GetMenuBar().Enable(ID_FILE_PAGESETUP, 1)
        self.GetMenuBar().Enable(ID_FILE_PPREVIEW,  1)
        self.GetMenuBar().Enable(ID_FILE_PRINT,     1)

        # OSX does previewing using PDFs and the Preview Application
        if sys.platform.startswith('darwin'):
            self.GetMenuBar().Enable(ID_FILE_PRINT,     0)
            self.GetMenuBar().Enable(ID_FILE_PAGESETUP, 0)
            self.GetMenuBar().Enable(ID_FILE_PPREVIEW,  0)

    def UpdateEditMenu(self):
        self.GetMenuBar().Enable(ID_EDIT_UNDO,  self.GetDocument().CanUndo())
        self.GetMenuBar().Enable(ID_EDIT_REDO,  self.GetDocument().CanRedo())
        self.GetMenuBar().Enable(ID_EDIT_CLEAR, 1)

    def UpdateViewMenu(self):
        self.GetMenuBar().Enable(ID_VIEW_ZOOM,   1)
        self.GetMenuBar().Enable(ID_VIEW_UNZOOM, self.GetPlotView().zoomed())
        self.GetMenuBar().Check(ID_VIEW_ALL_PANELS, not self.GetPlotView().AreSubplotsHidden())

    def UpdateToolsMenu(self):
        self.GetMenuBar().Check(ID_TOOLS_INFO, self.GetPlotView().IsInfoMode())
        self.GetMenuBar().Check(ID_TOOLS_ZOOM, self.GetPlotView().IsZoomMode())
        self.GetMenuBar().Check(ID_TOOLS_PAN,  self.GetPlotView().IsPanMode())
        self.GetMenuBar().Check(ID_TOOLS_GRID, self.GetPlotView().IsGridMode())

        self.GetMenuBar().Enable(ID_TOOLS_OPTIONS, 1)

    def UpdateHelpMenu(self):
        pass

    def GetPlotView(self):
        return self.plotView

    def GetCommandLine(self):
        return self.GetDocument().GetCommandLine()

    def GetDocument(self):
        """
        Returns a reference to the Document object contained within the
        MainFrame object.
        """
        return self.document

    def OnClear(self, event):
        self.GetPlotView().Clear()

    def OnOptions(self, event):
        cl     = self.GetCommandLine()
        dialog = OptionsDialog(self, -1)

        dialog.SetAutoComplete(cl.autoComplete)
        if wx.ID_OK <> dialog.ShowModal():
            dialog.destroy()
            return

        # TBF
        cl.autoComplete = dialog.GetAutoComplete()
        cl.wrap(dialog.GetWordWrap())

    def OnOpen(self, event):
        """
        Handles File->Open menu events.
        """
        default = self.historyFile or "commands.py"
        dialog = wx.FileDialog(self,
                              message = "Open Command Line History",
                              defaultFile = default,
                              wildcard = "Python Files (*.py)|*.py|All Files|*",
                              style=wx.OPEN)
        if wx.ID_OK <> dialog.ShowModal():
            return

        self.OpenFile(dialog.GetPath())

    def OpenFile(self, file):
        try:
            self.GetCommandLine().run("execfile('%s')" % file)
        except:
            pass

    def OnSave(self, event):
        """
        Handles File->Save menu events.
        """
        if self.historyFile is None:
            self.historyFile = self.QueryForFile()
        if self.historyFile is not None:
            self.SaveFile()

    def OnSaveAs(self, event):
        """
        Handles File->Save menu events.
        """
        self.historyFile = self.QueryForFile()
        if self.historyFile is not None:
            self.SaveFile()

    def QueryForFile(self):
        default = self.historyFile or "commands.py"
        dialog = wx.FileDialog(self,
                              message = "Save Command Line History",
                              defaultFile = default,
                              wildcard = "Python Files (*.py)|*.py|All Files|*",
                              style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if wx.ID_OK <> dialog.ShowModal():
            filename = None
        else:
            filename = dialog.GetPath()

        dialog.Destroy()

        return filename

    def SaveFile(self):
        history = self.GetHistory()

        f = open(self.historyFile, "w")
        f.writelines(history[::-1])
        f.close()

    def OnExport(self, event):
        """
        Handles File->Export menu events.
        """
        filename = wx.FileSelector('Save Plot', default_extension='png',
            wildcard=('Portable Network Graphics (*.png)|*.png|'
                + 'Encapsulated Postscript (*.eps)|*.eps|All files (*.*)|*.*'),
            parent=self, flags=wx.SAVE | wx.OVERWRITE_PROMPT)

        if not filename:
            return

        path, ext = os.path.splitext(filename)
        ext = ext[1:].lower()

        if ext != 'png' and ext != 'eps' and ext != 'ps':
            error_message = (
                'Only the PNG, PS, and EPS image formats are supported.\n'
                'A file extension of `png\', `ps\', or `eps\' must be used.')
            wx.MessageBox(error_message, 'Export Error',
                parent=self, style=wx.OK | wx.ICON_ERROR)
            return

        self.GetPlotView().Export(filename)

    def OnPrintPreview(self, event):
        """
        Handles File->Print Preview menu events
        """
        # OSX does previewing using PDFs and the Preview Application
        if sys.platform.startswith('darwin'): return
        self.GetPlotView().PrintPreview()

    def OnPageSetup(self, event):
        """
        Handles File->Page Setup menu events.
        """
        # OSX does previewing using PDFs and the Preview Application
        if sys.platform.startswith('darwin'): return
        self.GetPlotView().PageSetup()

    def OnPrint(self, event):
        """
        Handles File->Print menu events
        """
        # OSX does previewing using PDFs and the Preview Application
        if sys.platform.startswith('darwin'): return
        self.GetPlotView().Print()

    def OnUnfreeze(self, event):
        "Handler for unfreeze event."
        self.GetDocument().Unfreeze()

    def OnUndo(self, event):
        "Handler for undo event."
        self.GetDocument().Undo()

    def OnRedo(self, event):
        "Handler for redo event."
        self.GetDocument().Redo()

    def OnViewAllPanels(self, event):
        self.GetPlotView().DisplayAllSubplots()

    def OnZoom(self, event):
        "Handler for a zoom event."
        self.GetPlotView().ZoomIn()

    def OnUnzoom(self, event):
        "Handler for an unzoom event."
        self.GetPlotView().ZoomOut()

    def OnToolsInfo(self, event):
        "Handler for an info tool selection event."
        self.GetToolBar().ToggleTool(ID_TOOLBAR_INFOTOOL, True)
        self.GetToolBar().ToggleTool(ID_TOOLBAR_ZOOMTOOL, False)
        self.GetToolBar().ToggleTool(ID_TOOLBAR_PANTOOL,  False)
        self.GetPlotView().SetInfoMode()

    def OnToolsZoom(self, event):
        "Handler for a zoom tool selection event."
        self.GetToolBar().ToggleTool(ID_TOOLBAR_INFOTOOL, False)
        self.GetToolBar().ToggleTool(ID_TOOLBAR_ZOOMTOOL, True)
        self.GetToolBar().ToggleTool(ID_TOOLBAR_PANTOOL,  False)
        self.GetPlotView().SetZoomMode()

    def OnToolsPan(self, event):
        "Handler for a pan tool selection event."
        self.GetToolBar().ToggleTool(ID_TOOLBAR_INFOTOOL, False)
        self.GetToolBar().ToggleTool(ID_TOOLBAR_ZOOMTOOL, False)
        self.GetToolBar().ToggleTool(ID_TOOLBAR_PANTOOL,  True)
        self.GetPlotView().SetPanMode()

    def OnToolsGrid(self, event):
        "Handler for a grid tool selection event."
        self.GetToolBar().ToggleTool(ID_TOOLBAR_GRIDTOOL, True)
        self.GetPlotView().SetGridMode()

    def OnUserManual(self, event):
        "Handler for a user help event."
        frame = UserManualFrame(self)
        frame.Show(True)

    def OnTutorial(self, event):
        "Handler for a user tutorial event."
        frame = TutorialFrame(self)
        frame.Show(True)
