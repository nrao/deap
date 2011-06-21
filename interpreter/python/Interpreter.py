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
import os

# A list of functions available to the user from the command line.
# These are *really* methods of the Interpreter class masquerading as functions.
FUNCTIONS = [
    "clear"       # repeat of pylab function (clf)
  , "draw"        # repeat of pylab function (draw)
  , "export"      # repeat of pylab function (savefig)
  , "freeze"
  , "get_figure"  # repeat of pylab function (gcf)
  , "get_subplot" # repeat of pylab function (gca)
  , "hold"        # repeat of pylab function (hold)
  , "open_file"   # should just be execfile
  , "redo"
  , "undo"
  , "get_data"
]

class Interpreter:
    """
    The Intepreter is the mechanism whereby the user can interact with the
    graphics via the command line.
    """

    def __init__(self, document):
        "Constructor for Interpreter."
        self.document    = document
        self.commandLine = None

    def DefineFunctions(self):
        "Defines list of functions that the user calls from the command line."
        functions = { }
        for k in FUNCTIONS: functions[k] = getattr(self, k)
        return functions

    def SetCommandLine(self, commandLine):
        "Sets the command line associated with the interpreter."
        self.commandLine = commandLine
        if self.document is not None:
            self.document.SetCommandLine(commandLine)

    def GetCommandLine(self):
        "Returns the command line associated with the interpreter."
        return self.commandLine

    def SetDocument(self, document):
        "Returns the Document object associated with the interpreter."
        self.document = document
        if document is not None:
            document.SetCommandLine(self.GetCommandLine())

    def GetDocument(self):
        "Returns a reference to the Document contained in the Interpreter."
        return self.document

    #### Functions available from the command line ####

    def clear(self):
        """
        Clears the plotting canvas.
        """
        if self.document is not None:
            self.GetDocument().Clear()

    def draw(self):
        """
        Generates a redraw event, which refreshes the plot.
        """
        if self.document is not None:
            self.GetDocument().draw()

    def export(self, file):
        """
        Saves the plotting canvas to a graphical file format.  The file
        argument is a string representing the file name (and path) of the
        export file.  The file must have either a .png or .eps extension.

        Eg.
        export("plot.png") # Saves canvas to file in local directory
        """
        path, ext = os.path.splitext(file)
        ext = ext[1:].lower()

        if ext != 'png' and ext != 'eps':
            print 'Only the PNG and EPS image formats are supported.\n'
            print 'A file extension of `png\' or `eps\' must be used.'
        else:
            self.GetDocument().Export(file)

    def freeze(self, message = None):
        """
        Freezes further processing of the command line until the
        application receives an unfreeze via the GUI. The message
        argument, when supplied, is a string which is translated into
        a message dialog that is displayed to the user reminding him/her
        that a "freeze" command has been issued. If the message string 
        is not supplied, no dialog is displayed before the command line
        is frozen.

        Eg.
        freeze()             # Freezes the command line - no message dialog
        freeze("my message") # Freezes the command line & displays dialog
                             # containing the string, "my message"
        """
        if message is not None and type(message) is str:
            wx.MessageBox(message, "Freezing - Unfreeze to continue")

        count = self.GetDocument().Freeze()
        while self.GetDocument().IsFrozen() >= count:
            if wx.GetApp().Pending(): wx.GetApp().Dispatch()

    def get_subplot(self, index = None):
        """
        Returns either the indicated subplot object or a list of all subplot
        objects contained in the figure object (when the index is not 
        specified).  The index argument is an integer which represents the
        subplot number within the figure object.  Note that subplot indexing
        begins at zero.

        Eg.
        get_subplot()   # Return a list of all subplot objects
        get_subplot(0)  # Returns the first subplot object
        """
        if index is not None:
            try:
                return self.get_figure().axes[index]
            except IndexError:
                print "Error! That subplot does not exist."
        else:
            return self.get_figure().axes

    def get_figure(self):
        """
        Returns the matplotlib figure object. The matplotlib figure is the
        entry point for all plotting functionality.
        """
        return self.GetDocument().get_figure()

    def hold(self, b = None):
        """
        Set the hold state.  If hold is None (default), toggle the
        hold state.  Else set the hold state to boolean value b.
        This controls both the matplotlib figure object and the GUI window.

        Eg.
        hold()      # toggle hold
        hold(True)  # hold is on
        hold(False) # hold is off
        """ 
        self.GetDocument().Hold(b)

    def open_file(self, file):
        """
        Opens a previously saved session or user-created file containing DEAP
        commands.  file is a string containing the path to the desired file.

        Remove me - use execfile instead.
        """
        f = open(file, "r")
        history = f.readlines()
        f.close()

        # Reinitialize
        self.clear()
        self.GetCommandLine().SetHistory(history)
        self.draw()

    def redo(self):
        "Redoes the last command typed in the interactive shell."
        self.GetDocument().Redo()

    def undo(self):
        "Undoes the last command typed in the interactive shell."
        self.GetDocument().Undo()

    def get_data(self, index=None):
        """
        Returns either data for the indicated subplot or a list of all 
        data plotted on the graph.  Subplots are ordered starting with 
        Y1 columns and continuing with Y2 columns.
        
        Data for each subplot is returned in a list like:
        [[x1, x2, ..., xN], [y2, y2, ..., yN]]
        """
        j = 0
        data = []
        for axes in self.get_subplot():
            for line in axes.lines:
                data.append([line.get_xdata(), line.get_ydata()])
                j +=1
        if index:
            return data[j]
        return data
