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

import wx

class Panel(wx.Panel):
    """
    A panel is aware of its top-level frame, or site, so that it can
    cooperate with the frame to provide a customized user interface
    when the panel is active.  The frame notifies the panel when it
    is activated or deactivated.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        # The site is the top-level frame containing this panel.
        self.site  = None

        # But a panel can, recursively, serve as a site for other panels.
        self.panel = None

    def __getattr__(self, name):
        "Forward methods to hosting site by default."
        if self.GetSite() is not None and name[0] <> "_":
            return getattr(self.GetSite(), name)
        return None

    def GetSite(self):
        "Return the top-level frame containing this panel."
        return self.site

    def SetSite(self, site):
        "Define the top-level frame containing this panel."
        self.site = site

    def GetPanel(self):
        "Return any panel using this panel as a site."
        return self.panel

    def SetPanel(self, panel):
        "Sets the panel using this panel as a site."
        self.panel = panel

    def ActivateSite(self, site):
        """
        Override this method to customize the frame's interface (e.g.,
        menus and toolbars).
        """
        self.SetSite(site)
        if self.GetPanel() is not None:
            self.GetPanel().ActivateSite(self)
            
    def DeactivateSite(self):
        """
        Override this method as necessary to undo the effects of
        ActivateSite.
        """
        self.SetSite(None)
        if self.GetPanel() is not None:
            self.GetPanel().DeactivateSite()

    def UpdateMenus(self):
        """
        Override this method to dynamically customize menus as they
        are opened.
        """
        if self.GetPanel() is not None:
            self.GetPanel().UpdateMenus()
        
    def ActivatePanel(self, panel):
        "Make a new panel active within this site."
        self.panel = panel
        if self.GetSite() is not None:
            self.GetSite().ActivatePanel(self)
            
    def DeactivatePanel(self):
        "Remove an existing panel from active service."
        pass
