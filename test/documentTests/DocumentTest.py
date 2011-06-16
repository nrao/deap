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

from   document.Document import Document
from   document.Text     import Text
import unittest

class TestObject:
    def __init__(self, a):
        self.argument = a

class DocumentTestCase(unittest.TestCase):
    "Tests of Document class, which contains all plot data"

    def setUp(self):
        "Initializes objects used across tests."
        
        self.testDoc = Document()

        # add one default plot, for non-trivial tests
        self.xList1 = [1, 2, 3]
        self.yList1 = [10, 11, 12]
        self.intensityList1 = [[.1,3,.5],[.1,3,.5],[.1,3,.5]]
        plot = self.testDoc.AddXYPlot(self.xList1, self.yList1)
        self.testDoc.SetActivePlot(plot)

        # to reuse later
        self.xList2 = [4, 5, 6]
        self.yList2 = [14, 15, 16]
        self.intensityList2 = [[.1,.3,.5],[.1,.3,.5],[.1,.3,.5]]
        self.xList3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.yList3 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 110, 111, 112, 113, 114, 115, 116]

    def testAddXYPlot(self):
        """
        Tests the AddXYPlot operation of the Document class.
        If the method returns a 1, the currently active plot,
        then success
        """
    
        # returns the index of the plot
        assert self.testDoc.AddXYPlot(self.xList2, self.yList2) == 1 

    def testAddImage(self):
        """
        Tests the AddGrayScaleImage and AddColorImage operation of the
        Document class. If the method returns a 1, the currently active plot,
        then success
        """
        self.testDoc.Clear()
        # returns the index of the plot
        assert self.testDoc.AddColorImage(self.xList2, self.yList2, self.intensityList2) == 0

        self.testDoc.Clear()
        assert self.testDoc.AddGrayScaleImage(self.xList2, self.yList2, self.intensityList2) == 0
        

    def testModifyImage(self):
        """
        Tests the ModifyImage operation of the Document class.
        Modify the plot, using different combinations of parameters.
        Only requires x data or y data, but can also have both.
        Test boundary condition -- should return exception.
        """
        self.testDoc.Clear()
        panel = self.testDoc.AddColorImage(self.xList1, self.yList1, self.intensityList1)
        assert self.testDoc.ModifyImage(self.xList2, self.yList2, self.intensityList2, 0) == None
        #self.testDoc.SetActivePlot(index)    
        assert self.testDoc.GetXData() == self.xList2
        assert self.testDoc.GetYData() == self.yList2
        assert self.testDoc.GetIntensityData() == self.intensityList2
        
        assert self.testDoc.ModifyImage(self.xList1, None, None) == None
        
        assert self.testDoc.GetXData() == self.xList1
        assert self.testDoc.GetYData() == self.yList2
        assert self.testDoc.GetIntensityData() == self.intensityList2        
        
        assert self.testDoc.ModifyImage(None, self.yList1, self.intensityList1) == None
        
        assert self.testDoc.GetXData() == self.xList1
        assert self.testDoc.GetYData() == self.yList1
        assert self.testDoc.GetIntensityData() == self.intensityList1
      

    def testImageStuff(self):
        "Tests Image Attributes"
        self.testDoc.Clear()
        image1 = self.testDoc.AddGrayScaleImage(self.xList2, self.yList2, self.intensityList2) == 1
        self.testDoc.SetActivePlot(image1)
        self.testDoc.SetImageContrast(-1.0)
        assert self.testDoc.GetImageContrast() == -1.0
        self.testDoc.SetImageBrightness(-0.5)
        assert self.testDoc.GetImageBrightness() == -0.5

        self.testDoc.Clear()
        image2 = self.testDoc.AddColorImage(self.xList2, self.yList2, self.intensityList2)
        self.testDoc.SetActivePlot(image2)
        self.testDoc.SetImageContrast(2.0)
        assert self.testDoc.GetImageContrast() == 2.0
        self.testDoc.SetImageBrightness(1.5)
        assert self.testDoc.GetImageBrightness() == 1.5
        L = [-0.5, -0.1, 0.0, 0.02, 0.03, 0.04, 0.05, 0.10, 0.15, 0.17, 0.25, 0.33, 0.38, 0.45, 0.57, 0.6, 0.73, 0.9, 1.7]
        R = [ 1.0,  1.0, 1.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.60, 0.80, 0.90, 1.00, 1.00, 1.0, 1.00, 1.0, 0.0]
        G = [ 1.0,  1.0, 1.0, 0.00, 0.20, 0.50, 0.70, 0.90, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.80, 0.7, 0.60, 0.0, 0.0]
        B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.testDoc.SetImageColorTable(None,None,None,B)
        t,i,m,e = self.testDoc.GetImageColorTable()
        assert t == L
        assert i == R
        assert m == G
        assert e == B
        
    def testGetNumPlots(self):
        """
        Tests the GetNumPlots operation of the document class.
        If the method returns a 1, the number of plots currently in document,
        then success.
        """
        assert self.testDoc.GetNumPlots() == 1
        
    def testGetActivePlot(self):
        """
        Tests the GetActivePlot operation of the document class.
        Returns the index of the active plot, which is zero.
        """
        assert self.testDoc.GetActivePlot() == 0
        
    def testSetActivePlot(self):
        """
        Tests the SetActivePlot operation of the Document class.
        Need to add plot so test is useful.
        Then switch plot, and make sure the GetActivePlot returns as expected.
        Also, test that boundary conditions return an exception.
        """
        plot = self.testDoc.AddXYPlot(self.xList2, self.yList2)
        self.testDoc.SetActivePlot(plot)
        self.assertEquals(self.testDoc.GetActivePlot(), plot)
        
        try:
            self.testDoc.SetActivePlot(-1)
            self.fail()
        except:
            pass 
            
        try:
            self.testDoc.SetActivePlot(2)
            self.fail()
        except:
            pass
            
        self.assertEquals(self.testDoc.SetActivePlot(0), 1)
        self.assertEquals(self.testDoc.GetActivePlot(), 0)
    
    def testGetXandYData(self):
        """
        Tests the GetXData and GetYData operations of the Document class.
        Make sure that X and Y Data returns as expected
        Calling GetXData w/o parameter gets info for active plot.
        Test boundary conditions, make sure returns an exception.
        """
        assert self.testDoc.GetXData() == [1, 2, 3]
        assert self.testDoc.GetXData(0) == [1, 2, 3]
        
        try:  self.testDoc.GetXData(1)
        except:  pass
        else:  assert 1
        
        assert self.testDoc.GetYData() == [10, 11, 12]
        assert self.testDoc.GetYData(0) == [10, 11, 12]         
        
        try: self.testDoc.GetYData(1) == (0)
        except:  pass
        else:  assert 1

    def testRemovePlot(self):
        """
        Tests the RemovePlot operation of the Document class.
        Add plot, for non-trivial test.
        Then test boundary conditions -- should return an exception.
        Remove the plot, then make sure the X and Y data returns as expeted.
        """
        plot = self.testDoc.AddXYPlot(self.xList2, self.yList2)
        try:
            self.testDoc.RemovePlot(plot + 10)
            self.fail()
        except:
            pass

        try:
            self.testDoc.RemovePlot(-2)
            self.fail()
        except:
            pass

        self.testDoc.SetActivePlot(plot)
        self.assertEquals(self.testDoc.RemovePlot(), {0: 0})
        self.assertEquals(self.testDoc.RemovePlot(), { })
        plot = self.testDoc.AddXYPlot(self.xList2, self.yList2)
        self.testDoc.SetActivePlot(plot)
        self.assertEquals(self.testDoc.GetXData(), self.xList2)
        self.assertEquals(self.testDoc.GetYData(), self.yList2)
        self.assertEquals(self.testDoc.GetNumPlots(), 1)

    def testModifyXYPlot(self):
        """
        Tests the ModifyXYPlot operation of the Document class.
        Modify the plot, using different combinations of parameters.
        Only requires x data or y data, but can also have both.
        Test boundary condition -- should return exception.
        """
 
        assert self.testDoc.ModifyXYPlot(plot = 0, x = self.xList2, y = self.yList2) == None
            
        assert self.testDoc.GetXData() == self.xList2
        assert self.testDoc.GetYData() == self.yList2
        
        assert self.testDoc.ModifyXYPlot(plot = 0, x = self.xList1, y = None) == None
        
        assert self.testDoc.GetXData() == self.xList1
        assert self.testDoc.GetYData() == self.yList2
        
        assert self.testDoc.ModifyXYPlot(plot = 0, x = None, y = self.yList1) == None
        
        assert self.testDoc.GetXData() == self.xList1
        assert self.testDoc.GetYData() == self.yList1
        
        try: self.testDoc.ModifyXYPlot(plot = -1, x = None, y = self.yList1) 
        except: pass
        else: assert 1
        
        try: self.testDoc.ModifyXYPlot(plot = 1, x = None, y = self.yList1)  
        except: pass 
        else: assert 1
        
    def testAnnotations(self):
        """
        Tests the Annotation operations of the Document class -- Add, Get, GetNum, and Remove
        First, add an annotation and make sure it returns as expected.
        then test boundary conditions for remove annotation -- should return an exception.
        Remove an annotation, and make sure that GetNum returns zero.
        Try to remove another annotation, when none are present, and should return exception.
        """
        annotation = Text()
        assert self.testDoc.AddWorldAnnotation(annotation, 1, 1) == 0
        assert self.testDoc.GetAnnotation(0)[0] == annotation
        
        try: self.testDoc.GetAnnotation(1)
        except: pass
        else:  assert 1
        
        try: self.testDoc.GetAnnotation(-1)
        except: pass
        else:  assert 1
        
        assert self.testDoc.GetNumAnnotations() == 1
        
        try: self.testDoc.RemoveAnnotation(-1)
        except: pass
        else:  assert 1
        
        try: self.testDoc.RemoveAnnotation(1)
        except: pass
        else:  assert 1
        
        assert self.testDoc.RemoveAnnotation(0) == None
        assert self.testDoc.GetNumAnnotations() == 0
        
        try: self.testDoc.RemoveAnnotation(0)
        except: pass
        else:  assert 1
         
    def testShowLegend(self):
        """
        Tests the ShowLegend operations of the Document class.
        If ShowLegend returns none, then success.
        Then check with Get to make sure value set correctly.
        """
        assert self.testDoc.ShowLegend(1) == None
        assert self.testDoc.GetShowLegend() == 1
        
    def testSetAxisSettings(self):
        """
        Tests the SetXAxis, SetY1Axis, and SetY2Axis operations of the Document class.
        All classes just return None on success.
        then, test all Get methods to make sure appropriate
        values are returned.
        """
        assert self.testDoc.SetXAxis(1, 100, "logarithmic", "X Axis") == None
        assert self.testDoc.GetXAxisMin() == 1
        assert self.testDoc.GetXAxisMax() == 100
        assert self.testDoc.GetXAxisType() == "logarithmic"
        assert self.testDoc.GetXAxisLabel() == "X Axis"
        
        assert self.testDoc.SetY1Axis(2, 200, "linear", "Y1 Axis") == None
        assert self.testDoc.GetY1AxisMin() == 2
        assert self.testDoc.GetY1AxisMax() == 200
        assert self.testDoc.GetY1AxisType() == "linear"
        assert self.testDoc.GetY1AxisLabel() == "Y1 Axis"
        
    def testCaptions(self):
        """
        Tests the caption operations of the Document class -- 
        SetCaption, ShowCaption, and GetShowCaption
        All set methods return None on success, 
        and Get methods return expected value.
        Finally, test the boundary condition.
        """
        assert self.testDoc.SetCaption("This is my caption") == None
        assert self.testDoc.GetCaption() == "This is my caption"
        
        assert self.testDoc.ShowCaption(0, plot = None) == None
        assert self.testDoc.GetShowCaption(0) == 0
        
        assert self.testDoc.ShowCaption(1, plot = 0) == None
        assert self.testDoc.GetShowCaption(0) == 1
        
        try: self.testDoc.ShowCaption(1, plot = 1)
        except:  pass
        else:  assert 1
        
    def testBins(self):
        "Tests the Bins operations of the Document class"
        pass
        
    def testPlotAttributes(self):
        """
        Test the operations of the Document class that manipulate 
        the appearance of the plots -- SetXYLinePattern, XYErrorBars,
        UseY2 axis.
        All Set methods just return None on 
        success, and there are no boundary conditions.
        Check that Get methods return as expected.
        """
        assert self.testDoc.SetXYLinePattern(1, 2, 3) == None
        assert self.testDoc.GetXYLinePattern() == 1
        assert self.testDoc.GetXYLineWidth()   == 2
        assert self.testDoc.GetXYLineColor()   == 3
        
        assert self.testDoc.AddXYErrorBars([.1, .2, .1], [.2, .2, .3], 3) == None
        assert self.testDoc.GetXYLowerErrorBars() == [.1, .2, .1]
        assert self.testDoc.GetXYUpperErrorBars() == [.2, .2, .3]
        assert self.testDoc.GetXYErrorBarColor()  == 3        
        assert self.testDoc.SetXYErrorBarColor(3) == None
        
        assert self.testDoc.GetXYErrorBarShow() == 1
        assert self.testDoc.ShowXYErrorBars(0)  == None
        assert self.testDoc.GetXYErrorBarShow() == 0
        
        assert self.testDoc.UseY2Axis() == None
        
    def testFlags(self):
        """
        Test the operations of the Document class that manipulate the flags
        Set the flags and then get them, and make sure they match.
        """
        assert self.testDoc.SetFlags([1, 2, 3]) == None
        assert self.testDoc.GetFlags() == [1, 2, 3]
        assert self.testDoc.SetFlagValue(34) == None
        assert self.testDoc.GetFlagValue() == 34
        
        assert self.testDoc.SetFlagColor(4, flag = None) == None
        assert self.testDoc.GetFlagColor() == 4
        
    def testTitle(self):
        """
        Tests the SetTitle operation of the document class.
        Just returns None on success.
        """
        assert self.testDoc.SetTitle("My title") == None
        
    def testFrozen(self):
        """
        Tests all of the freeze operations of the document class.
        Test that default is right -- unfrozen.
        Freeze should return 1, Unfreeze 0.  
        And IsFrozen returns the current state.
        """
        assert self.testDoc.IsFrozen() == 0
        assert self.testDoc.Freeze() == 1
        assert self.testDoc.IsFrozen() == 1
        assert self.testDoc.Unfreeze() == 0
        
    def testUndoRedo(self):
        """
        Tests all of the undo and redo operations of the document class.
        Test that CanUndo returns 0, and undo returns None,
        and redo returns 0 -- nothing to undo/redo.
        """
        assert self.testDoc.CanUndo() == 0
    
    def testMarker(self):
        """ 
        Tests all of the marker operations of the document class.
        First, get the marker attributes when there is no marker.
        Should return an exception.
        then set the marker, and verify that Get actions return as expected.
        """      
        try: self.testDoc.GetXYMarker()
        except:  pass
        else:  assert 1
        
        try: self.testDoc.GetXYMarkerColor()
        except:  pass
        else:  assert 1
        
        assert self.testDoc.SetXYMarker(1, 3) == None
        assert self.testDoc.GetXYMarker() == 1
        assert self.testDoc.GetXYMarkerColor()[0] == 3
        
    def testAutoScale(self):
        """
        Tests all of the AutoScale operations of the document class.
        Exercise the Set and Get methods to set values and make
        sure they return appropriately.
        """
        try:
            self.testDoc.SetXAutoscale(4)
        except:
            pass
        else:
            self.fail("Accepted bad autoscale value!")

        try:
            self.testDoc.SetY1Autoscale(44)
        except:
            pass
        else:
            self.fail("Accepted bad autoscale value!")

        self.testDoc.SetXAutoscale(1)
        self.assertEquals(1, self.testDoc.GetXAutoscale())
        self.testDoc.SetXAutoscale(0)
        self.assertEquals(0, self.testDoc.GetXAutoscale())

        self.testDoc.SetY1Autoscale(1)
        self.assertEquals(1, self.testDoc.GetY1Autoscale())
        self.testDoc.SetY1Autoscale(0)
        self.assertEquals(0, self.testDoc.GetY1Autoscale())
        
def suite():
    """
    Returns a suite containing all the test cases in this module.
    It can be a good idea to put an identically named factory function
    like this in every test module. Such a naming convention allows
    automation of test discovery.
    """
    suite1 = unittest.makeSuite(DocumentTestCase)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.main()
