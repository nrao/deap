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

import copy

class Document:
    def __init__(self):
        self.frozen      = 0
        self.undo        = []
        self.redo        = []
        self.plotter     = None
        self.commandLine = None

    def SetPlotter(self, plotter):
        "Sets the PlotView object associated with the document."
        self.plotter = plotter

    def GetPlotter(self):
        "Returns the PlotView object associated with the document."
        return self.plotter

    def SetCommandLine(self, commandLine):
        "Sets the command line object associated with the document."
        self.commandLine = commandLine

    def GetCommandLine(self):
        "Returns the command line object associated with the document."
        return self.commandLine

    def CanUndo(self):
        "True iff we can reverse a previous command."
        return len(self.undo) > 0

    def Undo(self):
        "Reverse a previously applied command."
        if not self.CanUndo(): return

        undo = self.undo.pop()
        self.redo.append(undo)

        savedUndo = copy.copy(self.undo)
        savedRedo = copy.copy(self.redo)

        self.GetCommandLine().Clear()
        self.GetCommandLine().ExecuteCommands(savedUndo)

        self.undo = savedUndo
        self.redo = savedRedo

    def AddUndo(self, undo):
        "Remember a new action."
        if undo is None or \
           undo.isspace() or \
           undo == "" or \
           undo.strip(" ") in ("undo()", "redo()"):
            return

        self.redo = []
        self.undo.append(undo)

    def CanRedo(self):
        "True iff we can repeat a previous command."
        return len(self.redo) > 0

    def Redo(self):
        "Reapply a previously applied command."
        if not self.CanRedo(): return

        redo = self.redo.pop()
        self.undo.append(redo)

        savedUndo = copy.copy(self.undo)
        savedRedo = copy.copy(self.redo)

        self.GetCommandLine().ExecuteCommands(savedUndo)

        self.undo = savedUndo
        self.redo = savedRedo

    def IsFrozen(self):
        "Returns >=1 if application is frozen, 0 otherwise."
        return self.frozen

    def Freeze(self):
        """
        Use this method to tell the Document that the application is
        frozen at the command line.
        """
        self.frozen = self.frozen + 1
        return self.frozen

    def Unfreeze(self):
        """
        Use this method to tell the Document that the application has
        been unfrozen from the GUI.
        """
        self.frozen = max(0, self.frozen - 1)
        return self.frozen

    def Hold(self, state):
        "Sets the hold state of the matplotlib figure."
        if self.GetCommandLine():
            self.GetCommandLine().Hold(state)

    def Export(self, file):
        "Save the plotting canvas to a graphical file format."
        if self.GetPlotter():
            self.GetPlotter().Export(file)

    def Clear(self):
        """
        Clears the plotting canvas.
        """
        if self.GetPlotter():
            self.GetPlotter().Clear()

    def draw(self):
        """
        Generates a redraw event, which refreshes the plot.
        """
        if self.GetPlotter():
            self.GetPlotter().draw()

    def get_figure(self):
        """
        Returns the matplotlib figure object. The matplotlib figure is the
        entry point for all plotting functionality.
        """
        if self.GetPlotter():
            return self.GetPlotter().get_figure()
