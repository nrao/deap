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

import sys
import wx

class Notebook(wx.Notebook):
    """
    A notebook mediates between its containing frame and any contained panels.
    """
    
    def __init__(self, parent, site, id = wx.NewId()):
        wx.Notebook.__init__(self, parent, id)
        
        # The site is the top-level frame containing this notebook.
        self.site = site

        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        
        # Handle changed/changing events to properly activate panels.
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self,  id, self.OnChanged)
        wx.EVT_NOTEBOOK_PAGE_CHANGING(self, id, self.OnChanging)

    def OnEraseBackground(self, event):
        pass                            # to avoid flicker
        
    def GetSite(self):
        "Return the top-level frame containing this notebook."
        return self.site
    
    def SetSite(self, site):
        "Define the top-level frame containing this notebook."
        self.site = site

    def AddPage(self, page, title, select = 0):
        wx.Notebook.AddPage(self, page, title, select)

        # This is a workaround for a bug in the linux port of
        # wx.Widgets.  Under Windows, AddPage will trigger an OnChanged
        # event, so this ActivatePanel() is not necessary.
        if sys.platform == "linux2" and self.GetPageCount() == 1:
            self.GetSite().ActivatePanel(page)
        
    def OnChanged(self, event):
        "Activate the newly selected page."
        
        # Notebook events are command events... but we don't want them
        # to propagate up the containement heirarchy.
        if self is not event.GetEventObject(): return

        # OTOH, we *do* want the subclass event handler to get called.
        event.Skip()

        # But what we really care about is activating any new selection.
        if event.GetSelection() >= 0:
            page = self.GetPage(event.GetSelection())
            self.GetSite().ActivatePanel(page)

    def OnChanging(self, event):
        "Deactivate the formerly selected page."
        
        # Notebook events are command events... but we don't want them
        # to propagate up the containement heirarchy.
        if self is not event.GetEventObject(): return
        
        # OTOH, we *do* want the subclass event handler to get called.
        event.Skip()
        
        # But what we really care about is deactivating any old selection.
        if event.GetOldSelection() >= 0:
            page = self.GetPage(event.GetOldSelection())
            self.GetSite().DeactivatePanel()
