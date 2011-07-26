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

# Elizabeth McNany <eam74@case.edu>

import wx
from matplotlib.colors import ColorConverter

class PlotEditFrame(wx.Frame):
    """
    This class holds the frame for plot editing tools
    """

    def __init__(self, parent, plot):
        """Constructor for PlotEditFrame"""
        wx.Frame.__init__(self, parent, -1, "Edit Plot")
        self.parent = parent
        self.plot = plot
        self.figure = plot.get_figure()
        self.advanced_options = None
        self.scroll = wx.ScrolledWindow(self, -1)
        self.InitControls()
    
    def InitControls(self):
        """Create labels and controls based on the figure's attributes"""
        
        # Get current axes labels
        # NOTE: newer matplotlib (1.10) has an axes.get_xlabel() function
        plottitle = xaxislbl = y1axislbl = y2axislbl = "N/A"
        
        if len(self.figure.axes) > 0:
            plottitle = self.figure.axes[0].title.get_text()
            xaxislbl = self.figure.axes[0].xaxis.get_label().get_text()
            y1axislbl = self.figure.axes[0].yaxis.get_label().get_text()
        if len(self.figure.axes) == 2:
            y2axislbl = self.figure.axes[1].yaxis.get_label().get_text()
        
        tLbl = wx.StaticText(self, -1, "Title:")
        tTxt = wx.TextCtrl(self, -1, plottitle, size=(175,-1))
        xLbl = wx.StaticText(self, -1, "X-axis:")
        xTxt = wx.TextCtrl(self, -1, xaxislbl, size=(175,-1))
        y1Lbl = wx.StaticText(self, -1, "Y1-axis:")
        y1Txt = wx.TextCtrl(self, -1, y1axislbl, size=(175,-1))
        y2Lbl = wx.StaticText(self, -1, "Y2-axis:")
        y2Txt = wx.TextCtrl(self, -1, y2axislbl, size=(175,-1))
        
        if len(self.figure.axes) < 2:
            y2Txt.SetEditable(False)
            if len(self.figure.axes) == 0:
                tTxt.SetEditable(False)
                xTxt.SetEditable(False)
                y1Txt.SetEditable(False)
        
        self.axesCtrls = [(tLbl,tTxt), (xLbl,xTxt), (y1Lbl,y1Txt), (y2Lbl,y2Txt)]
        
        self.lineCtrls = [( wx.StaticText(self.scroll, -1, "Column:"),
                            wx.StaticText(self.scroll, -1, "Color:"),
                            wx.StaticText(self.scroll, -1, ""))]
        
        for axis in self.figure.axes:
            for line in axis.lines:
                color = self.MplToWxColour(line.get_color())
                lineTxt = wx.TextCtrl(self.scroll, -1, line.get_label(), size=(175,-1))
                lineColor = wx.TextCtrl(self.scroll, -1, "#%02x%02x%02x"%color.Get())
                lineBtn = wx.Button(self.scroll, -1, size=(25,25))
                lineBtn.SetBackgroundColour(color)
                self.Bind(wx.EVT_BUTTON, self.OnColor, lineBtn)
                self.Bind(wx.EVT_TEXT, self.OnColorChange, lineColor)
                self.lineCtrls.append((lineTxt, lineColor, lineBtn))
        
        self.advancedBtn = wx.Button(self, -1, "Advanced Options...")
        self.updateBtn = wx.Button(self, wx.ID_OK, "Update Plot")
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, "Cancel")
        
        self.Bind(wx.EVT_BUTTON, self.OnAdvanced, self.advancedBtn)
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.updateBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
        
        # Place controls
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        axesBox = wx.StaticBox(self, -1, "Axes")
        axesBoxSizer = wx.StaticBoxSizer(axesBox, wx.VERTICAL)
        axesSizer = wx.FlexGridSizer(rows=4, cols=2, vgap=3, hgap=3)
        for ctrl in self.axesCtrls:
            axesSizer.AddMany([(ctrl[0], 0, wx.ALIGN_RIGHT | wx.EXPAND),
                               (ctrl[1], 0, wx.ALIGN_LEFT | wx.EXPAND)])
        axesSizer.AddGrowableCol(1)
        axesBoxSizer.Add(axesSizer, 0, wx.EXPAND)
        
        lineBox = wx.StaticBox(self, -1, "Lines")
        lineBoxSizer = wx.StaticBoxSizer(lineBox, wx.VERTICAL)
        lineSizer = wx.FlexGridSizer(rows=len(self.lineCtrls)+1, cols=4, vgap=3, hgap=3)
        for ctrls in self.lineCtrls:
            lineSizer.AddMany([(ctrls[0], 0, wx.ALIGN_LEFT | wx.EXPAND),
                               (ctrls[1], 0, wx.ALIGN_LEFT),
                               (ctrls[2], 0, wx.ALIGN_CENTER| wx.FIXED_MINSIZE),
                               ((3,3),    0, wx.ALIGN_CENTER)])
        lineSizer.AddGrowableCol(0)
        self.scroll.SetSizer(lineSizer)
        lineBoxSizer.Add(self.scroll, 0, wx.EXPAND)
        
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        controlSizer.AddMany([(self.updateBtn, 1, wx.ALIGN_CENTER | wx.EXPAND),
                              (self.cancelBtn, 1, wx.ALIGN_CENTER | wx.EXPAND)])
        
        boxSizer.AddMany([(axesBoxSizer, 0, wx.EXPAND),
                          (lineBoxSizer, 0, wx.EXPAND),
                          (self.advancedBtn, 0, wx.EXPAND),
                          (controlSizer, 0, wx.EXPAND)])
        
        width = self.scroll.GetBestSize().width
        height = self.scroll.GetBestSize().height
        if height > 400:
            height = 400
            width = width + 25 # button size
        self.scroll.SetSize((width, height))
        self.scroll.SetScrollbars(0, 1, width, height)
        
        self.SetSizer(boxSizer)
        self.SetAutoLayout(1)
        self.Fit()
        
        height = self.GetSize().GetHeight()
        self.SetSizeHints(minH=height, maxH=height,
                                minW=width, maxW=width*5)
        

    def OnUpdate(self, event):
        """Update the plot"""
        
        # Validate data
        IsValidData = True
        for ctrl in self.lineCtrls[1:]:
            colorstr = ctrl[1].GetValue()
            if not self.IsValidColour(colorstr):
                IsValidData = False
                ctrl[1].SetBackgroundColour(wx.Colour(255,210,210))
                ctrl[1].SetFocus()
            else:
                ctrl[1].SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            ctrl[1].Refresh()
        
        if not IsValidData:
            wx.MessageBox("Please enter valid color identifiers. Colors may "
                        + "be entered as simple names ('red', 'blue', etc.) "
                        + "or as hex codes.", "Error", wx.ICON_ERROR)
            return
        
        # Update axes
        if len(self.figure.axes) > 0:
            axeslbls = [ctrl[1].GetValue() for ctrl in self.axesCtrls]
            self.figure.axes[0].set_title(axeslbls[0])
            self.figure.axes[0].set_xlabel(axeslbls[1])
            self.figure.axes[0].set_ylabel(axeslbls[2])
            if len(self.figure.axes) == 2:
                self.figure.axes[1].set_ylabel(axeslbls[3])
        
        # Update lines
        # indexing could be done more elegantly here
        k = 1
        for i in range(0, len(self.figure.axes)):
            for j in range(0, len(self.figure.axes[i].lines)):
                self.figure.axes[i].lines[j].set_label(self.lineCtrls[k][0].GetValue())
                self.figure.axes[i].lines[j].set_color(self.lineCtrls[k][1].GetValue())
                
                if self.advanced_options is not None:
                    alpha, zorder = self.advanced_options["lineCtrls"][k-1]
                    self.figure.axes[i].lines[j].set_zorder(zorder.GetValue())
                    self.figure.axes[i].lines[j].set_alpha(alpha.GetValue()/100.0)
                k += 1
            
            # Update legend
            alpha = 80
            loc = [2,1][i]
            pad = 0.1
            if self.advanced_options is not None:
                alphaCtrl, locCtrl, padCtrl = self.advanced_options["legendCtrls"][i]
                alpha = alphaCtrl.GetValue()
                pad = float(padCtrl.GetValue())
                loc = locCtrl[0].GetSelection()
                if loc < 1: # use user-entered numbers
                    loc = (float(locCtrl[1].GetValue()), float(locCtrl[2].GetValue()))
            legend = self.figure.axes[i].legend(loc=loc, pad=pad)
            legend.get_frame().set_alpha(alpha/100.0)
        
        # draw
        self.plot.draw()
        self.Close()
    
    def OnColor(self, event):
        """Launch color dialog"""
        button = event.GetEventObject()
        for i in range(0, len(self.lineCtrls)):
            if self.lineCtrls[i][2] == button:
                color = self.lineCtrls[i][1].GetValue()
                data = wx.ColourData()
                data.SetColour(self.MplToWxColour(color))
                dialog = wx.ColourDialog(self, data)
                dialog.GetColourData().SetChooseFull(True)
                if dialog.ShowModal() == wx.ID_OK:
                    data = dialog.GetColourData()
                    self.lineCtrls[i][1].SetValue("#%02x%02x%02x"%data.GetColour().Get())
                    self.lineCtrls[i][2].SetBackgroundColour(data.GetColour())
                    self.lineCtrls[i][2].ClearBackground()
                    self.lineCtrls[i][2].Refresh()
    
    def OnColorChange(self, event):
        """Validate and update button color"""
        ctrl = event.GetEventObject()
        for i in range(0, len(self.lineCtrls)):
            if self.lineCtrls[i][1] == ctrl:
                colorstr = ctrl.GetValue()
                if not self.IsValidColour(colorstr):
                    ctrl.SetBackgroundColour(wx.Colour(255,210,210))
                else:
                    ctrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                ctrl.Refresh()
                self.lineCtrls[i][2].SetBackgroundColour(self.MplToWxColour(colorstr))
                self.lineCtrls[i][2].ClearBackground()
                self.lineCtrls[i][2].Refresh()
    
    def MplToWxColour(self, color):
        """Converts matplotlib color (0-1) to wx.Colour (0-255)"""
        try:
            cc = ColorConverter()
            rgb = tuple([d*255 for d in cc.to_rgb(color)])
            return wx.Colour(*rgb)
        except ValueError: #invalid color
            return wx.Colour()
    
    def IsValidColour(self, color):
        """Checks if color is a valid matplotlib color"""
        try:
            cc = ColorConverter()
            cc.to_rgb(color)
            return True
        except ValueError: #invalid color
            return False
    
    def OnAdvanced(self, event):
        """Launch advanced options dialog"""
        dialog = wx.Dialog(self, title="Advanced Options")
        self.InitAdvancedControls(dialog)
        dialog.ShowModal()
    
    def InitAdvancedControls(self, dialog):
        """Initialize controls for advanced options dialog"""
        
        # Create legend box
        legendBox = wx.StaticBox(dialog, -1, "Legend")
        legendBoxSizer = wx.StaticBoxSizer(legendBox, wx.VERTICAL)
        legendGridSizer = wx.FlexGridSizer(rows=len(self.figure.axes)+1, cols=6, vgap=3, hgap=3)
        legendGridSizer.AddMany([(wx.StaticText(dialog, -1, ""), 0, wx.ALIGN_CENTER),
                                 (wx.StaticText(dialog, -1, "Transparency"), 0, wx.ALIGN_CENTER),
                                 (wx.StaticText(dialog, -1, "Location"), 0, wx.ALIGN_CENTER),
                                 (wx.StaticText(dialog, -1, "x"), 0, wx.ALIGN_CENTER),
                                 (wx.StaticText(dialog, -1, "y"), 0, wx.ALIGN_CENTER),
                                 (wx.StaticText(dialog, -1, "Pad"), 0, wx.ALIGN_CENTER)])
        
        loc_list = ['(select)', 'best', 'upper right', 'upper left', 'lower left',
                    'lower right', 'right', 'center left', 'center right',
                    'lower center', 'upper center', 'center']
        
        #Create controls
        lineBoxes = []
        self.advanced_options = {'legendCtrls':[], 'lineCtrls':[]}
        i = 1
        scrolls = []
        for axis in self.figure.axes:
            advscroll = wx.ScrolledWindow(dialog, -1)
            scrolls.append(advscroll)
            albl = wx.StaticText(dialog, -1, "Y%s-axis"%i)
            aalpha = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS, min=0, max=100,
                                 initial=axis.get_legend().get_frame().get_alpha()*100,
                                 size=(75,-1))
            aloc = wx.Choice(dialog, -1, choices=loc_list)
            aloc_x = wx.TextCtrl(dialog, -1, str(axis.get_legend().get_frame().get_x())[:7],
                                 size=(75,-1))
            aloc_y = wx.TextCtrl(dialog, -1, str(axis.get_legend().get_frame().get_y())[:7],
                                 size=(75,-1))
            apad = wx.TextCtrl(dialog, -1, str(axis.get_legend().pad)[:7],
                                 size=(75,-1))
            legendGridSizer.AddMany([(albl,   0, wx.ALIGN_CENTER),
                                     (aalpha, 0, wx.ALIGN_CENTER),
                                     (aloc,   0, wx.ALIGN_CENTER),
                                     (aloc_x, 0, wx.ALIGN_CENTER),
                                     (aloc_y, 0, wx.ALIGN_CENTER),
                                     (apad, 0, wx.ALIGN_CENTER),])
            self.advanced_options["legendCtrls"].append((aalpha, (aloc, aloc_x, aloc_y), apad))
            
            lineBox = wx.StaticBox(dialog, -1, "Y%s lines"%i)
            lineBoxSizer = wx.StaticBoxSizer(lineBox, wx.VERTICAL)
            lineGridSizer = wx.FlexGridSizer(rows=len(axis.lines)+1, cols=4, vgap=3, hgap=3)
            lineGridSizer.AddMany([((-1,-1), 0),
                                   (wx.StaticText(advscroll, -1, "Transparency"), 0, wx.ALIGN_CENTER),
                                   (wx.StaticText(advscroll, -1, "Order"), 0, wx.ALIGN_CENTER),
                                   ((-1,-1), 0)])
            i += 1
            for line in axis.lines:
                lbltxt = line.get_label()
                if len(lbltxt)>40:
                    lbltxt = line.get_label()[:37]+"..."
                lbl = wx.StaticText(advscroll, -1, lbltxt, style=wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE)
                alphabox = wx.SpinCtrl(advscroll, -1, style=wx.SP_ARROW_KEYS, min=0,
                                       max=100, initial=line.get_alpha()*100,
                                       size=(75,-1))
                zorderbox = wx.TextCtrl(advscroll, -1, str(line.get_zorder()), size=(30,-1))
                lineGridSizer.AddMany([(lbl, 0, wx.ALIGN_RIGHT | wx.EXPAND),
                                       (alphabox, 0, wx.ALIGN_CENTER),
                                       (zorderbox, 0, wx.ALIGN_CENTER),
                                       ((-1,-1), 0)])
                self.advanced_options["lineCtrls"].append((alphabox, zorderbox))
            
            lineGridSizer.AddGrowableCol(0)
            lineGridSizer.AddGrowableCol(3)
            advscroll.SetSizer(lineGridSizer)
            lineBoxSizer.Add(advscroll, 0, wx.EXPAND | wx.ALL)
            lineBoxes.append(lineBoxSizer)
        
        legendBoxSizer.Add(legendGridSizer, 0, wx.EXPAND | wx.ALL)
        
        updateBtn = wx.Button(dialog, wx.ID_OK, "OK")
        cancelBtn = wx.Button(dialog, wx.ID_CANCEL, "Cancel")
        dialog.Bind(wx.EVT_BUTTON, self.OnAdvancedUpdate, updateBtn)
        
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        controlSizer.AddMany([(updateBtn, 1, wx.EXPAND),
                              (cancelBtn, 1, wx.EXPAND)])
        
        # Place controls
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        boxSizer.Add(legendBoxSizer, 0, wx.EXPAND | wx.ALL)
        for linebox in lineBoxes:
            boxSizer.Add(linebox, 0, wx.EXPAND | wx.ALL)
        boxSizer.Add(controlSizer, 0, wx.EXPAND | wx.ALL)
        
        for advscroll in scrolls:
            width = advscroll.GetBestSize().width
            height = min(advscroll.GetBestSize().height, 250)
            advscroll.SetSize((width, height))
            advscroll.SetScrollbars(0, 1, width, height)
        
        dialog.SetSizer(boxSizer)
        dialog.SetAutoLayout(1)
        dialog.Fit()
    
    def OnAdvancedUpdate(self, event):
        """Validate and store advanced options for updating"""
        IsValidData = True
        for axis in self.advanced_options["legendCtrls"]:
            loc_s, loc_x, loc_y = axis[1]
            if loc_s.GetSelection() < 1:
                try:
                    float(loc_x.GetValue())
                    loc_x.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                except ValueError:
                    IsValidData = False
                    loc_x.SetBackgroundColour(wx.Colour(255,210,210))
                loc_x.Refresh()
                
                try:
                    float(loc_y.GetValue())
                    loc_y.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                except ValueError:
                    IsValidData = False
                    loc_y.SetBackgroundColour(wx.Colour(255,210,210))
                loc_y.Refresh()
            
            lpad = axis[2]
            try:
                float(lpad.GetValue())
                lpad.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            except ValueError:
                IsValidData = False
                lpad.SetBackgroundColour(wx.Colour(255,210,210))
            lpad.Refresh()
        
        for line in self.advanced_options["lineCtrls"]:
            try:
                int(line[1].GetValue())
                line[1].SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            except ValueError:
                IsValidData = False
                line[1].SetBackgroundColour(wx.Colour(255, 210, 210))
            line[1].Refresh()
        
        if IsValidData:
            dialog = event.GetEventObject().GetParent()
            dialog.Close()
        else:
            wx.MessageBox("Please enter valid numeric values for position and "
                        + "ordering.", "Error", wx.ICON_ERROR)
    
    def OnCancel(self, event):
        """Exit the editor"""
        self.plot.draw()
        self.Close()
