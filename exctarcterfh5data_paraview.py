import paraview
import pandas as pd
import numpy as np
import h5py
from paraview.simple import *
from paraview.vtk import *
from vtk import vtkXMLUnstructuredGridReader
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
# Connect(ds_host=None, ds_port=11111, rs_host=None, rs_port=11111) 

'''filenames       

Tape_tensile_1-STAGE1_RESULT.erfh5
Spotwelds-STAGE1_RESULT.erfh5
Support_Case_16_5-STAGE3_RESULT.erfh5
Support_Case_16_5-STAGE2_RESULT.erfh5
Support_Case_16_5-STAGE1_RESULT.erfh5
HEMISPHERE-1-LAYER-CASE-STAGE1_RESULT.erfh5
Thermoforming_Organosheet-STAGE1_RESULT.erfh5
DDF_ESI-STAGE1_RESULT.erfh5
Test_4-STAGE1_RESULT.erfh5
TF_Spotwelds_1-STAGE1_RESULT.erfh5
Test_150_outer-STAGE1_RESULT.erfh5
Test_170_outer-STAGE1_RESULT.erfh5
cross_beam-STAGE1_RESULT.erfh5
Test6_allstages.erfh5
Test6_last_Stage.erfh5 


'''

FileName=input("Enter the file you want to access: ")
src='E:/HdfViewTool/erfh5 files/'
fileName=src+ FileName
f = h5py.File(fileName, 'r')
a = list(f.keys())
d= list(f.values())
## for dataset inside post
post= f[a[0]]
b= list(post.keys())
# for subgrps inside post
data_a = f.get('post')
data1 = np.array(data_a)
# for subgrps inside constant
data_c= data_a.get(data1[0])
data3= np.array(data_c)
# for subgrp inside entity results
data_d=data_c.get('entityresults')
data4= np.array(data_d)
# for subgrp inside NODE
data_e= data_d.get(data4[0])
data5= np.array(data_e)
# for subgrp inside COORDINATES
data_f= data_e.get(data5[0])
data6= np.array(data_f)
# for subgrp inside Total_Stress
data_g= data_f.get(data6[0])
data7= np.array(data_g)
# for subgrp inside ZONE1_set1
data_h= data_g.get(data7[0])
data8= np.array(data_h)
# for dataset inside erfblock
data_i= data_h.get(data8[-1])
data9= np.array(data_i)
# saving data into csv file
csvFileName= FileName[:-6]+"_Coordinates.csv"
# bb=data.flatten()       
# np.savetxt(csvFileName,data9,delimiter=',')
df = pd.DataFrame(data=data9)
# Write the updated DataFrame back to the CSV file
df.to_csv(src+csvFileName, index=False)
newfile = pd.read_csv(src+csvFileName)
renamed_newfile=newfile.rename(columns={'0':'x','1':'y','2':'z'})
renamed_newfile.to_csv(src+csvFileName, index=None)

# #MERGING THE PARAMETER'S DATASET
newlist=[]
coordinates=pd.read_csv(src+csvFileName)
newlist.append(coordinates)
mergefile= pd.read_csv(src+ FileName[:-6]+'.csv')
newlist.append(mergefile)
merged = pd.concat(newlist, axis=1)
merged.to_csv(src+csvFileName, index=False)
print("\n")
f.close()


# fname=input("enter file name: ")
fname= csvFileName
# C:\\Users\\binary computers\\OneDrive\\Desktop\\HdfViewTool\\'

path= 'E:\\HdfViewTool\\erfh5 files\\'
trans_discsv = CSVReader(registrationName=fname, FileName= [path+fname])
df=pd.read_csv(path+fname)
PARAMS= df.axes[1]
NO_OF_PARAMS=len(PARAMS)-3
    
# trans_discsv = CSVReader(registrationName='trans_dis.csv', FileName=['C:\\Users\\binary computers\\OneDrive\\Desktop\\HdfViewTool\\trans_dis.csv'])


# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
trans_discsvDisplay = Show(trans_discsv, spreadSheetView1, 'SpreadSheetRepresentation')

layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts
LoadPalette(paletteName='WhiteBackground')


# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

def checkinput(point):
    if point<1 or point>5:
        print("Invalid input, try again")
        return False
    else:
        return True

# Properties modified on trans_discsvDisplay
trans_discsvDisplay.Assembly = ''
LISTTT=[]
for i in range(0,NO_OF_PARAMS):
    for j in range(3,len(PARAMS)):
        print("Press ", j-2, " for ", PARAMS[j])
    flag=False
    while flag==False:
        point= int(input("Enter parameter along which you want the visualization: "))
        flag=checkinput(point)

    LISTTT.append(PARAMS[point+2])
        
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # update the view to ensure updated data information
    renderView1.Update()

    # update the view to ensure updated data information
    spreadSheetView1.Update()

    # # resize frame
    # layout1.SetSplitFraction(0, 0.7752941176470588)

    # create a new 'Table To Points'
    tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=trans_discsv)
    # Properties modified on tableToPoints1
    tableToPoints1.XColumn = 'x'
    tableToPoints1.YColumn = 'y'
    tableToPoints1.ZColumn = 'z'

    # show data in view
    # tableToPoints1Display = Show(tableToPoints1, spreadSheetView1, 'SpreadSheetRepresentation')

    # hide data in view
    Hide(trans_discsv, spreadSheetView1)
    
    # update the view to ensure updated data information
    spreadSheetView1.Update()

    # # Properties modified on tableToPoints1Display
    # tableToPoints1Display.Assembly = ''

    # create a new 'Mesh Quality'
    meshQuality1 = MeshQuality(registrationName='MeshQuality1', Input=tableToPoints1)

    # show data in view
    meshQuality1Display = Show(meshQuality1, spreadSheetView1, 'SpreadSheetRepresentation')

    # hide data in view
    Hide(tableToPoints1, spreadSheetView1)

    # update the view to ensure updated data information
    spreadSheetView1.Update()

    # Properties modified on meshQuality1Display
    meshQuality1Display.Assembly = ''

    # set active view
    SetActiveView(renderView1)

    # set active source
    SetActiveSource(meshQuality1)

    # show data in view
    meshQuality1Display_1 = Show(meshQuality1, renderView1, 'GeometryRepresentation')

    # get color transfer function/color map for 'Quality'
    qualityLUT = GetColorTransferFunction(fname[:-5])

    # set active view
    SetActiveView(renderView1)
    meshQuality1Display_1.PolarAxes = 'PolarAxesRepresentation'

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    meshQuality1Display_1.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.009999868, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    meshQuality1Display_1.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.009999868, 1.0, 0.5, 0.0]

    # show color bar/color legend
    # meshQuality1Display_1.SetScalarBarVisibility(renderView1, True)

    #changing interaction mode based on data extents
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.1, 0.025, 10000.0]
    renderView1.CameraFocalPoint = [0.1, 0.025, 0.0]
    meshQuality1 = MeshQuality(registrationName='MeshQuality1', Input=tableToPoints1)

    # show data in view
    meshQuality1Display = Show(meshQuality1, spreadSheetView1, 'SpreadSheetRepresentation')
    materialLibrary1 = GetMaterialLibrary()

    # reset view to fit data
    renderView1.ResetCamera(False)


    # change representation type
    meshQuality1Display_1.SetRepresentationType('Points')
    
    #changing interaction mode based on data extents
    renderView1.InteractionMode = '3D'
    renderView1.CameraPosition = [0.5, 0.025, 10000.0]
    renderView1.CameraFocalPoint = [0.5, 0.025, 0.0]
    
    # reset view to fit data
    renderView1.ResetCamera(False)  

    # set scalar coloring
    ColorBy(meshQuality1Display_1, ('POINTS', PARAMS[point+2]))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    # HideScalarBarIfNotNeeded(qualityLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    meshQuality1Display_1.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    meshQuality1Display_1.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'X'
    xLUT = GetColorTransferFunction(PARAMS[point+2])
    
    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    xLUT.ApplyPreset('Rainbow Uniform', True)

    # get opacity transfer function/opacity "map for 'X'
    xPWF = GetOpacityTransferFunction(PARAMS[point+2])

    # Properties modified on meshQuality1Display_1
    meshQuality1Display_1.PointSize = 10.0
    
    renderView1.CameraPosition = [2.59066786221997015, 1.1987959725872877, 1.4018003609951137]
    renderView1.CameraFocalPoint = [0.09999999999999998, 0.02500000000000002, -1.1914346495454615e-17]
    renderView1.CameraViewUp = [-0.8087975908562638, 0.2589255588547178, -0.5280189504145433]
    renderView1.CameraParallelScale = 0.13051557376055906
    xLUT.ApplyPreset('Rainbow Uniform', True)
    meshQuality1Display_1.RenderPointsAsSpheres = 1


    renderView1.Update()
    # Set the desired size of the render view
    renderView1.ViewSize = [1000,15000]  # Width, Height 
    
    myview = GetActiveView()
        
    SaveScreenshot('E:/HdfViewTool/screenshots_pv/'+fname[:-5]+PARAMS[point+2]+"view.png", viewOrLayout=renderView1,ImageResolution=[5000, 5000])
    Interact()
    # source=GetSources()
    # SaveData("sample.vtu")
    # writer = CreateWriter("sample.vtu", myview)
    # reader = vtkXMLUnstructuredGridReader()
    # reader.SetFileName("your_data.vtu")
    # reader.Update()

    
    # Get a reference to the VTK object and save it as a .vtk file
    # vtk_object = reader.GetClientSideObject()
    # SaveData("output_file.vtk", vtk_object, FileType='Ascii')
    if i==NO_OF_PARAMS-1:
        SaveState('E:/HdfViewTool/pvsm_files/'+fname[:-5]+" view.pvsm")
        
    # myview = GetActiveView()
    # ExportView('sampleSVGGG.svg', view=myview,Plottitle='ParaView GL2PS Export',Compressoutputfile=1)

    Delete(renderView1)
    del renderView1


# find source
tableToPoints1 = FindSource('TableToPoints1')

# set active source
SetActiveSource(tableToPoints1)
