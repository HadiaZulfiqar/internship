import paraview
import pandas as pd
import numpy as np
import h5py
import os
from paraview.simple import *
from paraview.vtk import *
from vtk import vtkXMLUnstructuredGridReader
import pyautogui
paraview.simple._DisableFirstRenderCameraReset()

'''
filenames       

Tape_tensile_1-STAGE1_RESULT
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
Test_8_150_all_allstages
Test7_150_outer_allstages
Test_8_150_all_last_Stage
Test7_150_outer_last_Stage


'''


def checkfname(data):
    
   
    flag = False
    while flag==False:
        try:
            flag = True
            if data.isdigit() or data.isspace():
                raise ValueError   
        except ValueError:
            data= input("Number out of range! Enter again: ")
            flag = False
    return data
        
   
def checkinp(min,max,data):
    flag = False
    while flag==False:
        try:
            flag = True
            if (int(data) >max or int(data) <min) or data.isalpha() or data.isspace():
                raise ValueError 
        except ValueError:
            data= input("Number out of range! Enter again: ")
            flag = False
    return int(data)
   
   
def erfh5(fname):
    FileName=fname+'.erfh5'
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
    csvFileName= fname+"_Coordinates.csv"
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
    mergefile= pd.read_csv(src+ fname+'.csv')
    newlist.append(mergefile)
    merged = pd.concat(newlist, axis=1)
    merged.to_csv(src+csvFileName, index=False)
    print("\n")
    Filename= [src,csvFileName]
    f.close()
    return Filename
                    
def stl(fname):
    Fname= fname+'_Coordinates.csv'
    #change the directory accordingly
    src= 'E:\\HdfViewTool\\ddf&stampforming\\'+fname+'.stl'
    Dest='E:/HdfViewTool/stlcoords/'
    
    # create a new 'STL Reader'
    stlfile = STLReader(registrationName=fname+'.stl', FileNames=[src])


    # get color transfer function/color map for 'STLSolidLabeling'
    sTLSolidLabelingLUT = GetColorTransferFunction('STLSolidLabeling')

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # save data
    SaveData(Dest+Fname, proxy=stlfile, WriteTimeSteps=0,
        Filenamesuffix='_%d',
        ChooseArraysToWrite=1,
        PointDataArrays=[],
        CellDataArrays=['STLSolidLabeling'],
        FieldDataArrays=[],
        VertexDataArrays=[],
        EdgeDataArrays=[],
        RowDataArrays=[],
        Precision=5,
        UseScientificNotation=0,
        FieldAssociation='Point Data',
        AddMetaData=1,
        AddTime=0)


    mergesrc='E:/HdfViewTool/erfh5 files/'

    coord=pd.read_csv(Dest+Fname)

    mergefile= pd.read_csv(mergesrc+fname+'.csv')

    merged = pd.concat([coord,mergefile], axis=1)
    merged.to_csv(Dest+Fname, index=False)

    coordinates=pd.read_csv(Dest+Fname)
    renamed_mergefile=coordinates.rename(columns={'Points:0':'x','Points:1':'y','Points:2':'z'})
    renamed_mergefile.to_csv(Dest+Fname, index=False)
    Filename=[Dest, Fname]
    return Filename
    

                    ###################### paraview visualization ###############################

Flag=False
while(Flag==False):
    fname= input("Enter the file you want to access: ")
    fname= checkfname(fname)
    path1='E:/HdfViewTool/erfh5 files/'+str(fname)+'.erfh5'
    path2='E:/HdfViewTool/ddf&stampforming/'+str(fname)+'.stl'
    if not (os.path.exists(path1) or os.path.exists(path2)):
        print('File does not exist. Enter again')
        Flag=False
    else:
        Flag= True
       


choice= input("Press 1 for if you have erfh5 file\nPress 2 for if you have stl file\n")
File=[]

choice= checkinp(1,2,choice)
if choice==1:
    File= erfh5(fname)
elif choice==2:
    File= stl(fname)
    

# fname=input("enter file name: ")
fname= File[1]

path= File[0]

trans_discsv = CSVReader(registrationName=fname, FileName= [path+fname])
df=pd.read_csv(path+fname)
PARAMS= df.axes[1]
NO_OF_PARAMS=len(PARAMS)-3
    

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
trans_discsvDisplay = Show(trans_discsv, spreadSheetView1, 'SpreadSheetRepresentation')
layout1 = GetLayout()

# saving layout sizes for layouts
LoadPalette(paletteName='WhiteBackground')


# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)




representation= input("Please select the representation form:\nPress 1 for Points\nPress 2 for Point Gaussian\n")
representation= checkinp(1,2,representation)

# Properties modified on trans_discsvDisplay
trans_discsvDisplay.Assembly = ''
LISTTT=[]
for i in range(0,NO_OF_PARAMS):
    for j in range(3,len(PARAMS)):
        print("Press ", j-2, " for ", PARAMS[j])
    # flag=False
    point= input("Enter parameter along which you want the visualization: ")
    point=checkinp(1,len(PARAMS)-2,point)
    # while flag==False:
    #     point= int(input("Enter parameter along which you want the visualization: "))
    #     flag=checkinput(point)

    LISTTT.append(PARAMS[point+2])
        
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # update the view to ensure updated data information
    renderView1.Update()

    # update the view to ensure updated data information
    spreadSheetView1.Update()

    # create a new 'Table To Points'
    tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=trans_discsv)
    # Properties modified on tableToPoints1
    tableToPoints1.XColumn = 'x'
    tableToPoints1.YColumn = 'y'
    tableToPoints1.ZColumn = 'z'

    # tableToPoints1Display = Show(tableToPoints1, spreadSheetView1, 'SpreadSheetRepresentation')

    # hide data in view
    Hide(trans_discsv, spreadSheetView1)
    
    # update the view to ensure updated data information
    spreadSheetView1.Update()

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
    qualityLUT = GetColorTransferFunction(fname[:-4])

    # set active view
    SetActiveView(renderView1)
    meshQuality1Display_1.PolarAxes = 'PolarAxesRepresentation'

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    meshQuality1Display_1.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.009999868, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    meshQuality1Display_1.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.009999868, 1.0, 0.5, 0.0]

    meshQuality1 = MeshQuality(registrationName='MeshQuality1', Input=tableToPoints1)

    # show data in view
    meshQuality1Display = Show(meshQuality1, spreadSheetView1, 'SpreadSheetRepresentation')
    materialLibrary1 = GetMaterialLibrary()

    # reset view to fit data
    renderView1.ResetCamera(False)
    
    #changing interaction mode based on data extents
    renderView1.InteractionMode = '3D'
    renderView1.CameraPosition = [0.5, 0.025, 10000.0]
    renderView1.CameraFocalPoint = [0.5, 0.025, 0.0]
    
    # reset view to fit data
    renderView1.ResetCamera(False)  

    # set scalar coloring
    ColorBy(meshQuality1Display_1, ('POINTS', PARAMS[point+2]))

    # rescale color and/or opacity maps used to include current data range
    meshQuality1Display_1.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    meshQuality1Display_1.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'X'
    paramLUT = GetColorTransferFunction(PARAMS[point+2])
    
    
    # Get the color transfer function
    color_transfer_function = GetColorTransferFunction(fname)

    # Set the desired number of values
    num_values = 7
    
    # Get the VTK object associated with the color transfer function
    vtk_object = color_transfer_function.GetClientSideObject()
    
    # Get the current range of the color transfer function 
    range_min_max = vtk_object.GetRange()

    range_min, range_max = range_min_max[0], range_min_max[1]

    # Calculate the step size for the extra values
    step = (range_max - range_min) / (num_values - 1)

    # Rescale the transfer function
    color_transfer_function.RescaleTransferFunction(range_min, range_max + step)

    
    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    paramLUT.ApplyPreset('Rainbow Uniform', True)

    # get opacity transfer function/opacity "map for 'X'  
    xPWF = GetOpacityTransferFunction(PARAMS[point+2])
    Flag= False
    if representation==1:
        # change representation type
        meshQuality1Display_1.SetRepresentationType('Points')
        # Properties modified on meshQuality1Display_1
        meshQuality1Display_1.PointSize = 10.0
    elif representation==2:
        # change representation type
        meshQuality1Display_1.SetRepresentationType('Point Gaussian')
        # get color transfer function/color map for 'Fiber_Angle'
        paramLUT = GetColorTransferFunction('Fiber_Angle')
        # Properties modified on meshQuality1Display
        meshQuality1Display_1.ShaderPreset = 'Sphere'    
        # Properties modified on meshQuality1Display
        meshQuality1Display_1.GaussianRadius = 0.003      
        # elif representation<1 or representation>2:
        #     print("Invalid response, try again!")
        #     representation= int(input("Please select the representation form:\nPress 1 for Points\nPress 2 for Point Gaussian\n"))
        #     Flag=False
    # renderView1.FitToAll()
    paramLUT.ApplyPreset('Rainbow Uniform', True)
    meshQuality1Display_1.RenderPointsAsSpheres = 1


    renderView1.Update() 
               
    myview = GetActiveView()
    
    # pyautogui.getWindowsWithTitle('ParaView')[0].maximize()
    layout1 = GetLayout()

    # layout/tab size in pixels
    # layout1.SetSize(10000, 2000)    
    renderView1.ViewSize = [20000, 20000]  # Adjust as needed
    renderView1.CenterAxesVisibility = False
    renderView1.OrientationAxesVisibility = False
    
    for k in range(0,3):
        num=  1.0
        
        renderView1.CameraPosition = [0.0, 0.0, 0.0]
        renderView1.CameraFocalPoint = [0.0, 0.0, 0.0]
        renderView1.CameraViewUp = [0.0, 0.0, 0.0]
        # renderView1.CameraParallelScale = 0.31552865687738218       Test6_last_Stage
        # renderView1.CameraViewAngle = 19.39676113360324
        
        
        renderView1.CameraPosition[k]=num
        renderView1.CameraViewUp[2-k]=num
        renderView1.ResetCamera(False)
        
        
        
            
        # SaveScreenshot('E:/HdfViewTool/screenshots_pv/'+fname[:-4]+PARAMS[point+2]+"view.png", viewOrLayout=renderView1,ImageResolution=[5000, 5000])
        SaveScreenshot('E:/HdfViewTool/screenshots_pv/'+fname[:-4]+PARAMS[point+2]+"-"+str(k)+"view.png", viewOrLayout=renderView1, ImageResolution=[5000, 5000],
        CompressionLevel='0')
    
    if i==NO_OF_PARAMS-1:
        SaveState('E:/HdfViewTool/pvsm_files/'+fname[:-4]+" view.pvsm")
    Interact()
    Delete(renderView1)
    del renderView1


