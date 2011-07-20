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

from   wxmpl   import AxesLimits
from   wxmpl   import PlotPanel
from   wxmpl   import PlotPanelDirector
from   wxmpl   import FigurePrinter
from   wxmpl   import FigurePrintout
from   wxmpl   import LocationPainter
from   wxmpl   import LINUX_PRINTING_COMMAND
import weakref
import wx
import wxmpl
from   matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from   matplotlib.transforms import bound_vertices, inverse_transform_bbox

#
# Utility functions and classes
#

def is_log_x(axes):
    """
    Returns a boolean indicating if C{axes} contains log axes.
    """
    if axes is not None:
        return axes.get_xscale() == 'log'

def is_log_y(axes):
    """
    Returns a boolean indicating if C{axes} contains log axes.
    """
    if axes is not None:
        return axes.get_yscale() == 'log'

def get_data(axes, x, y):
    """
    Returns the corresponding data coordinates C{xdata, ydata} as a 2-tuple.

    If no axes is specified, a 2-tuple of C{None} is returned.
    """
    if axes is None: return None, None

    return axes.transData.inverse_xy_tup((x, y))

def get_selected_data(axes, x1, y1, x2, y2):
    """
    Verifies that the axes in question overlaps with the canvas area
    from C{(x1, y1)} to C{(x1, y1)}.  The corresponding X and Y axes ranges 
    are returned as a 3-tuple.

    If no axes overlaps with the specified area, 2-tuple of C{None}s is
    returned.
    """
    if axes is None: return None, None

    bbox = bound_vertices([(x1, y1), (x2, y2)])

    bxr, byr = wxmpl.get_bbox_lims(bbox)
    axr, ayr = wxmpl.get_bbox_lims(axes.bbox)

    xmin = max(bxr[0], axr[0])
    xmax = min(bxr[1], axr[1])
    ymin = max(byr[0], ayr[0])
    ymax = min(byr[1], ayr[1])
    return wxmpl.get_bbox_lims(
           inverse_transform_bbox(axes.transData,
                                  bound_vertices([(xmin, ymin), (xmax, ymax)])))

class MyAxesLimits(AxesLimits):
    """
    Extended base class to include rezooming capabilities.
    """
    def __init__(self):
        AxesLimits.__init__(self)
        self.redo_history = weakref.WeakKeyDictionary()

    def _get_redo_history(self, axes):
        """
        Returns the redo history list of X and Y limits associated with C{axes}.
        """
        return self.redo_history.setdefault(axes, [])

    def can_redo(self, axes):
        """
        Returns a boolean indicating if there are zooming actions that can be
        redone.
        """
        return not (not self._get_redo_history(axes))

    def can_unzoom(self, axes):
        """
        Returns a boolean indicating if there are unzooming actions that can be
        redone.
        """
        return len(self._get_history(axes)) > 0

    def redo(self, axes):
        """
        Rezooms the axes.
        """
        if not self.can_redo(axes): return

        x, y = self._get_redo_history(axes).pop()
        return AxesLimits.set(self, axes, x, y)

    def set(self, axes, xrange, yrange):
        """
        Override base class functionality to clear redo history.
        """
        if not self.zoomed(axes):
            for i in self._get_redo_history(axes):
                self._get_redo_history(axes).pop()
        return AxesLimits.set(self, axes, xrange, yrange)

    def restore(self, axes):
        """
        Override base class functionality to add action to redo history.
        """
        if self.zoomed(axes):
            self._get_redo_history(axes).append((axes.get_xlim()
                                               , axes.get_ylim()))

        return AxesLimits.restore(self, axes)

class PanTool:
    """
    This class is dedicated to the management of panning actions.
    """
    def __init__(self, view, enabled):
        self.view      = view
        self.enabled   = enabled
        self.isPanning = False
        self.panx      = 0
        self.pany      = 0

    def getView(self):
        return self.view

    def setEnabled(self, state):
        """
        Enable or disable panning.
        """
        self.enabled = state

    def setX(self, x):
        """
        Sets the current x position for panning.
        """
        self.x = x

    def getX(self):
        """
        Returns the current x position for panning.
        """
        return self.x

    def setY(self, y):
        """
        Sets the current y position for panning.
        """
        self.y = y

    def getY(self):
        """
        Returns the current y position for panning.
        """
        return self.y

    def pan(self, x, y, axes):
        """
        Modifies the desired axes limits to make it appear to the user that the
        axes are panning as he/she moves the mouse.
        """
        if not self.enabled: return

        if not is_log_x(axes):
            xtick = axes.get_xaxis()._get_tick(major=False)._size
            movex = (self.getX() - x) / xtick / 10
            # TBF: matplotlib's Axes' panx method is broken, so we do it here
            #      in the next two lines for them.
            axes.xaxis.pan(movex)
            axes._send_xlim_event()
            self.panx += movex
        if not is_log_y(axes):
            ytick = axes.get_yaxis()._get_tick(major=False)._size
            movey = (self.getY() - y) / ytick / 10
            axes.pany(movey)
            self.pany += movey

        self.setX(x)
        self.setY(y)

        FigureCanvasWxAgg.draw(self.getView())

    def panAll(self, x, y, axesList):
        """
        Pans across multiple subplots simultaneously.  Use this
        function rather than pan to avoid lag on the x-axis.
        """
        if not self.enabled:    return

        i=0
        movex, movey = 0, 0
        xmin, xmax = 0, 0
        for axes in axesList:
            if not is_log_x(axes):
                xtick = axes.get_xaxis()._get_tick(major=False)._size
                movex = (self.getX() - x) / xtick / 10
                # TBF: matplotlib's Axes' panx method is broken, so we do it here
                axes.xaxis.pan(movex)
                if i==0:    # we want to keep all plots on a common x-axis
                    xmin, xmax = axes.viewLim.intervalx().get_bounds()
                axes.set_xlim(xmin, xmax)
                axes._send_xlim_event()
            if not is_log_y(axes):
                ytick = axes.get_yaxis()._get_tick(major=False)._size
                movey = (self.getY() - y) / ytick / 10
                axes.pany(movey)
            i += 1

        self.panx += movex
        self.pany += movey
        self.setX(x)
        self.setY(y)

        FigureCanvasWxAgg.draw(self.getView())

    def end_pan(self, x, y, axes):
        """
        Returns the axes limits to their original settings before panning
        started.
        """
        if not self.enabled: return

        panx = self.panx
        pany = self.pany
        if not is_log_x(axes):
            # TBF: matplotlib's Axes' panx method is broken, so we do it
            #      here for them.
            axes.xaxis.pan(-self.panx)
            axes._send_xlim_event()
            self.panx = 0
        if not is_log_y(axes):
            axes.pany(-self.pany)
            self.pany = 0

        FigureCanvasWxAgg.draw(self.getView())

    def end_pan_all(self, x, y, axesList):
        """
        End panning for multiple subplots.  Use this function
        to correctly reset limits for all axes.
        """

        if not self.enabled: return
        i = 0
        xmin, xmax = 0, 0
        for axes in axesList:
            if not is_log_x(axes):
                # TBF: matplotlib's Axes' panx method is broken, so we do it
                #      here for them.
                axes.xaxis.pan(-self.panx)
                if i==0:    # we want to keep all plots on a common x-axis
                    xmin, xmax = axes.viewLim.intervalx().get_bounds()
                axes.set_xlim(xmin, xmax)
                axes._send_xlim_event()

            if not is_log_y(axes):
                axes.pany(-self.pany)
                axes._send_ylim_event()

            i += 1

        self.panx = 0
        self.pany = 0

        FigureCanvasWxAgg.draw(self.getView())

class MyPlotPanelDirector(PlotPanelDirector):
    """
    Extends the base class to include panning, subplot selection, and 
    unzoom/rezoom.
    """
    def __init__(self, view, zoom=True, selection=True, rightClickUnzoom=True):
        PlotPanelDirector.__init__(self, view, zoom, selection, rightClickUnzoom)
        self.limits = MyAxesLimits() # New & improved!

        self.infoMode       = not zoom
        self.zoomMode       = zoom
        self.panMode        = False
        self.gridMode       = False
        self.activeSubplot  = None
        self.selectedAxes   = None
        self.panTool        = PanTool(view, False)

    def getView(self):
        return self.view

    def getActiveSubplot(self):
        return self.activeSubplot

    def setActiveSubplot(self, subplot):
        self.activeSubplot = subplot
        if subplot is not None:
            self.getView().get_figure().sca(subplot)

    def leftButtonDown(self, evt, x, y):
        """
        Completely overrides base class functionality.
        """
        self.leftButtonPoint = (x, y)

        view = self.getView()

        if self.selectedAxes is None:
            axes, xdata, ydata = self.find_axes(view, x, y)
        else:
            axes = self.selectedAxes
            xdata, ydata = get_data(axes, x, y)

        self.setActiveSubplot(axes)

        self.panTool.setX(x)
        self.panTool.setY(y)

        if self.selectionEnabled and not wxmpl.is_polar(axes):
            view.cursor.setCross()
            view.crosshairs.clear()

    def find_axes(self, canvas, x, y):
        """
        Override the wxmpl.find_axes function
        """
        #return wxmpl.find_axes(canvas, x, y)
        axes = None
        for a in canvas.get_figure().get_axes():
            if a.in_axes(x, y):
                if axes is None:
                    axes = a
        if axes is None:
            return None, None, None
        xdata, ydata = axes.transData.inverse_xy_tup((x, y))
        return axes, xdata, ydata

    def find_all_axes(self, canvas, x=None, y=None):
        """
        Return a list of all axes in canvas
        """
        axeslist = []
        for a in canvas.get_figure().get_axes():
            if x is None and y is None:
                axeslist.append(a)
            elif a.in_axes(x, y):
                axeslist.append(a)
        return axeslist

    def leftButtonUp(self, evt, x, y):
        """
        Completely overrides base class functionality.
        """
        if self.leftButtonPoint is None:
            return

        view = self.getView()

        if self.selectedAxes is None:
            axes, xdata, ydata = self.find_axes(view, x, y)
        else:
            axes = self.selectedAxes
            xdata, ydata = get_data(axes, x, y)

        self.setActiveSubplot(axes)
        self.end_x         = x
        self.end_y         = y

        if self.IsInfoMode() and axes is not None:
            self.SelectAxes(axes)

        x0, y0 = self.leftButtonPoint
        self.leftButtonPoint = None
        view.rubberband.clear()

        if x0 == x:
            if y0 == y and axes is not None:
                view.notify_point(axes, x, y)
                view.crosshairs.set(x, y)
            return
        elif y0 == y:
            return

        xdata = ydata = None
        xrange, yrange = get_selected_data(axes, x0, y0, x, y)

        if axes is not None:
            xdata, ydata = axes.transData.inverse_xy_tup((x, y))
            if self.zoomEnabled:
                for ax in self.find_all_axes(view, x, y):
                    xrange, yrange = get_selected_data(ax, x0, y0, x, y)
                    if xrange is not None and yrange is not None:
                        if self.limits.set(ax, xrange, yrange):
                            FigureCanvasWxAgg.draw(view)
            else:
                self.getView().notify_selection(axes, x0, y0, x, y)

        if axes is None:
            view.cursor.setNormal()
        elif wxmpl.is_polar(axes):
            view.cursor.setNormal()
            view.location.set(wxmpl.format_coord(axes, xdata, ydata))
        else:
            view.crosshairs.set(x, y)
            view.location.set(wxmpl.format_coord(axes, xdata, ydata))

        if len(self.find_all_axes(self.view, x, y)) > 1:
            self.UpdateLocationStr(x, y)

    def SelectAxes(self, axes):
        """
        Make selected subplot the only one shown.
        """
        for a in self.getView().GetAxes():
            if a == axes:
                a.set_position([0.125, 0.1, 0.8, 0.8]) # TBF: magic numbers
                self.selectedAxes = a
            else:
                a.set_visible(False)
        FigureCanvasWxAgg.draw(self.getView())

    def rightButtonUp(self, evt, x, y):
        """
        Completely overrides base class functionality.
        """
        view = self.getView()

        if self.selectedAxes is None:
            axes, xdata, ydata = self.find_axes(view, x, y)
        else:
            axes = self.selectedAxes
            xdata, ydata = get_data(axes, x, y)

        self.setActiveSubplot(axes)

        if self.zoomEnabled and self.rightClickUnzoom:
            xmin = xmax = None
            for axes in self.find_all_axes(view, x, y): # unzoom all axes
                self.limits.restore(axes)
                if not self.limits.can_unzoom(axes):
                    # rescale manually - wxmpl will try to autoscale
                    if xmin is None or xmax is None: # make sure x-axis matches
                        xmin, xmax = axes.viewLim.intervalx().get_bounds()
                    axes.set_xlim(xmin, xmax)
                    axes._send_xlim_event()
            view.crosshairs.clear()
            view.draw()
            view.crosshairs.set(x, y)

        if self.IsInfoMode() and axes is not None:
            self.DisplayAllSubplots()
            FigureCanvasWxAgg.draw(view)

        if self.IsPanMode() and axes is not None:
            self.panTool.end_pan_all(x, y, self.find_all_axes(view, x, y))

    def UpdateLocationStr(self, x, y):
        """
        Update coordinate location for all axes
        """
        axes = self.find_all_axes(self.view, x, y)
        coordstr = ""
        i = 0
        for ax in axes:
            i += 1
            xdata, ydata = get_data(ax, x, y)
            xi = ax.format_xdata(xdata)
            yi = ax.format_ydata(ydata)
            coordstr += "\nx%s=%s,\ty%s=%s"%(i, xi, i, yi)
        self.view.location.set(coordstr[1:])

    def mouseMotion(self, evt, x, y):
        """
        Completely overrides base class functionality.
        """
        view = self.getView()

        if self.selectedAxes is None:
            axes, xdata, ydata = self.find_axes(view, x, y)
        else:
            axes = self.selectedAxes
            xdata, ydata = get_data(axes, x, y)

        if self.leftButtonPoint is not None:
            self.selectionMouseMotion(evt, x, y, axes, xdata, ydata)
        else:
            if axes is None:
                self.canvasMouseMotion(evt, x, y)
            elif wxmpl.is_polar(axes):
                self.polarAxesMouseMotion(evt, x, y, axes, xdata, ydata)
            else:
                self.axesMouseMotion(evt, x, y, axes, xdata, ydata)

        if self.IsPanMode() and self.leftButtonPoint:
            if len(self.find_all_axes(view, x, y)) > 1:
                self.panTool.panAll(x, y, self.find_all_axes(view, x, y))
            elif self.getActiveSubplot() is not None:
                self.panTool.pan(x, y, self.getActiveSubplot())

        if len(self.find_all_axes(self.view, x, y)) > 1:
            self.UpdateLocationStr(x, y)

    def AreSubplotsHidden(self):
        """
        Returns a boolean indicating if there are any subplots that are
        hidden, i.e. there is a selected subplot.
        """
        retval = True
        for a in self.getView().GetAxes():
            retval &= a.get_visible()
        return not retval
        
    def DisplayAllSubplots(self): 
        """
        Displays all subplots.  This is used to "unselect" a subplot.
        """
        for a in self.getView().GetAxes():
            if a == self.getActiveSubplot():
                a.set_position(a._originalPosition)
                self.selectedAxes = None
            a.set_visible(True)
        self.getView().draw()

    def SetInfoMode(self):
        """
        In info mode, the user can select subplots.
        """
        view = self.getView()
        view.set_zoom(False)
        view.set_selection(False)
        view.set_crosshairs(False)
        view.cursor.setEnabled(True)
        view.cursor.setNormal()
        view.cursor.setEnabled(False)

        self.panTool.setEnabled(False)

        self.infoMode = True
        self.zoomMode = False
        self.panMode  = False

    def SetZoomMode(self):
        """
        In zoom mode, the user can zoom/unzoom within one or more subplots.
        """
        view = self.getView()
        view.set_zoom(True)
        view.set_selection(True)
        view.set_crosshairs(True)
        view.cursor.setEnabled(True)
        view.cursor.setCross()

        self.panTool.setEnabled(False)

        self.zoomMode = True
        self.infoMode = False
        self.panMode  = False

    def SetPanMode(self):
        """
        In pan mode, the user can pan around one or more subplots.
        """
        view = self.getView()
        view.set_zoom(False)
        view.set_selection(False)
        view.set_crosshairs(False)
        view.cursor.setEnabled(False)
        view.cursor.cursor = wx.CURSOR_HAND
        view.SetCursor(wx.StockCursor(wx.CURSOR_HAND))

        self.panTool.setEnabled(True)

        self.infoMode = False
        self.zoomMode = False
        self.panMode  = True

    def SetGridMode(self, setting=None):
        """
        Turns the grid on or off, or toggles if no setting is given.
        """
        if setting:
            self.gridMode = setting
        else:
            self.gridMode = not self.gridMode

        axes = self.getView().GetAxes()
        for subplot in axes:
            if self.gridMode:
                subplot.yaxis.grid(True)
                subplot.xaxis.grid(True)
            else:
                subplot.yaxis.grid(False)
                subplot.xaxis.grid(False)
        if len(axes) == 2:
            for line in axes[1].yaxis.get_gridlines():
                line.set_color('gray')
        self.getView().draw()

    def IsInfoMode(self):
        """
        Returns a boolean indicating if the info tool is selected.
        """
        return self.infoMode

    def IsZoomMode(self):
        """
        Returns a boolean indicating if the zoom tool is selected.
        """
        return self.zoomMode

    def IsPanMode(self):
        """
        Returns a boolean indicating if the pan tool is selected.
        """
        return self.panMode

    def IsGridMode(self):
        """
        Returns a boolean indicating if the grid is on.
        """
        return self.gridMode

    def ZoomIn(self):
        """
        Window to rezoom functionality.
        """
        if len(self.find_all_axes(self.getView())) > 1:
            for ax in self.find_all_axes(self.getView()):
                self.limits.redo(ax)
        elif self.getActiveSubplot() is not None:
            self.limits.redo(self.getActiveSubplot())
        self.getView().draw()

    def ZoomOut(self):
        """
        Window to unzoom functionality.
        """
        if len(self.find_all_axes(self.getView())) > 1:
            for ax in self.find_all_axes(self.getView()):
                self.limits.restore(ax)
        elif self.getActiveSubplot() is not None:
            self.limits.restore(self.getActiveSubplot())
        self.getView().draw()

class PlotView(PlotPanel):
    """
    Adding functionality...
    """
    def __init__(self, parent, id, size=(6.0, 3.70), dpi=96, cursor=True, location=True, crosshairs=True, selection=True, zoom=True):
        PlotPanel.__init__(self, parent, id, size, dpi, cursor, location, crosshairs, selection, zoom)

        # New & improved!
        self.director = MyPlotPanelDirector(self, zoom, selection) 
        self.director.SetInfoMode()

        self.InitPrinter()

        # Need to set this member variable so that this figure can be used
        # in pylab functions from the command line.
        self.get_figure().num = 0

    def InitPrinter(self):
        """
        Initializes printer settings.
        """
        pData = wx.PrintData()
        pData.SetPaperId(wx.PAPER_LETTER)
        pData.SetPrinterCommand(LINUX_PRINTING_COMMAND)
        pData.SetOrientation(wx.LANDSCAPE)
        self.printer = FigurePrinter(self, pData)

    def GetPrinter(self):
        """
        Returns the printer object.
        """
        return self.printer

    def IsInfoMode(self):
        """
        Returns a boolean indicating if the info tool is selected.
        """
        return self.director.IsInfoMode()

    def IsZoomMode(self):
        """
        Returns a boolean indicating if the zoom tool is selected.
        """
        return self.director.IsZoomMode()

    def IsPanMode(self):
        """
        Returns a boolean indicating if the pan tool is selected.
        """
        return self.director.IsPanMode()

    def IsGridMode(self):
        """
        Returns a boolean indicating if the grid is on.
        """
        return self.director.IsGridMode()

    def SetInfoMode(self):
        """
        Enables the info tool.
        """
        self.director.SetInfoMode()

    def SetZoomMode(self):
        """
        Enables the zoom tool.
        """
        self.director.SetZoomMode()

    def SetPanMode(self):
        """
        Enables the pan tool.
        """
        self.director.SetPanMode()

    def SetGridMode(self):
        """
        Toggles the grid.
        """
        self.director.SetGridMode()

    def GetAxes(self):
        """
        Returns a list of all the subplots contained in the figure object.
        """
        return self.get_figure().get_axes()

    def Clear(self):
        """
        Clears the figure object and redraws.
        """
        self.get_figure().clear()
        self.draw()

    def Export(self, filename):
        """
        Saves the contents of the canvas to a file.
        """
        try:
            self.print_figure(filename)
        except IOError, e:
            if e.strerror:
                err = e.strerror
            else:
                err = e
            wx.MessageBox('Could not save file: %s' % err, 'Error - plotit',
                parent=self, style=wx.OK | wx.ICON_ERROR)

    def PrintPreview(self):
        """
        Shows the user a print preview of the canvas.
        """
        printer = self.GetPrinter()
        fig = self.get_figure()
        #printer.previewFigure(fig, "Plot")
        self.previewFigure(fig, "Plot")
        self.draw()
    
    def previewFigure(self, figure, title=None):
        """
        Replace wxmpl.FigurePrinter.previewFigure method - fails in
        version 1.2.9 because FigurePrintout is missing method HasPage
        """
        window = self.printer.view
        while not isinstance(window, wx.Frame):
            window = window.GetParent()
            assert window is not None

        fpo = MyFigurePrintout(figure, title)
        fpo4p = MyFigurePrintout(figure, title)
        preview = wx.PrintPreview(fpo, fpo4p, self.printer.pData)
        frame = wx.PreviewFrame(preview, window, 'Print Preview')
        if self.printer.pData.GetOrientation() == wx.PORTRAIT:
            frame.SetSize(wx.Size(450, 625))
        else:
            frame.SetSize(wx.Size(600, 500))
        frame.Initialize()
        frame.Show(True)

    def Print(self):
        """
        Prints the canvas.
        """
        printer = self.GetPrinter()
        fig = self.get_figure()

        # this makes a copy of the wx.PrintData instead of just saving
        # a reference to the one inside the PrintDialogData that will
        # be destroyed when the dialog is destroyed (causing segfaults)
        printData = wx.PrintData(printer.getPrintData())
        #printer.printFigure(fig, "Plot")
        self.printFigure(fig, "Plot")
        self.printer.setPrintData(printData) # reset print data
        self.draw()

    def printFigure(self, figure, title=None):
        """
        Replace wxmpl.FigurePrinter.printFigure method - fails in
        version 1.2.9 because FigurePrintout is missing method HasPage
        """
        pdData = wx.PrintDialogData()
        pdData.SetPrintData(self.printer.pData)
        printer = wx.Printer(pdData)
        fpo = MyFigurePrintout(figure, title)
        if printer.Print(self.printer.view, fpo, True):
            self.printer.pData = pdData.GetPrintData()

    def PageSetup(self):
        """
        Changes the canvas print settings.
        """
        data = wx.PrintDialogData(self.printer.getPrintData())
        printerDialog = wx.PrintDialog(self, data)
        printerDialog.GetPrintDialogData().SetSetupDialog(True)
        printerDialog.ShowModal()

        # this makes a copy of the wx.PrintData instead of just saving
        # a reference to the one inside the PrintDialogData that will
        # be destroyed when the dialog is destroyed
        printData = \
            wx.PrintData(printerDialog.GetPrintDialogData().GetPrintData())
        self.printer.setPrintData(printData)
        
        printerDialog.Destroy()
        self.draw()

    def zoomed(self, axes = None):
        """
        Override base class fuctionality to all axes to be None.  If axes is
        None, then we use the active subplot.
        """
        axes = axes or self.director.getActiveSubplot()
        if axes is not None:
            return self.director.limits.zoomed(axes)
        else:
            return False

    def AreSubplotsHidden(self):
        """
        Returns a boolean indicating if there are any subplots that are
        hidden, i.e. there is a selected subplot.
        """
        return self.director.AreSubplotsHidden()
        
    def DisplayAllSubplots(self): 
        """
        Displays all subplots.  This is used to "unselect" a subplot.
        """
        self.director.DisplayAllSubplots()

    def ZoomIn(self):
        """
        Window to rezoom functionality.
        """
        self.director.ZoomIn()

    def ZoomOut(self):
        """
        Window to unzoom functionality.
        """
        self.director.ZoomOut()

class MyFigurePrintout(FigurePrintout):
    """
    Fix for wxmpl.FigurePrinter.printFigure method - fails in
    version 1.2.9 because FigurePrintout is missing method HasPage
    """
    def HasPage(self, page):
        return page <= 1
