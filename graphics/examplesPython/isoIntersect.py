#!/usr/local/bin/python

from libVTKCommonPython import *
from libVTKGraphicsPython import *

#catch  load vtktcl 
# get the interactor ui
#source ../../examplesTcl/vtkInt.tcl
#source ../../examplesTcl/colors.tcl
from colors import *
# Create the RenderWindow, Renderer and both Actors
#
ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# create pipeline
#
pl3d2 = vtkPLOT3DReader()
pl3d2.SetXYZFileName("../../../vtkdata/combxyz.bin")
pl3d2.SetQFileName("../../../vtkdata/combq.bin")
pl3d2.SetScalarFunctionNumber(153)
pl3d2.Update()

pl3d = vtkPLOT3DReader()
pl3d.SetXYZFileName("../../../vtkdata/combxyz.bin")
pl3d.SetQFileName("../../../vtkdata/combq.bin")
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

iso = vtkContourFilter()
iso.SetInput(pl3d.GetOutput())
iso.SetValue(0,.24)

probe2 = vtkProbeFilter()
probe2.SetInput(iso.GetOutput())
probe2.SetSource(pl3d2.GetOutput())

cast2 = vtkCastToConcrete()
cast2.SetInput(probe2.GetOutput())

isoLines = vtkContourFilter()
isoLines.SetInput(cast2.GetOutput())
isoLines.GenerateValues(10,0,1400)

isoStrips = vtkStripper()
isoStrips.SetInput(isoLines.GetOutput())

isoTubes = vtkTubeFilter()
isoTubes.SetInput(isoStrips.GetOutput())
isoTubes.SetRadius(.1)
isoTubes.SetNumberOfSides(5)

isoLinesMapper = vtkPolyDataMapper()
isoLinesMapper.SetInput(isoTubes.GetOutput())
isoLinesMapper.ScalarVisibilityOn()
isoLinesMapper.SetScalarRange(0,1400)

isoLinesActor = vtkActor()
isoLinesActor.SetMapper(isoLinesMapper)
isoLinesActor.GetProperty().SetColor(bisque[0],bisque[1],bisque[2])

isoMapper = vtkPolyDataMapper()
isoMapper.SetInput(iso.GetOutput())
isoMapper.ScalarVisibilityOff()

isoActor = vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor(bisque[0],bisque[1],bisque[2])

outline = vtkStructuredGridOutlineFilter()
outline.SetInput(pl3d.GetOutput())
outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInput(outline.GetOutput())
outlineActor = vtkActor()
outlineActor.SetMapper(outlineMapper)

# Add the actors to the renderer, set the background and size
#
ren.AddActor(outlineActor)
ren.AddActor(isoLinesActor)
ren.AddActor(isoActor)
ren.SetBackground(1,1,1)
renWin.SetSize(640,480)
ren.SetBackground(0.1,0.2,0.4)

cam1=ren.GetActiveCamera()
cam1.SetClippingRange(3.95297,50)
cam1.SetFocalPoint(9.71821,0.458166,29.3999)
cam1.SetPosition(2.7439,-37.3196,38.7167)
cam1.ComputeViewPlaneNormal()
cam1.SetViewUp(-0.16123,0.264271,0.950876)
cam1.Dolly(1.2)
ren.ResetCameraClippingRange()

# render the image
#

renWin.Render()
#renWin SetFileName "isoIntersect.tcl.ppm"
#renWin SaveImageAsPPM

# prevent the tk window from showing up then start the event loop
#wm withdraw .


iren.Start()
