//Maya ASCII 2024 scene
//Name: camera_template.ma
//Last modified: Thu, Sep 18, 2025 08:52:39 PM
//Codeset: 1252
requires maya "2024";
requires "stereoCamera" "10.0";
requires "mtoa" "5.3.4.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202310181224-69282f2959";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26100)";
fileInfo "UUID" "3FE54DFF-4E29-0761-B385-0E9E62FD0651";
createNode transform -n "cineCam_grp";
	rename -uid "F0C88274-48A9-BF1F-BEFD-889773643BD4";
	setAttr -l on ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "cineCam_world_grp" -p "cineCam_grp";
	rename -uid "019336B5-4365-C940-DB43-1B8E25D34926";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.11663594 0.34990779 0.50335568 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.37700048 0.62080461 0.73223627 ;
createNode transform -n "cineCam_world_ctrl" -p "cineCam_world_grp";
	rename -uid "14E379D8-4806-F482-7D56-E3BCEA172738";
	addAttr -ci true -sn "RigScale" -ln "RigScale" -nn "Rig Scale" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "RigVisibility" -ln "RigVisibility" -nn "Rig Visibility" -min 
		0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.00064097717 0.014365435 0.020134229 ;
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".rp" -type "double3" 0 -1.5777218104420236e-30 2.1316282072803006e-14 ;
	setAttr ".sp" -type "double3" 0 -1.5777218104420236e-30 2.1316282072803006e-14 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
	setAttr -k on ".RigScale";
	setAttr -k on ".RigVisibility" yes;
createNode nurbsCurve -n "cineCam_world_ctrl_shp" -p "cineCam_world_ctrl";
	rename -uid "6F34B6CD-4664-30CC-EC98-16A4B06A22DA";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		41.763892769593816 2.5573008800108178e-15 -41.763892769593816
		3.6165695875799479e-15 3.6165695875799479e-15 -59.063063572255189
		-41.763892769593816 2.5573008800108171e-15 -41.763892769593802
		-59.063063572255217 -1.2806075602992884e-31 1.2014167692194412e-15
		-41.763892769593816 -2.5573008800108182e-15 41.763892769593824
		-5.916387473111607e-15 -3.6165695875799503e-15 59.063063572255238
		41.763892769593816 -2.5573008800108178e-15 41.763892769593816
		59.063063572255217 -8.0873467981614996e-31 1.2317665540050882e-14
		41.763892769593816 2.5573008800108178e-15 -41.763892769593816
		3.6165695875799479e-15 3.6165695875799479e-15 -59.063063572255189
		-41.763892769593816 2.5573008800108171e-15 -41.763892769593802
		;
createNode transform -n "cineCam_track_grp" -p "cineCam_grp";
	rename -uid "44F2B5F0-41F0-1069-3D14-93B17D1F9906";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.11953993 0.32778531 0.25415203 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.90319705 0.43389574 0.32177135 ;
createNode transform -n "cineCam_track_ctrl" -p "cineCam_track_grp";
	rename -uid "6CD9427B-48F8-591C-0875-66BA75E35CE0";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.79910648 0.15896055 0.082281567 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "cineCam_track_ctrl_shp" -p "cineCam_track_ctrl";
	rename -uid "1DB9ADE7-4FF9-C99C-E7AC-79A68664C3A1";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-42.034095364483406 0 0
		-23.118752450465877 0 -18.495001960372697
		-23.118752450465877 0 -13.871251470279525
		-13.871251470279525 0 -13.871251470279525
		-13.871251470279525 0 -23.118752450465877
		-18.495001960372697 0 -23.118752450465877
		0 0 -42.034095364483406
		18.495001960372697 0 -23.118752450465877
		13.871251470279525 0 -23.118752450465877
		13.871251470279525 0 -13.871251470279525
		23.118752450465877 0 -13.871251470279525
		23.118752450465877 0 -18.495001960372697
		42.034095364483406 0 0
		23.118752450465877 0 18.495001960372697
		23.118752450465877 0 13.871251470279525
		13.871251470279525 0 13.871251470279525
		13.871251470279525 0 23.118752450465877
		18.495001960372697 0 23.118752450465877
		0 0 42.034095364483406
		-18.495001960372697 0 23.118752450465877
		-13.871251470279525 0 23.118752450465877
		-13.871251470279525 0 13.871251470279525
		-23.118752450465877 0 13.871251470279525
		-23.118752450465877 0 18.495001960372697
		-42.034095364483406 0 0
		;
createNode parentConstraint -n "cineCam_track_grp_parentConstraint1" -p "cineCam_track_grp";
	rename -uid "CDF8B85E-453A-21BC-B046-5C9B7915E41A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_world_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 1.5777218104420236e-30 -2.1316282072803006e-14 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "cineCam_track_grp_scaleConstraint1" -p "cineCam_track_grp";
	rename -uid "765175EE-4090-0A3C-1E5C-B389DB711DE7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_world_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "cineCam_crane_grp" -p "cineCam_grp";
	rename -uid "78767465-4D15-0493-9BA1-7881F80C3358";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.90464503 0.36131009 0.09989699 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38798997 0.66667348 0.60745037 ;
createNode transform -n "cineCam_crane_pivot" -p "cineCam_crane_grp";
	rename -uid "9FF7B99B-4E9B-527F-8807-F0B17E1216FC";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.12425626 0.40939596 0.33354276 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "cineCam_crane_pivot_shp" -p "cineCam_crane_pivot";
	rename -uid "107CA1A7-4091-CCD8-CE7C-4B8217CE7D67";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.8361162489122451 4.798237340988473e-16 -7.836116248912246
		6.7857323231109119e-16 6.7857323231109119e-16 -11.081941875543876
		-7.8361162489122451 4.798237340988472e-16 -7.8361162489122442
		-11.081941875543881 3.5177356190060269e-32 -5.7448982375248306e-16
		-7.8361162489122451 -4.798237340988472e-16 7.8361162489122451
		-1.1100856969603225e-15 -6.7857323231109169e-16 11.081941875543883
		7.8361162489122451 -4.798237340988472e-16 7.8361162489122442
		11.081941875543881 -9.2536792101100992e-32 1.511240500779959e-15
		7.8361162489122451 4.798237340988473e-16 -7.836116248912246
		6.7857323231109119e-16 6.7857323231109119e-16 -11.081941875543876
		-7.8361162489122451 4.798237340988472e-16 -7.8361162489122442
		;
createNode transform -n "cineCam_crane_top" -p "cineCam_crane_pivot";
	rename -uid "33B45BAB-4D49-2455-81BF-2EB0DEE0BE8D";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.12425626 0.40939596 0.33354276 ;
	setAttr ".t" -type "double3" 0 50 0 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" -1.0658141036401503e-14 0 4.4408920985006262e-15 ;
	setAttr ".sp" -type "double3" -1.0658141036401503e-14 0 4.4408920985006262e-15 ;
	setAttr ".mntl" -type "double3" -1 1 -1 ;
	setAttr ".mtye" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "arc_pointer_shp" -p "cineCam_crane_top";
	rename -uid "92E7DE04-4424-7441-ADE7-8982B99E3B13";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 1 0 no 3
		6 0 0 0 1 1 1
		4
		-7.0710678100585938 4.4408920985006262e-16 -7.0710678100585938
		-7.0710678100585938 -0.33333333333333282 -7.0710678100585938
		-7.0710678100585938 -0.66666666666666607 -7.0710678100585938
		-7.0710678100585938 -50 -7.0710678100585938
		;
createNode nurbsCurve -n "arc_pointer_shp3" -p "cineCam_crane_top";
	rename -uid "E0280CFD-4FA6-17AA-3DAE-A882FE6BDED5";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 1 0 no 3
		6 0 0 0 1 1 1
		4
		7.0710678100585938 -3.3306690738754696e-16 -7.0710678100585938
		7.0710678100585938 -0.3333333333333337 -7.0710678100585938
		7.0710678100585938 -0.66666666666666696 -7.0710678100585938
		7.0710678100585938 -50 -7.0710678100585938
		;
createNode nurbsCurve -n "cineCam_crane_top_shp" -p "cineCam_crane_top";
	rename -uid "EA8929A7-415E-2DB9-CB6D-779A3973D844";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.8361162489122531 6.6613381477509392e-16 -7.8361162489122478
		-6.0844186831689385e-15 4.4408920985006262e-16 -11.081941875543876
		-7.8361162489122274 -8.8817841970012523e-16 -7.8361162489122407
		-11.081941875543894 6.6613381477509392e-16 3.3306690738754696e-16
		-7.8361162489122398 -1.2212453270876722e-15 7.8361162489122407
		-5.1565894411607715e-15 -7.7715611723760958e-16 11.081941875543885
		7.8361162489122478 -3.3306690738754696e-16 7.8361162489122425
		11.081941875543873 -6.6613381477509392e-16 5.440092820663267e-15
		7.8361162489122531 6.6613381477509392e-16 -7.8361162489122478
		-6.0844186831689385e-15 4.4408920985006262e-16 -11.081941875543876
		-7.8361162489122274 -8.8817841970012523e-16 -7.8361162489122407
		;
createNode nurbsCurve -n "arc_pointer_shp4" -p "cineCam_crane_top";
	rename -uid "497FCCD8-44C5-7798-F61D-D490EA6B26A8";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 1 0 no 3
		6 0 0 0 1 1 1
		4
		-7.0710678100583779 -2.6978419498391304e-14 7.0710678100583779
		-7.0710678100583779 -0.33333333333167259 7.0710678100583779
		-7.0710678100585938 -0.66666666666666741 7.0710678100585938
		-7.0710678100585938 -50 7.0710678100585938
		;
createNode nurbsCurve -n "arc_pointer_shp2" -p "cineCam_crane_top";
	rename -uid "45C1F0A2-4A6F-8139-5F09-D7BD3A26F3E0";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		3 1 0 no 3
		6 0 0 0 1 1 1
		4
		7.0710678100557693 -3.3706371027619753e-13 7.0710678100558972
		7.0710678100557693 -0.33333333333281923 7.0710678100558972
		7.0710678100585938 -0.66666666666666696 7.0710678100585938
		7.0710678100585938 -50 7.0710678100585938
		;
createNode parentConstraint -n "cineCam_crane_grp_parentConstraint1" -p "cineCam_crane_grp";
	rename -uid "F1FC8567-412B-9DB2-BF57-1D885F5F73AB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_track_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "cineCam_crane_grp_scaleConstraint1" -p "cineCam_crane_grp";
	rename -uid "AF436C44-4D91-BE7E-D45A-20942B0C2040";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_world_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "cineCam_rotation_grp" -p "cineCam_grp";
	rename -uid "BFD1D147-48DB-B47B-AFA3-7A9E9F23A742";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.81484652 0.55200464 0.14413089 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".rp" -type "double3" 0 0 -9.5006224575402758 ;
	setAttr ".sp" -type "double3" 0 0 -9.5006224575402758 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.91123086 0.76355791 0.41502637 ;
createNode transform -n "cineCam_rotation_ctrl" -p "cineCam_rotation_grp";
	rename -uid "1EF2DCBC-40CF-B5D2-6466-23AEE83E48B4";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.81484652 0.55200464 0.14413089 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 1 0 ;
	setAttr ".sp" -type "double3" 0 1 0 ;
	setAttr ".opm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1.7763568394002505e-15 1;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "cineCam_rotation_ctrl_shp" -p "cineCam_rotation_ctrl";
	rename -uid "EA5A658A-4683-4487-82C9-58A4A555DACC";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 40 0 no 3
		41 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40
		41
		-20.4469918107932 1 5
		-19.827385998344923 -1.0452406779207379 1.2823651253103274
		-18.588174373448364 -2.9828371096351205 -2.4352697493793451
		-16.522821665287434 -5.0280777875558584 -5.7398340824368326
		-16.522821665287434 -2.9828371096351205 -5.7398340824368326
		-16.522821665287434 -1.0452406779207379 -5.7398340824368326
		-14.044398415494321 -1.0452406779207379 -8.6313278738621353
		-10.946369353252926 -1.0452406779207379 -10.903215852839157
		-7.4352697493793451 -1.0452406779207379 -12.762033290183993
		-3.9241701455057658 -1.0452406779207379 -13.794709644264458
		0 -1.0452406779207379 -14.001244915080552
		3.9241701455057658 -1.0452406779207379 -13.794709644264458
		7.4352697493793451 -1.0452406779207379 -12.762033290183993
		10.946369353252926 -1.0452406779207379 -10.903215852839157
		14.044398415494321 -1.0452406779207379 -8.6313278738621353
		16.522821665287434 -1.0452406779207379 -5.7398340824368326
		16.522821665287434 -2.9828371096351205 -5.7398340824368326
		16.522821665287434 -5.0280777875558584 -5.7398340824368326
		18.588174373448364 -2.9828371096351205 -2.4352697493793451
		19.827385998344923 -1.0452406779207379 1.2823651253103274
		20.4469918107932 1 5
		19.827385998344923 3.0452406779207308 1.2823651253103274
		18.588174373448364 4.9828371096351134 -2.4352697493793451
		16.522821665287434 7.0280777875558584 -5.7398340824368326
		16.522821665287434 4.9828371096351134 -5.7398340824368326
		16.522821665287434 3.0452406779207308 -5.7398340824368326
		14.044398415494321 3.0452406779207308 -8.6313278738621353
		10.946369353252926 3.0452406779207308 -10.903215852839157
		7.4352697493793451 3.0452406779207308 -12.762033290183993
		3.9241701455057658 3.0452406779207308 -13.794709644264458
		0 3.0452406779207308 -14.001244915080552
		-3.9241701455057658 3.0452406779207308 -13.794709644264458
		-7.4352697493793451 3.0452406779207308 -12.762033290183993
		-10.946369353252926 3.0452406779207308 -10.903215852839157
		-14.044398415494321 3.0452406779207308 -8.6313278738621353
		-16.522821665287434 3.0452406779207308 -5.7398340824368326
		-16.522821665287434 4.9828371096351134 -5.7398340824368326
		-16.522821665287434 7.0280777875558584 -5.7398340824368326
		-18.588174373448364 4.9828371096351134 -2.4352697493793451
		-19.827385998344923 3.0452406779207308 1.2823651253103274
		-20.4469918107932 1 5
		;
createNode parentConstraint -n "cineCam_rotation_grp_parentConstraint1" -p "cineCam_rotation_grp";
	rename -uid "CE71FD8B-4CA0-5081-5145-DC92E75F7A78";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineRig_crane_topW0" -dv 1 -min 0 
		-at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 1.0658141036401503e-14 -1 -9.5006224575402811 ;
	setAttr ".rst" -type "double3" 0 0 -1.7763568394002505e-15 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "cineCam_rotation_grp_scaleConstraint1" -p "cineCam_rotation_grp";
	rename -uid "47C69404-4955-6865-6F52-8A8DB5153C8B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_world_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "cineCam_crane_arm_grp" -p "cineCam_grp";
	rename -uid "2D5B1C96-4A97-3273-3181-B4BDDBC93C2D";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.26225138 0.4507786 0.14126594 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.95552289 0.62990862 0.38123336 ;
createNode transform -n "cineCam_crane_arm_ctrl" -p "cineCam_crane_arm_grp";
	rename -uid "CCAE4CA9-42C8-B859-554A-1997739C744B";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.90464503 0.36131009 0.11953994 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s" -type "double3" 1 1 50 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr ".rp" -type "double3" 0 1 0 ;
	setAttr ".sp" -type "double3" 0 1 0 ;
	setAttr ".mnsl" -type "double3" -1 -1 1 ;
	setAttr ".msze" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "cineCam_crane_arm_ctrl_shp" -p "cineCam_crane_arm_ctrl";
	rename -uid "1ACD66FF-470E-E00D-C010-1DA0D2DEA3C5";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		10 1 0
		-10 1 0
		-10 1 1
		10 1 1
		10 1 0
		;
createNode parentConstraint -n "cineCam_crane_arm_grp_parentConstraint1" -p "cineCam_crane_arm_grp";
	rename -uid "A912987A-4C45-CF23-6C2C-55BF1A19E831";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "camRig_rotation_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 -1 0 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "cineCam_crane_arm_grp_scaleConstraint1" -p "cineCam_crane_arm_grp";
	rename -uid "537F13BA-4084-4BFF-168E-5AA1527A0E43";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_world_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "camCam_freehand_grp" -p "cineCam_grp";
	rename -uid "DAD540FD-4FFC-32B1-0730-DDA5C7953A3E";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.7083903 0.072272107 0.051269874 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".rp" -type "double3" 0 1.0000000000000036 0.99999999999999289 ;
	setAttr ".sp" -type "double3" 0 1.0000000000000036 0.99999999999999289 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38495269 0.66144204 0.77504981 ;
createNode transform -n "cineCam_freehand_ctrl" -p "camCam_freehand_grp";
	rename -uid "D25C34AA-4840-395F-82CC-598F69DFAC61";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.060200009 0.1806 0.25979999 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 0 0.99999999999999289 ;
	setAttr ".sp" -type "double3" 0 0 0.99999999999999289 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "cineCam_freehand_ctrl_shp" -p "cineCam_freehand_ctrl";
	rename -uid "DCE521A0-48F2-BB06-CA93-C0B261C8F9A8";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-15 0 0.99999999999999289
		-8.25 6.5999999999999996 0.99999999999999289
		-8.25 4.9500000000000002 0.99999999999999289
		-4.9500000000000002 4.9500000000000002 0.99999999999999289
		-4.9500000000000002 8.25 0.99999999999999289
		-6.5999999999999996 8.25 0.99999999999999289
		0 15 0.99999999999999289
		6.5999999999999996 8.25 0.99999999999999289
		4.9500000000000002 8.25 0.99999999999999289
		4.9500000000000002 4.9500000000000002 0.99999999999999289
		8.25 4.9500000000000002 0.99999999999999289
		8.25 6.5999999999999996 0.99999999999999289
		15 0 0.99999999999999289
		8.25 -6.5999999999999996 0.99999999999999289
		8.25 -4.9500000000000002 0.99999999999999289
		4.9500000000000002 -4.9500000000000002 0.99999999999999289
		4.9500000000000002 -8.25 0.99999999999999289
		6.5999999999999996 -8.25 0.99999999999999289
		0 -15 0.99999999999999289
		-6.5999999999999996 -8.25 0.99999999999999289
		-4.9500000000000002 -8.25 0.99999999999999289
		-4.9500000000000002 -4.9500000000000002 0.99999999999999289
		-8.25 -4.9500000000000002 0.99999999999999289
		-8.25 -6.5999999999999996 0.99999999999999289
		-15 0 0.99999999999999289
		;
createNode parentConstraint -n "camRig_freehand_ctrl_GRP_parentConstraint1" -p "camCam_freehand_grp";
	rename -uid "856721E3-4FFE-20A8-0CD1-CB97EE7DE1C7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_crane_arm_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 3.5527136788005009e-15 1 ;
	setAttr ".rst" -type "double3" 0 0 7.1054273576010019e-15 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode orientConstraint -n "camRig_freehand_ctrl_GRP_orientConstraint1" -p "camCam_freehand_grp";
	rename -uid "262D427E-46DD-202C-A3C5-2AB4AB01170E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "camRig_rotation_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "camRig_freehand_ctrl_GRP_scaleConstraint1" -p "camCam_freehand_grp";
	rename -uid "A842C8FA-45B0-5097-5F7D-EBB35065DBAC";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_world_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "cineCam_shake_grp" -p "cineCam_grp";
	rename -uid "D85FC772-4A0F-8F23-0A63-76AA5F44D041";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.080458045 0.26507977 0.37583894 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.48149121 0.55898899 0.60356277 ;
createNode transform -n "cineCam_shake_ctrl" -p "cineCam_shake_grp";
	rename -uid "BE3786C1-4C8A-5253-731A-E285CF4C20FE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.19991963 0.2777279 0.32885906 ;
	setAttr ".t" -type "double3" 0 0 7.1054273576010019e-15 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".opm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 1;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
createNode nurbsCurve -n "cineCam_shake_ctrl_shp" -p "cineCam_shake_ctrl";
	rename -uid "6FAE4006-4449-258F-0218-789B573795B6";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 36 0 no 3
		37 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36
		37
		0 6 0
		1.3200000000000001 5.8200000000000003 0
		2.5800000000000001 5.4000000000000004 0
		3.7199999999999998 4.6799999999999997 0
		4.6799999999999997 3.7199999999999998 0
		5.4000000000000004 2.5800000000000001 0
		5.8200000000000003 1.3200000000000001 0
		6 0 0
		6 0 0
		6.7200000000000006 0 0
		6 0 0
		5.8200000000000003 -1.3200000000000001 0
		5.4000000000000004 -2.5800000000000001 0
		4.6799999999999997 -3.7199999999999998 0
		3.7199999999999998 -4.6799999999999997 0
		2.5800000000000001 -5.4000000000000004 0
		1.3200000000000001 -5.8200000000000003 0
		0 -6 0
		0 -6.7200000000000006 0
		0 -6 0
		-1.3200000000000001 -5.8200000000000003 0
		-2.5800000000000001 -5.4000000000000004 0
		-3.7199999999999998 -4.6799999999999997 0
		-4.6799999999999997 -3.7199999999999998 0
		-5.4000000000000004 -2.5800000000000001 0
		-5.8200000000000003 -1.3200000000000001 0
		-6 0 0
		-6.8399999999999999 0 0
		-6 0 0
		-5.8200000000000003 1.3200000000000001 0
		-5.4000000000000004 2.5800000000000001 0
		-4.6799999999999997 3.7199999999999998 0
		-3.7199999999999998 4.6799999999999997 0
		-2.5800000000000001 5.4000000000000004 0
		-1.3200000000000001 5.8200000000000003 0
		0 6 0
		0 6.8399999999999999 0
		;
createNode parentConstraint -n "cineCam_shake_grp_parentConstraint1" -p "cineCam_shake_grp";
	rename -uid "A498BEC9-4615-2380-F1BC-8383547004C7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_freehand_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 0 -1 ;
	setAttr -k on ".w0";
createNode transform -n "cineCam_focus_grp" -p "cineCam_grp";
	rename -uid "001A886E-4B3E-33B6-EBD2-1C87710232F8";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.80536914 0.13226025 0.36772084 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.90640384 0.39914337 0.63495839 ;
createNode transform -n "cineCam_focusplane_ctrl" -p "cineCam_focus_grp";
	rename -uid "65C838EC-47B4-5902-FAAC-7C926D943251";
	addAttr -ci true -sn "FocalPlaneOpacity" -ln "FocalPlaneOpacity" -nn "Opacity" 
		-dv 5 -min 0 -max 10 -at "long";
	setAttr -k off ".v";
	setAttr ".t" -type "double3" 0 0 10 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr ".rp" -type "double3" -1.347111479062089e-15 1.2212453270876722e-14 1 ;
	setAttr ".sp" -type "double3" -1.347111479062089e-15 1.2212453270876722e-14 1 ;
	setAttr ".mntl" -type "double3" 0 0 1 ;
	setAttr ".mxtl" -type "double3" 0 0 1 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".mtze" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".mnrl" -type "double3" 0 0 0 ;
	setAttr ".mxrl" -type "double3" 0 0 0 ;
	setAttr ".mrxe" yes;
	setAttr ".mrye" yes;
	setAttr ".mrze" yes;
	setAttr ".xrxe" yes;
	setAttr ".xrye" yes;
	setAttr ".xrze" yes;
	setAttr -cb on ".FocalPlaneOpacity";
createNode mesh -n "cineCam_focusplane_ctrlShape" -p "cineCam_focusplane_ctrl";
	rename -uid "04A638EF-4ED9-C329-E448-C29521708125";
	setAttr -k off ".v";
	setAttr ".mb" no;
	setAttr ".csh" no;
	setAttr ".rcsh" no;
	setAttr ".vis" no;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".smo" no;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "cineCam_FocusPlane_loc" -p "cineCam_focus_grp";
	rename -uid "24D5150D-4FF4-AB16-933E-92A6A0A6EADA";
	setAttr -l on -k off ".v" no;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode locator -n "cineCam_FocusPlane_locShape" -p "cineCam_FocusPlane_loc";
	rename -uid "C9F1BF73-485D-90F6-AD2C-9190474B50D2";
	setAttr -k off ".v" no;
	setAttr ".lodv" no;
createNode parentConstraint -n "cineCam_FocusPlane_loc_parentConstraint1" -p "cineCam_FocusPlane_loc";
	rename -uid "886A6754-4078-38C6-EED6-95987CDD69C0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "pPlane1W0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" -1.347111479062089e-15 1.2212453270876722e-14 11 ;
	setAttr -k on ".w0";
createNode parentConstraint -n "cineCam_focus_grp_parentConstraint1" -p "cineCam_focus_grp";
	rename -uid "B8D916DF-4FA6-15AD-7A78-5BB197A43D76";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineRig_cameraW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" -7.6571373978539531e-16 0 1.0000000000000071 ;
	setAttr ".tg[0].tor" -type "double3" 0 179.99999999999994 0 ;
	setAttr ".lr" -type "double3" 0 6.229989375805466e-14 0 ;
	setAttr ".rsrr" -type "double3" 0 360 0 ;
	setAttr -k on ".w0";
createNode transform -n "cineCam_aim_grp" -p "cineCam_grp";
	rename -uid "6C970237-43C7-AA9E-E73D-229F71237091";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.87199998 0.87199998 0.41029999 ;
	setAttr ".t" -type "double3" 0 49 49 ;
	setAttr ".r" -type "double3" 0 360 0 ;
	setAttr ".rp" -type "double3" 0 65 60 ;
	setAttr ".sp" -type "double3" 0 65 60 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.93971139 0.93971139 0.66734141 ;
createNode transform -n "cineCam_aim_ctrl" -p "cineCam_aim_grp";
	rename -uid "8DFB2E9C-4A11-987C-A41B-1FAE7177FA0C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.87199998 0.87199998 0.41029999 ;
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 3.1554436208840472e-30 0 11 ;
	setAttr ".sp" -type "double3" 3.1554436208840472e-30 0 11 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 1 0.39041173 ;
createNode nurbsCurve -n "cineCam_aim_ctrl_shp" -p "cineCam_aim_ctrl";
	rename -uid "9E1E6BF0-4CF6-7EB3-151F-30BAB02CB57D";
	setAttr -k off ".v";
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-6.1232339957367663e-16 -5 11
		-1.9000000000000006 -4.6500000000000341 11
		-3.5500000000000003 -3.5499999999999545 11
		-4.6500000000000004 -1.8999999999999773 11
		-5 0 11
		-4.6500000000000004 1.8999999999999773 11
		-3.5499999999999994 3.5499999999999545 11
		-1.8999999999999995 4.6500000000000341 11
		6.1232339957367663e-16 5 11
		0 0 11
		-6.1232339957367663e-16 -5 11
		1.8999999999999995 -4.6500000000000341 11
		3.5499999999999994 -3.5499999999999545 11
		4.6500000000000004 -1.8999999999999773 11
		5 0 11
		0 0 11
		-5 0 11
		-4.6500000000000004 1.8999999999999773 11
		-3.5499999999999994 3.5499999999999545 11
		-1.8999999999999995 4.6500000000000341 11
		6.1232339957367663e-16 5 11
		1.9000000000000006 4.6500000000000341 11
		3.5500000000000003 3.5499999999999545 11
		4.6500000000000004 1.8999999999999773 11
		5 0 11
		;
createNode transform -n "cineCam_aim" -p "cineCam_aim_ctrl";
	rename -uid "CA0527D9-44BB-5FB3-0E50-B29411F78ED3";
	setAttr ".s" -type "double3" 0.1 0.1 0.1 ;
	setAttr ".rp" -type "double3" 5.0487097934144758e-30 5.6843418860808018e-15 11.000000000000012 ;
	setAttr ".sp" -type "double3" 5.0487097934144756e-29 5.6843418860808015e-14 110.00000000000006 ;
	setAttr ".spt" -type "double3" -4.5438388140730281e-29 -5.1159076974727215e-14 -99.000000000000057 ;
createNode locator -n "cineCam_aimShape" -p "cineCam_aim";
	rename -uid "B2A0CAA7-4C6B-AB25-64A8-7C98C7AF6ADC";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 0 110 ;
createNode transform -n "cineCam_camera_grp" -p "cineCam_grp";
	rename -uid "EAB7C3E7-4E36-C8FC-6B1C-2AAC04C9967C";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.49790001 0.87199998 0.41029999 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 0.21003135714285293 0 ;
	setAttr ".sp" -type "double3" 0 0.21003135714285293 0 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.72862244 0.93971139 0.66734141 ;
createNode parentConstraint -n "cineCam_camera_GRP_parentConstraint1" -p "cineCam_camera_grp";
	rename -uid "C3D109EF-46DF-7431-D8D1-C3A02A7AC268";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineCam_shake_ctrlW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 0.21003135714285293 -7.1054273576010019e-15 ;
	setAttr ".rst" -type "double3" 0 0 1 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "cineCam_camshape_grp" -p "cineCam_camera_grp";
	rename -uid "5F74E987-474F-18D1-F6E5-1E8A8632BB36";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "cineCam" -p "cineCam_camshape_grp";
	rename -uid "1A433CD6-4CAC-E557-B9AA-9E97A4E5A1E0";
	addAttr -ci true -sn "body" -ln "body" -nn "-------------------------" -min 0 -max 
		0 -en "BODY" -at "enum";
	addAttr -ci true -sn "visibility_vis" -ln "visibility_vis" -nn "Visibility" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "Camera_Scale" -ln "Camera_Scale" -nn "Scale" -dv 1 -min 1 
		-max 100 -at "double";
	addAttr -ci true -sn "camerashake" -ln "camerashake" -nn "Shake" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "CameraAIm" -ln "CameraAIm" -nn "AIm" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "Sensor" -ln "Sensor" -nn "-------------------------" -min 
		0 -max 0 -en "SENSOR" -at "enum";
	addAttr -ci true -sn "ShutterAngle" -ln "ShutterAngle" -nn "Shutter Angle" -dv 144 
		-at "long";
	addAttr -ci true -sn "NearClipPlane" -ln "NearClipPlane" -nn "Near Clip Plane" -dv 
		1 -min 0.1 -at "long";
	addAttr -ci true -sn "FarClipPlane" -ln "FarClipPlane" -nn "Far Clip Plane" -dv 
		10000 -at "long";
	addAttr -ci true -sn "Lens" -ln "Lens" -nn "-------------------------" -min 0 -max 
		0 -en "LENS" -at "enum";
	addAttr -ci true -sn "DepthofField" -ln "DepthofField" -nn "Depth of Field" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "FocusPlane" -ln "FocusPlane" -nn "Focus Plane" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "FocalLength" -ln "FocalLength" -nn "Focal Length" -dv 35 -min 
		1 -at "double";
	addAttr -ci true -sn "FStop" -ln "FStop" -nn "F-Stop" -dv 3.6 -min 0 -at "double";
	addAttr -ci true -sn "Focus_Region_Scale" -ln "Focus_Region_Scale" -nn "Focus Region Scale" 
		-at "double";
	addAttr -ci true -sn "Guides" -ln "Guides" -nn "-------------------------" -min 
		0 -max 0 -en "GUIDES" -at "enum";
	addAttr -ci true -sn "Letterbox_vis" -ln "Letterbox_vis" -nn "Letterbox" -min 0 
		-max 3 -en "Off:2.39:1.90:4x3" -at "enum";
	addAttr -ci true -sn "Letterbox_Opacity" -ln "Letterbox_Opacity" -nn "Letterbox Opacity" 
		-dv 10 -min 0 -max 10 -at "long";
	addAttr -ci true -sn "Grid_vis" -ln "Grid_vis" -nn "Grids" -min 0 -max 2 -en "Off:3x3:2x2" 
		-at "enum";
	addAttr -ci true -sn "DisplayFilmGate" -ln "DisplayFilmGate" -nn "Film Gate" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "DisplayResolution" -ln "DisplayResolution" -nn "Resolution" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "DisplayGateMask" -ln "DisplayGateMask" -nn "Gate Mask" -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "GateMaskOpacity" -ln "GateMaskOpacity" -nn "Gate Mask Opacity" 
		-dv 1 -min 0 -max 1 -at "double";
	addAttr -ci true -sn "DisplayFieldChart" -ln "DisplayFieldChart" -nn "Field Chart" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "DisplaySafeAction" -ln "DisplaySafeAction" -nn "Safe Action" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "DisplaySafeTitle" -ln "DisplaySafeTitle" -nn "Safe Title" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "DisplayFilmPivot" -ln "DisplayFilmPivot" -nn "Film Pivot" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "DisplayFilmOrigin" -ln "DisplayFilmOrigin" -nn "Film Origin" 
		-min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.13885719 0.44295302 0.21034236 ;
	setAttr ".t" -type "double3" -7.1810511287741049e-30 0 7.1054273576010019e-15 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 0 1.4210854715202004e-14 ;
	setAttr ".sp" -type "double3" 0 0 1.4210854715202004e-14 ;
	setAttr ".opm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 7.1054273576010019e-15 1;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.73001599 0.73001599 0.73001599 ;
	setAttr -l on -cb on ".body";
	setAttr -cb on ".visibility_vis" yes;
	setAttr -k on ".Camera_Scale" 8;
	setAttr -cb on ".camerashake";
	setAttr -cb on ".CameraAIm";
	setAttr -l on -cb on ".Sensor";
	setAttr -k on ".ShutterAngle";
	setAttr -k on ".NearClipPlane";
	setAttr -k on ".FarClipPlane";
	setAttr -l on -cb on ".Lens";
	setAttr -cb on ".DepthofField";
	setAttr -cb on ".FocusPlane";
	setAttr -k on ".FocalLength";
	setAttr -k on ".FStop" 5.6;
	setAttr -k on ".Focus_Region_Scale" 1;
	setAttr -l on -cb on ".Guides";
	setAttr -cb on ".Letterbox_vis";
	setAttr -k on ".Letterbox_Opacity";
	setAttr -cb on ".Grid_vis";
	setAttr -cb on ".DisplayFilmGate";
	setAttr -cb on ".DisplayResolution";
	setAttr -cb on ".DisplayGateMask";
	setAttr -k on ".GateMaskOpacity";
	setAttr -cb on ".DisplayFieldChart";
	setAttr -cb on ".DisplaySafeAction";
	setAttr -cb on ".DisplaySafeTitle";
	setAttr -cb on ".DisplayFilmPivot";
	setAttr -cb on ".DisplayFilmOrigin";
createNode camera -n "cineCam_cam" -p "cineCam";
	rename -uid "0C70CEC5-425D-0EC1-B3F3-96A76E530554";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".cap" -type "double2" 1.41732 0.94488 ;
	setAttr ".ff" 0;
	setAttr ".zom" 1.4275390738401683;
	setAttr ".ncp" 1;
	setAttr ".fd" 10;
	setAttr -l on ".coi";
	setAttr -l on ".ow" 30;
	setAttr ".imn" -type "string" "camera1";
	setAttr ".den" -type "string" "camera1_depth";
	setAttr ".man" -type "string" "camera1_mask";
	setAttr ".tp" -type "double3" 0 31.999999999999996 2.4868995751603507e-14 ;
	setAttr -av ".dfg" no;
	setAttr ".dgc" -type "float3" 0.019354839 0.019354839 0.019354839 ;
	setAttr -av ".dcf";
	setAttr ".oclr" -type "float3" 1 1 1 ;
	setAttr ".ai_translator" -type "string" "perspective";
createNode aimConstraint -n "cineCam_camshape_grp_aimConstraint1" -p "cineCam_camshape_grp";
	rename -uid "074BF189-45AF-F091-5133-DA936F6AA146";
	addAttr -dcb 0 -ci true -sn "w0" -ln "camRig_aimW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".o" -type "double3" 0 270.00000000000006 0 ;
	setAttr ".rsrr" -type "double3" 0 180.00000000000011 0 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode transform -n "cineCam_guides_grp" -p "cineCam_grp";
	rename -uid "1FD8ADBE-4834-42F2-0AF5-2DBA66257133";
	setAttr ".rp" -type "double3" 0 49 50.000000000000007 ;
	setAttr ".sp" -type "double3" 0 49 50.000000000000007 ;
	setAttr ".hio" yes;
createNode transform -n "cineCam_guides_loc_grp" -p "cineCam_guides_grp";
	rename -uid "F18CCCA2-4813-054D-E465-7D8D88E3795F";
	setAttr ".rp" -type "double3" 0 49 50 ;
	setAttr ".sp" -type "double3" 0 49 50 ;
	setAttr ".hio" yes;
createNode transform -n "cineCam_guides_scale_grp" -p "cineCam_guides_loc_grp";
	rename -uid "109B093C-4144-6FDF-C48A-67AC9F976913";
	setAttr ".rp" -type "double3" 0 49 49.999999999999993 ;
	setAttr ".sp" -type "double3" 0 36542.913442270379 49.999999999999993 ;
	setAttr ".spt" -type "double3" 0 -36493.913442270379 0 ;
	setAttr ".hio" yes;
createNode transform -n "cineCam_grids_grp" -p "cineCam_guides_scale_grp";
	rename -uid "9CEFF548-45F5-B9C7-99F3-449C228175BC";
	setAttr ".t" -type "double3" 1.2246467991473562e-14 0 0 ;
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999978 1 ;
	setAttr ".hio" yes;
createNode transform -n "cineCam_viewguide_2x2" -p "cineCam_grids_grp";
	rename -uid "227BC1A2-4D7B-EB4B-4F96-7087499AA8F0";
	setAttr ".tmp" yes;
	setAttr ".wfcc" -type "float3" 0.49664429 0.49664429 0.49664429 ;
	setAttr ".uoc" 2;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 36542.913442270365 49.999999999999993 ;
	setAttr ".sp" -type "double3" 0 36542.913442270372 49.999999999999993 ;
	setAttr ".spt" -type "double3" 0 -7.2759576141834243e-12 0 ;
	setAttr ".hio" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.72778755 0.72778755 0.72778755 ;
createNode mesh -n "cineCam_viewguide_2xShape2" -p "cineCam_viewguide_2x2";
	rename -uid "22D0E6A5-47F8-C286-889C-798E0C8DC8CD";
	setAttr -k off ".v";
	setAttr ".wfcc" -type "float3" 0.49664429 0.49664429 0.49664429 ;
	setAttr ".uoc" 2;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.75 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".lev" 0;
	setAttr ".dsc" yes;
	setAttr ".pt[7]" -type "float3"  0 0 -2.9802322e-08;
	setAttr ".dsm" 1;
	setAttr ".hio" yes;
createNode transform -n "cineCam_viewguide_3x3" -p "cineCam_grids_grp";
	rename -uid "D554A220-4F87-64F5-1399-7BA83BC491DD";
	setAttr ".tmp" yes;
	setAttr ".wfcc" -type "float3" 0.53691274 0.53691274 0.53691274 ;
	setAttr ".uoc" 2;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 36542.913442270365 49.999999999999993 ;
	setAttr ".sp" -type "double3" 0 36542.913442270372 49.999999999999993 ;
	setAttr ".spt" -type "double3" 0 -7.2759576141834243e-12 0 ;
	setAttr ".hio" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.75400859 0.75400859 0.75400859 ;
createNode mesh -n "cineCam_viewguide_3xShape3" -p "cineCam_viewguide_3x3";
	rename -uid "9D400601-4F4D-F1EA-989E-3EAA078D66D9";
	setAttr -k off ".v";
	setAttr ".wfcc" -type "float3" 0.53691274 0.53691274 0.53691274 ;
	setAttr ".uoc" 2;
	setAttr ".ove" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".lev" 0;
	setAttr ".dsc" yes;
	setAttr ".bck" 1;
	setAttr ".dsm" 1;
	setAttr ".difs" yes;
	setAttr ".hio" yes;
createNode transform -n "cineCam_letterbox_grp" -p "cineCam_guides_scale_grp";
	rename -uid "0E102370-4697-F8D8-BA06-38ABC30DEF6B";
	setAttr ".t" -type "double3" 1.2246467991473562e-14 0 0 ;
	setAttr ".s" -type "double3" 0.99999999999999978 0.99999999999999978 1 ;
	setAttr ".hio" yes;
createNode transform -n "cineCam_letterbox_4x3" -p "cineCam_letterbox_grp";
	rename -uid "81EACAA3-47DF-6769-F00E-6DA9813F31D9";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 36542.913442270372 50 ;
	setAttr ".sp" -type "double3" 0 36542.913442270379 50 ;
	setAttr ".spt" -type "double3" 0 -7.2759576141834243e-12 0 ;
	setAttr ".hio" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.62736166 0.62736166 0.62736166 ;
createNode mesh -n "cineCam_letterbox_4xShape3" -p "cineCam_letterbox_4x3";
	rename -uid "BA5D43F8-439D-F315-5538-A28D314CCB46";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".hio" yes;
createNode transform -n "cineCam_letterbox_2_39" -p "cineCam_letterbox_grp";
	rename -uid "4F541030-49F7-560E-6D8A-3CB5ED9C7E4A";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 36542.913442270372 50 ;
	setAttr ".sp" -type "double3" 0 36542.913442270379 50 ;
	setAttr ".spt" -type "double3" 0 -7.2759576141834243e-12 0 ;
	setAttr ".hio" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.62736166 0.62736166 0.62736166 ;
createNode mesh -n "cineCam_letterbox_2_Shape39" -p "cineCam_letterbox_2_39";
	rename -uid "969B84CB-427C-EC1A-ECEF-73B248A13438";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".hfm" 0;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".hio" yes;
createNode transform -n "cineCam_letterbox_1_90" -p "cineCam_letterbox_grp";
	rename -uid "79F5B12D-4537-BCA4-083E-F2BD6E429B6B";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999989 1 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp" -type "double3" 0 36542.913442270372 50 ;
	setAttr ".sp" -type "double3" 0 36542.913442270379 50 ;
	setAttr ".spt" -type "double3" 0 -7.2759576141834243e-12 0 ;
	setAttr ".hio" yes;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.62736166 0.62736166 0.62736166 ;
createNode mesh -n "cineCam_letterbox_1_Shape90" -p "cineCam_letterbox_1_90";
	rename -uid "5C819980-4D01-4444-19A4-2B9EA238F590";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.49999998509883881 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".hio" yes;
createNode parentConstraint -n "cineCam_guides_grp_parentConstraint1" -p "cineCam_guides_grp";
	rename -uid "2FD8ECA8-4E72-BDDB-7814-72BD5DCD1671";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "cineRig_cameraW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 7.6571373978385023e-19 -7.1054273576010019e-15 
		-0.00099999999999766942 ;
	setAttr ".tg[0].tor" -type "double3" 0 179.99999999999994 0 ;
	setAttr ".lr" -type "double3" 0 6.229989375805466e-14 0 ;
	setAttr ".rst" -type "double3" -2.4488199242883704e-31 -7.1054273576010019e-15 0.00099999999999766942 ;
	setAttr ".rsrr" -type "double3" 0 360 0 ;
	setAttr ".hio" yes;
	setAttr -k on ".w0";
createNode decomposeMatrix -n "decomposeMatrix2";
	rename -uid "AC2C3AD8-4EAE-4452-8EAC-ABB2BA284C86";
createNode multMatrix -n "multMatrix10";
	rename -uid "BFEC810D-4B75-D220-2BFF-01B90065D200";
	setAttr -s 2 ".i";
createNode expression -n "expression1";
	rename -uid "E86C4B34-4A8D-9C2B-4695-A783C394839C";
	setAttr -k on ".nds";
	setAttr ".ixp" -type "string" ".O[0] = .I[0] / 10";
createNode expression -n "expression2";
	rename -uid "09637E1B-4FB2-F665-090F-DF97653F5DD6";
	setAttr -k on ".nds";
	setAttr ".ixp" -type "string" ".O[0] = .I[0] / 10";
createNode transformGeometry -n "transformGeometry6";
	rename -uid "4ED65442-44CC-2B12-FEBC-AB9DD17B1EE4";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.347111479062089e-15 1.2212453270876722e-14 1 1;
createNode transformGeometry -n "transformGeometry5";
	rename -uid "D086FF08-4C88-7AA4-DE8D-46902FB3A0AE";
	setAttr ".txf" -type "matrix" 0.0060000000000000001 0 0 0 0 0.0060000000000000001 0 0
		 0 0 0.0060000000000000001 0 0 0 0 1;
createNode transformGeometry -n "transformGeometry4";
	rename -uid "34E42EFE-4094-CA3A-D6A3-C7B760740738";
	setAttr ".txf" -type "matrix" -1 0 -1.224646799147353e-16 0 -1.2246467991473535e-16 1.1102230246251563e-15 1 0
		 1.3558546808486143e-31 1 -1.1102230246251563e-15 0 0 0 0 1;
createNode polyPlane -n "polyPlane1";
	rename -uid "741ACA05-4648-5D06-7BAB-1CA167F5CE00";
	setAttr ".w" 1920;
	setAttr ".h" 1080;
	setAttr ".sw" 1;
	setAttr ".sh" 1;
	setAttr ".cuv" 2;
createNode unitConversion -n "unitConversion2";
	rename -uid "5E012143-4347-E73D-5CBF-7A85B37A3C8A";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "multiplyDivide2";
	rename -uid "69C4300A-4C96-FA13-0509-B391DF5FA624";
	setAttr ".op" 2;
createNode multiplyDivide -n "multiplyDivide1";
	rename -uid "175000C9-4275-00A0-E371-6AABF93C7143";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 3.1500001 1 1 ;
createNode animCurveUU -n "cineCam_viewguide_2x2_visibility";
	rename -uid "5879A54C-4D9D-A08F-F833-F78CB2489120";
	setAttr ".tan" 18;
	setAttr -s 3 ".ktv[0:2]"  0 0 1 0 2 1;
createNode transformGeometry -n "transformGeometry19";
	rename -uid "A35A3CC1-44A3-4C9E-C977-23840BE658C8";
	setAttr ".txf" -type "matrix" 80.217790208289031 0 0 0 0 0 0.58192020799143662 0
		 0 -45.12250699216257 0 0 0 36542.913442270372 49.999999999999993 1;
createNode polyPlane -n "polyPlane6";
	rename -uid "BF28AC2C-4A40-DD9E-1C26-5A842236CBF6";
	setAttr ".sw" 2;
	setAttr ".sh" 2;
	setAttr ".cuv" 2;
createNode animCurveUU -n "cineCam_viewguide_3x3_visibility";
	rename -uid "5D8483E7-41CF-1DF7-A579-EA9F9CBE7B57";
	setAttr ".tan" 18;
	setAttr -s 3 ".ktv[0:2]"  0 0 1 1 2 0;
createNode transformGeometry -n "transformGeometry20";
	rename -uid "86AFBECC-4A66-4536-C5D6-FFA9825A6806";
	setAttr ".txf" -type "matrix" 80.217790208289031 0 0 0 0 0 0.58192020799143662 0
		 0 -45.12250699216257 0 0 0 36542.913442270372 49.999999999999993 1;
createNode polyPlane -n "polyPlane5";
	rename -uid "F84BE465-4AF7-29A5-2E86-BF8802D2FAD2";
	setAttr ".sw" 3;
	setAttr ".sh" 3;
	setAttr ".cuv" 2;
createNode animCurveUU -n "cineCam_letterbox_4x3_visibility";
	rename -uid "16CFD71F-4861-1F62-333B-729A7E06CBC9";
	setAttr ".tan" 18;
	setAttr -s 3 ".ktv[0:2]"  0 0 2 0 3 1;
createNode groupId -n "groupId1";
	rename -uid "4B610E51-4943-891A-23D8-FC8466E0AE51";
	setAttr ".ihi" 0;
createNode groupId -n "groupId3";
	rename -uid "5061D059-4792-EE8B-C5DF-C2A3D364E679";
	setAttr ".ihi" 0;
createNode deleteComponent -n "deleteComponent7";
	rename -uid "2FC79697-4F8F-3268-9C16-17A36782B626";
	setAttr ".dc" -type "componentList" 1 "f[1]";
createNode transformGeometry -n "transformGeometry16";
	rename -uid "27EBB561-455C-240A-2230-F3946D0B7A03";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 50 1;
createNode transformGeometry -n "transformGeometry13";
	rename -uid "3D8D982F-4C36-31CA-9D3A-1A82304BD15F";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 -50.104000000000006 1;
createNode transformGeometry -n "transformGeometry10";
	rename -uid "E18C0471-4332-C62B-C202-1CAB46F592FC";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 36493.913442270379 0.1039999999999992 1;
createNode transformGeometry -n "transformGeometry7";
	rename -uid "251AE886-4AD1-5695-4BE4-2AB5F7FD2A76";
	setAttr ".txf" -type "matrix" 80.000001148538189 0 0 0 0 0 45 0 0 -45 0 0 0 49 50.000000000000007 1;
createNode deleteComponent -n "deleteComponent5";
	rename -uid "3592C5DE-41D7-79FC-9180-259B0C9C6CAE";
	setAttr ".dc" -type "componentList" 5 "e[5]" "e[7]" "e[9]" "e[11]" "e[13]";
createNode groupParts -n "groupParts2";
	rename -uid "C1837129-4915-6306-4A63-92A0EAC36A22";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 2 "f[0]" "f[7]";
createNode groupParts -n "groupParts1";
	rename -uid "F0341991-4568-3589-445C-6CB954BE0878";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[1:6]";
	setAttr ".irc" -type "componentList" 2 "f[0]" "f[7]";
createNode polyPlane -n "polyPlane2";
	rename -uid "94DF3601-409C-29BB-38EA-D88E2449F347";
	setAttr ".sw" 8;
	setAttr ".sh" 1;
	setAttr ".cuv" 2;
createNode groupId -n "groupId2";
	rename -uid "B11D9CBC-43D6-A035-A8E8-379B2A692C04";
	setAttr ".ihi" 0;
createNode animCurveUU -n "cineCam_letterbox_2_39_visibility";
	rename -uid "1DBABDD4-4CF7-1BC0-35BA-DC9E0D04A15C";
	setAttr ".tan" 18;
	setAttr -s 4 ".ktv[0:3]"  0 0 1 1 2 0 3 0;
createNode groupId -n "groupId4";
	rename -uid "11CA8819-4780-BB43-6C19-81A0E90D88D0";
	setAttr ".ihi" 0;
createNode groupId -n "groupId6";
	rename -uid "52AAFA16-4C82-D47F-2DA8-189A5000C61F";
	setAttr ".ihi" 0;
createNode deleteComponent -n "deleteComponent8";
	rename -uid "3075900E-49CA-5D3A-E2AB-BA9E24CF6847";
	setAttr ".dc" -type "componentList" 1 "f[1]";
createNode transformGeometry -n "transformGeometry17";
	rename -uid "B0A56949-44DB-E525-7D46-28B579298557";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 50 1;
createNode transformGeometry -n "transformGeometry14";
	rename -uid "F8779076-4F9E-F4A2-C29C-D69E00BDE7B9";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 -50.104000000000006 1;
createNode transformGeometry -n "transformGeometry11";
	rename -uid "28C413D5-4EC2-F5EF-17CA-1BA639649031";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 36493.913442270379 0.1039999999999992 1;
createNode transformGeometry -n "transformGeometry8";
	rename -uid "E18EB9AB-494F-72FD-5C17-839A20FA3751";
	setAttr ".txf" -type "matrix" 80 0 0 0 0 0 45 0 0 -45 0 0 0 49 50.000000000000007 1;
createNode polyTweak -n "polyTweak1";
	rename -uid "A8C990F4-4C37-8460-81F1-64AD8D148D00";
	setAttr ".uopa" yes;
	setAttr -s 6 ".tk";
	setAttr ".tk[0]" -type "float3" 0 0 5.5879354e-09 ;
	setAttr ".tk[1]" -type "float3" 0 0 5.5879354e-09 ;
	setAttr ".tk[2]" -type "float3" 0 0 -0.0034821033 ;
	setAttr ".tk[3]" -type "float3" 0 0 -0.0034821033 ;
	setAttr ".tk[14]" -type "float3" 0 0 0.0035658455 ;
	setAttr ".tk[15]" -type "float3" 0 0 0.0035658455 ;
createNode deleteComponent -n "deleteComponent4";
	rename -uid "6D0F197F-47A4-73B9-EADE-94B80EB051C3";
	setAttr ".dc" -type "componentList" 2 "e[12]" "e[15]";
createNode deleteComponent -n "deleteComponent3";
	rename -uid "FFE1B66B-49B0-7374-A097-38B2B8E059DD";
	setAttr ".dc" -type "componentList" 1 "e[10]";
createNode deleteComponent -n "deleteComponent2";
	rename -uid "5DCBAC2F-4219-ED3D-94F3-3697F5E43124";
	setAttr ".dc" -type "componentList" 1 "e[8]";
createNode deleteComponent -n "deleteComponent1";
	rename -uid "1AE24642-4714-F6B6-6DDD-0684EBC21F69";
	setAttr ".dc" -type "componentList" 1 "e[6]";
createNode groupParts -n "groupParts4";
	rename -uid "ACF10721-43CE-6D52-B531-75A5A5B95FD4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 2 "f[0]" "f[7]";
createNode groupParts -n "groupParts3";
	rename -uid "09F30A7F-4DBE-DC98-24A7-D9B0BA89DAA8";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[1:6]";
	setAttr ".irc" -type "componentList" 2 "f[0]" "f[7]";
createNode polyPlane -n "polyPlane3";
	rename -uid "6F6FD0A7-4D17-1DA7-31CA-A5881665095C";
	setAttr ".sw" 1;
	setAttr ".sh" 8;
	setAttr ".cuv" 2;
createNode groupId -n "groupId5";
	rename -uid "C64027C5-450C-AEAC-C994-C883DE660913";
	setAttr ".ihi" 0;
createNode animCurveUU -n "cineCam_letterbox_1_90_visibility";
	rename -uid "E9522448-4B96-EAE9-0DCA-E38558727C93";
	setAttr ".tan" 18;
	setAttr -s 4 ".ktv[0:3]"  0 0 1 0 2 1 3 0;
createNode groupId -n "groupId7";
	rename -uid "B6B7B15C-4645-43E3-1777-0C8976F76CC3";
	setAttr ".ihi" 0;
createNode groupId -n "groupId9";
	rename -uid "0F89EEEA-425B-6C4C-0015-B29FCCAE5643";
	setAttr ".ihi" 0;
createNode deleteComponent -n "deleteComponent9";
	rename -uid "47C10BFC-41E0-CAC7-798C-6296D816CBCE";
	setAttr ".dc" -type "componentList" 1 "f[1]";
createNode transformGeometry -n "transformGeometry18";
	rename -uid "9D24C4F5-44AA-0F65-3DC5-6982A8FC7DBB";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 50 1;
createNode transformGeometry -n "transformGeometry15";
	rename -uid "F6FE8746-453E-3723-1D65-A89EE66499E9";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 -50.104000000000006 1;
createNode transformGeometry -n "transformGeometry12";
	rename -uid "83479B3D-4079-3C59-9D97-4A80619B5178";
	setAttr ".txf" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 36493.913442270379 0.1039999999999992 1;
createNode transformGeometry -n "transformGeometry9";
	rename -uid "58671DBF-46E3-2AB9-7098-07A753A86E9F";
	setAttr ".txf" -type "matrix" 80 0 0 0 0 0 45 0 0 -45 0 0 0 49 50.000000000000007 1;
createNode deleteComponent -n "deleteComponent6";
	rename -uid "018353A5-4BDF-F284-4338-2095216D9CD4";
	setAttr ".dc" -type "componentList" 28 "e[6]" "e[9]" "e[12]" "e[15]" "e[18]" "e[21]" "e[24]" "e[27]" "e[30]" "e[33]" "e[36]" "e[39]" "e[42]" "e[45]" "e[48]" "e[51]" "e[54]" "e[57]" "e[60]" "e[63]" "e[66]" "e[69]" "e[72]" "e[75]" "e[78]" "e[81]" "e[84]" "e[87]";
createNode groupParts -n "groupParts6";
	rename -uid "0C9D2011-457F-436E-C090-5995CF27DD3B";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 2 "f[0]" "f[30]";
createNode groupParts -n "groupParts5";
	rename -uid "E66ABBA9-44C3-03C7-1DFF-9FA93B1487D7";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[1:29]";
	setAttr ".irc" -type "componentList" 2 "f[0]" "f[30]";
createNode polyPlane -n "polyPlane4";
	rename -uid "D94E1FDE-4434-6200-7909-26AAA9ABEF7A";
	setAttr ".sw" 1;
	setAttr ".sh" 31;
	setAttr ".cuv" 2;
createNode groupId -n "groupId8";
	rename -uid "A870BCD6-46FF-5853-5082-059A61C2B7E5";
	setAttr ".ihi" 0;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".dli" 1;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -s 5 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 8 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 3 ".u";
select -ne :defaultRenderingList1;
select -ne :standardSurface1;
	setAttr ".b" 0.80000001192092896;
	setAttr ".bc" -type "float3" 1 1 1 ;
	setAttr ".s" 0.20000000298023224;
	setAttr ".sr" 0.40000000596046448;
select -ne :initialShadingGroup;
	setAttr -s 3 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 3 ".gn";
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".outf" 51;
	setAttr ".imfkey" -type "string" "exr";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".w" 1920;
	setAttr ".h" 1080;
	setAttr ".pa" 1;
	setAttr ".dar" 1.7769999504089355;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "C:/Program Files/OCIO/OpenColorIO-Configs-1.2/aces_1.2/config.ocio";
	setAttr ".vtn" -type "string" "sRGB (ACES)";
	setAttr ".vn" -type "string" "sRGB";
	setAttr ".dn" -type "string" "ACES";
	setAttr ".wsn" -type "string" "ACES - ACEScg";
	setAttr ".ovt" no;
	setAttr ".povt" no;
	setAttr ".otn" -type "string" "sRGB (ACES)";
	setAttr ".potn" -type "string" "sRGB (ACES)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "cineCam_world_ctrl.RigScale" "cineCam_world_ctrl.sx" -l on;
connectAttr "cineCam_world_ctrl.RigScale" "cineCam_world_ctrl.sy" -l on;
connectAttr "cineCam_world_ctrl.RigScale" "cineCam_world_ctrl.sz" -l on;
connectAttr "cineCam_track_grp_parentConstraint1.ctx" "cineCam_track_grp.tx" -l on
		;
connectAttr "cineCam_track_grp_parentConstraint1.cty" "cineCam_track_grp.ty" -l on
		;
connectAttr "cineCam_track_grp_parentConstraint1.ctz" "cineCam_track_grp.tz" -l on
		;
connectAttr "cineCam_track_grp_parentConstraint1.crx" "cineCam_track_grp.rx" -l on
		;
connectAttr "cineCam_track_grp_parentConstraint1.cry" "cineCam_track_grp.ry" -l on
		;
connectAttr "cineCam_track_grp_parentConstraint1.crz" "cineCam_track_grp.rz" -l on
		;
connectAttr "cineCam_track_grp_scaleConstraint1.csx" "cineCam_track_grp.sx" -l on
		;
connectAttr "cineCam_track_grp_scaleConstraint1.csy" "cineCam_track_grp.sy" -l on
		;
connectAttr "cineCam_track_grp_scaleConstraint1.csz" "cineCam_track_grp.sz" -l on
		;
connectAttr "cineCam_world_ctrl.RigVisibility" "cineCam_track_grp.v";
connectAttr "cineCam_track_grp.ro" "cineCam_track_grp_parentConstraint1.cro";
connectAttr "cineCam_track_grp.pim" "cineCam_track_grp_parentConstraint1.cpim";
connectAttr "cineCam_track_grp.rp" "cineCam_track_grp_parentConstraint1.crp";
connectAttr "cineCam_track_grp.rpt" "cineCam_track_grp_parentConstraint1.crt";
connectAttr "cineCam_world_ctrl.t" "cineCam_track_grp_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_world_ctrl.rp" "cineCam_track_grp_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_world_ctrl.rpt" "cineCam_track_grp_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_world_ctrl.r" "cineCam_track_grp_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_world_ctrl.ro" "cineCam_track_grp_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_world_ctrl.s" "cineCam_track_grp_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_world_ctrl.pm" "cineCam_track_grp_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_track_grp_parentConstraint1.w0" "cineCam_track_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_track_grp.pim" "cineCam_track_grp_scaleConstraint1.cpim";
connectAttr "cineCam_world_ctrl.s" "cineCam_track_grp_scaleConstraint1.tg[0].ts"
		;
connectAttr "cineCam_world_ctrl.pm" "cineCam_track_grp_scaleConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_track_grp_scaleConstraint1.w0" "cineCam_track_grp_scaleConstraint1.tg[0].tw"
		;
connectAttr "cineCam_crane_grp_parentConstraint1.ctx" "cineCam_crane_grp.tx" -l on
		;
connectAttr "cineCam_crane_grp_parentConstraint1.cty" "cineCam_crane_grp.ty" -l on
		;
connectAttr "cineCam_crane_grp_parentConstraint1.ctz" "cineCam_crane_grp.tz" -l on
		;
connectAttr "cineCam_crane_grp_parentConstraint1.crx" "cineCam_crane_grp.rx" -l on
		;
connectAttr "cineCam_crane_grp_parentConstraint1.cry" "cineCam_crane_grp.ry" -l on
		;
connectAttr "cineCam_crane_grp_parentConstraint1.crz" "cineCam_crane_grp.rz" -l on
		;
connectAttr "cineCam_crane_grp_scaleConstraint1.csx" "cineCam_crane_grp.sx" -l on
		;
connectAttr "cineCam_crane_grp_scaleConstraint1.csy" "cineCam_crane_grp.sy" -l on
		;
connectAttr "cineCam_crane_grp_scaleConstraint1.csz" "cineCam_crane_grp.sz" -l on
		;
connectAttr "cineCam_world_ctrl.RigVisibility" "cineCam_crane_grp.v";
connectAttr "decomposeMatrix2.oty" "arc_pointer_shp.cp[3].yv";
connectAttr "decomposeMatrix2.oty" "arc_pointer_shp3.cp[3].yv";
connectAttr "decomposeMatrix2.oty" "arc_pointer_shp4.cp[3].yv";
connectAttr "decomposeMatrix2.oty" "arc_pointer_shp2.cp[3].yv";
connectAttr "cineCam_crane_grp.ro" "cineCam_crane_grp_parentConstraint1.cro";
connectAttr "cineCam_crane_grp.pim" "cineCam_crane_grp_parentConstraint1.cpim";
connectAttr "cineCam_crane_grp.rp" "cineCam_crane_grp_parentConstraint1.crp";
connectAttr "cineCam_crane_grp.rpt" "cineCam_crane_grp_parentConstraint1.crt";
connectAttr "cineCam_track_ctrl.t" "cineCam_crane_grp_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_track_ctrl.rp" "cineCam_crane_grp_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_track_ctrl.rpt" "cineCam_crane_grp_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_track_ctrl.r" "cineCam_crane_grp_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_track_ctrl.ro" "cineCam_crane_grp_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_track_ctrl.s" "cineCam_crane_grp_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_track_ctrl.pm" "cineCam_crane_grp_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_crane_grp_parentConstraint1.w0" "cineCam_crane_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_crane_grp.pim" "cineCam_crane_grp_scaleConstraint1.cpim";
connectAttr "cineCam_world_ctrl.s" "cineCam_crane_grp_scaleConstraint1.tg[0].ts"
		;
connectAttr "cineCam_world_ctrl.pm" "cineCam_crane_grp_scaleConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_crane_grp_scaleConstraint1.w0" "cineCam_crane_grp_scaleConstraint1.tg[0].tw"
		;
connectAttr "cineCam_rotation_grp_parentConstraint1.ctx" "cineCam_rotation_grp.tx"
		 -l on;
connectAttr "cineCam_rotation_grp_parentConstraint1.cty" "cineCam_rotation_grp.ty"
		 -l on;
connectAttr "cineCam_rotation_grp_parentConstraint1.ctz" "cineCam_rotation_grp.tz"
		 -l on;
connectAttr "cineCam_rotation_grp_parentConstraint1.crx" "cineCam_rotation_grp.rx"
		 -l on;
connectAttr "cineCam_rotation_grp_parentConstraint1.cry" "cineCam_rotation_grp.ry"
		 -l on;
connectAttr "cineCam_rotation_grp_parentConstraint1.crz" "cineCam_rotation_grp.rz"
		 -l on;
connectAttr "cineCam_rotation_grp_scaleConstraint1.csx" "cineCam_rotation_grp.sx"
		 -l on;
connectAttr "cineCam_rotation_grp_scaleConstraint1.csy" "cineCam_rotation_grp.sy"
		 -l on;
connectAttr "cineCam_rotation_grp_scaleConstraint1.csz" "cineCam_rotation_grp.sz"
		 -l on;
connectAttr "cineCam_world_ctrl.RigVisibility" "cineCam_rotation_grp.v";
connectAttr "cineCam_rotation_grp.ro" "cineCam_rotation_grp_parentConstraint1.cro"
		;
connectAttr "cineCam_rotation_grp.pim" "cineCam_rotation_grp_parentConstraint1.cpim"
		;
connectAttr "cineCam_rotation_grp.rp" "cineCam_rotation_grp_parentConstraint1.crp"
		;
connectAttr "cineCam_rotation_grp.rpt" "cineCam_rotation_grp_parentConstraint1.crt"
		;
connectAttr "cineCam_crane_top.t" "cineCam_rotation_grp_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_crane_top.rp" "cineCam_rotation_grp_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_crane_top.rpt" "cineCam_rotation_grp_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_crane_top.r" "cineCam_rotation_grp_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_crane_top.ro" "cineCam_rotation_grp_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_crane_top.s" "cineCam_rotation_grp_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_crane_top.pm" "cineCam_rotation_grp_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_rotation_grp_parentConstraint1.w0" "cineCam_rotation_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_rotation_grp.pim" "cineCam_rotation_grp_scaleConstraint1.cpim"
		;
connectAttr "cineCam_world_ctrl.s" "cineCam_rotation_grp_scaleConstraint1.tg[0].ts"
		;
connectAttr "cineCam_world_ctrl.pm" "cineCam_rotation_grp_scaleConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_rotation_grp_scaleConstraint1.w0" "cineCam_rotation_grp_scaleConstraint1.tg[0].tw"
		;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.ctx" "cineCam_crane_arm_grp.tx"
		 -l on;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.cty" "cineCam_crane_arm_grp.ty"
		 -l on;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.ctz" "cineCam_crane_arm_grp.tz"
		 -l on;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.crx" "cineCam_crane_arm_grp.rx"
		 -l on;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.cry" "cineCam_crane_arm_grp.ry"
		 -l on;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.crz" "cineCam_crane_arm_grp.rz"
		 -l on;
connectAttr "cineCam_crane_arm_grp_scaleConstraint1.csx" "cineCam_crane_arm_grp.sx"
		 -l on;
connectAttr "cineCam_crane_arm_grp_scaleConstraint1.csy" "cineCam_crane_arm_grp.sy"
		 -l on;
connectAttr "cineCam_crane_arm_grp_scaleConstraint1.csz" "cineCam_crane_arm_grp.sz"
		 -l on;
connectAttr "cineCam_world_ctrl.RigVisibility" "cineCam_crane_arm_grp.v";
connectAttr "cineCam_crane_arm_grp.ro" "cineCam_crane_arm_grp_parentConstraint1.cro"
		;
connectAttr "cineCam_crane_arm_grp.pim" "cineCam_crane_arm_grp_parentConstraint1.cpim"
		;
connectAttr "cineCam_crane_arm_grp.rp" "cineCam_crane_arm_grp_parentConstraint1.crp"
		;
connectAttr "cineCam_crane_arm_grp.rpt" "cineCam_crane_arm_grp_parentConstraint1.crt"
		;
connectAttr "cineCam_rotation_ctrl.t" "cineCam_crane_arm_grp_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_rotation_ctrl.rp" "cineCam_crane_arm_grp_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_rotation_ctrl.rpt" "cineCam_crane_arm_grp_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_rotation_ctrl.r" "cineCam_crane_arm_grp_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_rotation_ctrl.ro" "cineCam_crane_arm_grp_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_rotation_ctrl.s" "cineCam_crane_arm_grp_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_rotation_ctrl.pm" "cineCam_crane_arm_grp_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_crane_arm_grp_parentConstraint1.w0" "cineCam_crane_arm_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_crane_arm_grp.pim" "cineCam_crane_arm_grp_scaleConstraint1.cpim"
		;
connectAttr "cineCam_world_ctrl.s" "cineCam_crane_arm_grp_scaleConstraint1.tg[0].ts"
		;
connectAttr "cineCam_world_ctrl.pm" "cineCam_crane_arm_grp_scaleConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_crane_arm_grp_scaleConstraint1.w0" "cineCam_crane_arm_grp_scaleConstraint1.tg[0].tw"
		;
connectAttr "camRig_freehand_ctrl_GRP_parentConstraint1.ctx" "camCam_freehand_grp.tx"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_parentConstraint1.cty" "camCam_freehand_grp.ty"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_parentConstraint1.ctz" "camCam_freehand_grp.tz"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_orientConstraint1.crx" "camCam_freehand_grp.rx"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_orientConstraint1.cry" "camCam_freehand_grp.ry"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_orientConstraint1.crz" "camCam_freehand_grp.rz"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_scaleConstraint1.csx" "camCam_freehand_grp.sx"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_scaleConstraint1.csy" "camCam_freehand_grp.sy"
		 -l on;
connectAttr "camRig_freehand_ctrl_GRP_scaleConstraint1.csz" "camCam_freehand_grp.sz"
		 -l on;
connectAttr "cineCam_world_ctrl.RigVisibility" "camCam_freehand_grp.v";
connectAttr "camCam_freehand_grp.ro" "camRig_freehand_ctrl_GRP_parentConstraint1.cro"
		;
connectAttr "camCam_freehand_grp.pim" "camRig_freehand_ctrl_GRP_parentConstraint1.cpim"
		;
connectAttr "camCam_freehand_grp.rp" "camRig_freehand_ctrl_GRP_parentConstraint1.crp"
		;
connectAttr "camCam_freehand_grp.rpt" "camRig_freehand_ctrl_GRP_parentConstraint1.crt"
		;
connectAttr "cineCam_crane_arm_ctrl.t" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_crane_arm_ctrl.rp" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_crane_arm_ctrl.rpt" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_crane_arm_ctrl.r" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_crane_arm_ctrl.ro" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_crane_arm_ctrl.s" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_crane_arm_ctrl.pm" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "camRig_freehand_ctrl_GRP_parentConstraint1.w0" "camRig_freehand_ctrl_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "camCam_freehand_grp.ro" "camRig_freehand_ctrl_GRP_orientConstraint1.cro"
		;
connectAttr "camCam_freehand_grp.pim" "camRig_freehand_ctrl_GRP_orientConstraint1.cpim"
		;
connectAttr "cineCam_rotation_ctrl.r" "camRig_freehand_ctrl_GRP_orientConstraint1.tg[0].tr"
		;
connectAttr "cineCam_rotation_ctrl.ro" "camRig_freehand_ctrl_GRP_orientConstraint1.tg[0].tro"
		;
connectAttr "cineCam_rotation_ctrl.pm" "camRig_freehand_ctrl_GRP_orientConstraint1.tg[0].tpm"
		;
connectAttr "camRig_freehand_ctrl_GRP_orientConstraint1.w0" "camRig_freehand_ctrl_GRP_orientConstraint1.tg[0].tw"
		;
connectAttr "camCam_freehand_grp.pim" "camRig_freehand_ctrl_GRP_scaleConstraint1.cpim"
		;
connectAttr "cineCam_world_ctrl.s" "camRig_freehand_ctrl_GRP_scaleConstraint1.tg[0].ts"
		;
connectAttr "cineCam_world_ctrl.pm" "camRig_freehand_ctrl_GRP_scaleConstraint1.tg[0].tpm"
		;
connectAttr "camRig_freehand_ctrl_GRP_scaleConstraint1.w0" "camRig_freehand_ctrl_GRP_scaleConstraint1.tg[0].tw"
		;
connectAttr "cineCam_shake_grp_parentConstraint1.ctx" "cineCam_shake_grp.tx";
connectAttr "cineCam_shake_grp_parentConstraint1.cty" "cineCam_shake_grp.ty";
connectAttr "cineCam_shake_grp_parentConstraint1.ctz" "cineCam_shake_grp.tz";
connectAttr "cineCam_shake_grp_parentConstraint1.crx" "cineCam_shake_grp.rx";
connectAttr "cineCam_shake_grp_parentConstraint1.cry" "cineCam_shake_grp.ry";
connectAttr "cineCam_shake_grp_parentConstraint1.crz" "cineCam_shake_grp.rz";
connectAttr "cineCam.camerashake" "cineCam_shake_ctrl.v";
connectAttr "cineCam_shake_grp.ro" "cineCam_shake_grp_parentConstraint1.cro";
connectAttr "cineCam_shake_grp.pim" "cineCam_shake_grp_parentConstraint1.cpim";
connectAttr "cineCam_shake_grp.rp" "cineCam_shake_grp_parentConstraint1.crp";
connectAttr "cineCam_shake_grp.rpt" "cineCam_shake_grp_parentConstraint1.crt";
connectAttr "cineCam_freehand_ctrl.t" "cineCam_shake_grp_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_freehand_ctrl.rp" "cineCam_shake_grp_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_freehand_ctrl.rpt" "cineCam_shake_grp_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_freehand_ctrl.r" "cineCam_shake_grp_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_freehand_ctrl.ro" "cineCam_shake_grp_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_freehand_ctrl.s" "cineCam_shake_grp_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_freehand_ctrl.pm" "cineCam_shake_grp_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_shake_grp_parentConstraint1.w0" "cineCam_shake_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_focus_grp_parentConstraint1.ctx" "cineCam_focus_grp.tx";
connectAttr "cineCam_focus_grp_parentConstraint1.cty" "cineCam_focus_grp.ty";
connectAttr "cineCam_focus_grp_parentConstraint1.ctz" "cineCam_focus_grp.tz";
connectAttr "cineCam_focus_grp_parentConstraint1.crx" "cineCam_focus_grp.rx";
connectAttr "cineCam_focus_grp_parentConstraint1.cry" "cineCam_focus_grp.ry";
connectAttr "cineCam_focus_grp_parentConstraint1.crz" "cineCam_focus_grp.rz";
connectAttr "cineCam.FocusPlane" "cineCam_focusplane_ctrl.v" -l on;
connectAttr "expression1.out[0]" "cineCam_focusplane_ctrl.sx" -l on;
connectAttr "expression2.out[0]" "cineCam_focusplane_ctrl.sy" -l on;
connectAttr "transformGeometry6.og" "cineCam_focusplane_ctrlShape.i";
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.ctx" "cineCam_FocusPlane_loc.tx"
		 -l on;
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.cty" "cineCam_FocusPlane_loc.ty"
		 -l on;
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.ctz" "cineCam_FocusPlane_loc.tz"
		 -l on;
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.crx" "cineCam_FocusPlane_loc.rx"
		 -l on;
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.cry" "cineCam_FocusPlane_loc.ry"
		 -l on;
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.crz" "cineCam_FocusPlane_loc.rz"
		 -l on;
connectAttr "cineCam_FocusPlane_loc.ro" "cineCam_FocusPlane_loc_parentConstraint1.cro"
		;
connectAttr "cineCam_FocusPlane_loc.pim" "cineCam_FocusPlane_loc_parentConstraint1.cpim"
		;
connectAttr "cineCam_FocusPlane_loc.rp" "cineCam_FocusPlane_loc_parentConstraint1.crp"
		;
connectAttr "cineCam_FocusPlane_loc.rpt" "cineCam_FocusPlane_loc_parentConstraint1.crt"
		;
connectAttr "cineCam_focusplane_ctrl.t" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_focusplane_ctrl.rp" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_focusplane_ctrl.rpt" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_focusplane_ctrl.r" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_focusplane_ctrl.ro" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_focusplane_ctrl.s" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_focusplane_ctrl.pm" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_FocusPlane_loc_parentConstraint1.w0" "cineCam_FocusPlane_loc_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_focus_grp.ro" "cineCam_focus_grp_parentConstraint1.cro";
connectAttr "cineCam_focus_grp.pim" "cineCam_focus_grp_parentConstraint1.cpim";
connectAttr "cineCam_focus_grp.rp" "cineCam_focus_grp_parentConstraint1.crp";
connectAttr "cineCam_focus_grp.rpt" "cineCam_focus_grp_parentConstraint1.crt";
connectAttr "cineCam.t" "cineCam_focus_grp_parentConstraint1.tg[0].tt";
connectAttr "cineCam.rp" "cineCam_focus_grp_parentConstraint1.tg[0].trp";
connectAttr "cineCam.rpt" "cineCam_focus_grp_parentConstraint1.tg[0].trt";
connectAttr "cineCam.r" "cineCam_focus_grp_parentConstraint1.tg[0].tr";
connectAttr "cineCam.ro" "cineCam_focus_grp_parentConstraint1.tg[0].tro";
connectAttr "cineCam.s" "cineCam_focus_grp_parentConstraint1.tg[0].ts";
connectAttr "cineCam.pm" "cineCam_focus_grp_parentConstraint1.tg[0].tpm";
connectAttr "cineCam_focus_grp_parentConstraint1.w0" "cineCam_focus_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam.CameraAIm" "cineCam_aim_ctrl.v";
connectAttr "cineCam.CameraAIm" "cineCam_aim.v";
connectAttr "cineCam_camera_GRP_parentConstraint1.ctx" "cineCam_camera_grp.tx" -l
		 on;
connectAttr "cineCam_camera_GRP_parentConstraint1.cty" "cineCam_camera_grp.ty" -l
		 on;
connectAttr "cineCam_camera_GRP_parentConstraint1.ctz" "cineCam_camera_grp.tz" -l
		 on;
connectAttr "cineCam_camera_GRP_parentConstraint1.crx" "cineCam_camera_grp.rx" -l
		 on;
connectAttr "cineCam_camera_GRP_parentConstraint1.cry" "cineCam_camera_grp.ry" -l
		 on;
connectAttr "cineCam_camera_GRP_parentConstraint1.crz" "cineCam_camera_grp.rz" -l
		 on;
connectAttr "cineCam_camera_grp.ro" "cineCam_camera_GRP_parentConstraint1.cro";
connectAttr "cineCam_camera_grp.pim" "cineCam_camera_GRP_parentConstraint1.cpim"
		;
connectAttr "cineCam_camera_grp.rp" "cineCam_camera_GRP_parentConstraint1.crp";
connectAttr "cineCam_camera_grp.rpt" "cineCam_camera_GRP_parentConstraint1.crt";
connectAttr "cineCam_shake_ctrl.t" "cineCam_camera_GRP_parentConstraint1.tg[0].tt"
		;
connectAttr "cineCam_shake_ctrl.rp" "cineCam_camera_GRP_parentConstraint1.tg[0].trp"
		;
connectAttr "cineCam_shake_ctrl.rpt" "cineCam_camera_GRP_parentConstraint1.tg[0].trt"
		;
connectAttr "cineCam_shake_ctrl.r" "cineCam_camera_GRP_parentConstraint1.tg[0].tr"
		;
connectAttr "cineCam_shake_ctrl.ro" "cineCam_camera_GRP_parentConstraint1.tg[0].tro"
		;
connectAttr "cineCam_shake_ctrl.s" "cineCam_camera_GRP_parentConstraint1.tg[0].ts"
		;
connectAttr "cineCam_shake_ctrl.pm" "cineCam_camera_GRP_parentConstraint1.tg[0].tpm"
		;
connectAttr "cineCam_camera_GRP_parentConstraint1.w0" "cineCam_camera_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "cineCam_camshape_grp_aimConstraint1.crx" "cineCam_camshape_grp.rx" 
		-l on;
connectAttr "cineCam_camshape_grp_aimConstraint1.cry" "cineCam_camshape_grp.ry" 
		-l on;
connectAttr "cineCam_camshape_grp_aimConstraint1.crz" "cineCam_camshape_grp.rz" 
		-l on;
connectAttr "cineCam.visibility_vis" "cineCam.v";
connectAttr "cineCam.DisplayFilmGate" "cineCam_cam.dfg";
connectAttr "cineCam_focusplane_ctrl.tz" "cineCam_cam.fd";
connectAttr "cineCam.FocalLength" "cineCam_cam.fl";
connectAttr "cineCam.Focus_Region_Scale" "cineCam_cam.frs";
connectAttr "unitConversion2.o" "cineCam_cam.sa";
connectAttr "cineCam.NearClipPlane" "cineCam_cam.ncp";
connectAttr "cineCam.FarClipPlane" "cineCam_cam.fcp";
connectAttr "cineCam.Camera_Scale" "cineCam_cam.lls";
connectAttr "cineCam.DisplayGateMask" "cineCam_cam.dgm";
connectAttr "cineCam.DisplayResolution" "cineCam_cam.dr";
connectAttr "cineCam.GateMaskOpacity" "cineCam_cam.dgo";
connectAttr "cineCam.DisplayFieldChart" "cineCam_cam.dfc";
connectAttr "cineCam.DisplaySafeAction" "cineCam_cam.dsa";
connectAttr "cineCam.DisplaySafeTitle" "cineCam_cam.dst";
connectAttr "cineCam.DisplayFilmPivot" "cineCam_cam.dfp";
connectAttr "cineCam.DisplayFilmOrigin" "cineCam_cam.dfo";
connectAttr "cineCam.DepthofField" "cineCam_cam.dof";
connectAttr "cineCam.FStop" "cineCam_cam.fs";
connectAttr "cineCam.CameraAIm" "cineCam_camshape_grp_aimConstraint1.w0";
connectAttr "cineCam_camshape_grp.pim" "cineCam_camshape_grp_aimConstraint1.cpim"
		;
connectAttr "cineCam_camshape_grp.t" "cineCam_camshape_grp_aimConstraint1.ct";
connectAttr "cineCam_camshape_grp.rp" "cineCam_camshape_grp_aimConstraint1.crp";
connectAttr "cineCam_camshape_grp.rpt" "cineCam_camshape_grp_aimConstraint1.crt"
		;
connectAttr "cineCam_camshape_grp.ro" "cineCam_camshape_grp_aimConstraint1.cro";
connectAttr "cineCam_aim.t" "cineCam_camshape_grp_aimConstraint1.tg[0].tt";
connectAttr "cineCam_aim.rp" "cineCam_camshape_grp_aimConstraint1.tg[0].trp";
connectAttr "cineCam_aim.rpt" "cineCam_camshape_grp_aimConstraint1.tg[0].trt";
connectAttr "cineCam_aim.pm" "cineCam_camshape_grp_aimConstraint1.tg[0].tpm";
connectAttr "cineCam_camshape_grp_aimConstraint1.w0" "cineCam_camshape_grp_aimConstraint1.tg[0].tw"
		;
connectAttr "cineCam_guides_grp_parentConstraint1.ctx" "cineCam_guides_grp.tx";
connectAttr "cineCam_guides_grp_parentConstraint1.cty" "cineCam_guides_grp.ty";
connectAttr "cineCam_guides_grp_parentConstraint1.ctz" "cineCam_guides_grp.tz";
connectAttr "cineCam_guides_grp_parentConstraint1.crx" "cineCam_guides_grp.rx";
connectAttr "cineCam_guides_grp_parentConstraint1.cry" "cineCam_guides_grp.ry";
connectAttr "cineCam_guides_grp_parentConstraint1.crz" "cineCam_guides_grp.rz";
connectAttr "cineCam_cam.ncp" "cineCam_guides_loc_grp.tz";
connectAttr "cineCam_cam.ncp" "cineCam_guides_loc_grp.sx";
connectAttr "cineCam_cam.ncp" "cineCam_guides_loc_grp.sy";
connectAttr "multiplyDivide2.ox" "cineCam_guides_scale_grp.sx";
connectAttr "multiplyDivide2.ox" "cineCam_guides_scale_grp.sy";
connectAttr "cineCam_viewguide_2x2_visibility.o" "cineCam_viewguide_2x2.v";
connectAttr "transformGeometry19.og" "cineCam_viewguide_2xShape2.i";
connectAttr "cineCam_viewguide_3x3_visibility.o" "cineCam_viewguide_3x3.v";
connectAttr "transformGeometry20.og" "cineCam_viewguide_3xShape3.i";
connectAttr "cineCam_letterbox_4x3_visibility.o" "cineCam_letterbox_4x3.v";
connectAttr "groupId1.id" "cineCam_letterbox_4xShape3.iog.og[0].gid";
connectAttr "groupId3.id" "cineCam_letterbox_4xShape3.iog.og[1].gid";
connectAttr "deleteComponent7.og" "cineCam_letterbox_4xShape3.i";
connectAttr "groupId2.id" "cineCam_letterbox_4xShape3.ciog.cog[0].cgid";
connectAttr "cineCam_letterbox_2_39_visibility.o" "cineCam_letterbox_2_39.v";
connectAttr "groupId4.id" "cineCam_letterbox_2_Shape39.iog.og[0].gid";
connectAttr "groupId6.id" "cineCam_letterbox_2_Shape39.iog.og[1].gid";
connectAttr "deleteComponent8.og" "cineCam_letterbox_2_Shape39.i";
connectAttr "groupId5.id" "cineCam_letterbox_2_Shape39.ciog.cog[0].cgid";
connectAttr "cineCam_letterbox_1_90_visibility.o" "cineCam_letterbox_1_90.v";
connectAttr "groupId7.id" "cineCam_letterbox_1_Shape90.iog.og[0].gid";
connectAttr "groupId9.id" "cineCam_letterbox_1_Shape90.iog.og[1].gid";
connectAttr "deleteComponent9.og" "cineCam_letterbox_1_Shape90.i";
connectAttr "groupId8.id" "cineCam_letterbox_1_Shape90.ciog.cog[0].cgid";
connectAttr "cineCam_guides_grp.ro" "cineCam_guides_grp_parentConstraint1.cro";
connectAttr "cineCam_guides_grp.pim" "cineCam_guides_grp_parentConstraint1.cpim"
		;
connectAttr "cineCam_guides_grp.rp" "cineCam_guides_grp_parentConstraint1.crp";
connectAttr "cineCam_guides_grp.rpt" "cineCam_guides_grp_parentConstraint1.crt";
connectAttr "cineCam.t" "cineCam_guides_grp_parentConstraint1.tg[0].tt";
connectAttr "cineCam.rp" "cineCam_guides_grp_parentConstraint1.tg[0].trp";
connectAttr "cineCam.rpt" "cineCam_guides_grp_parentConstraint1.tg[0].trt";
connectAttr "cineCam.r" "cineCam_guides_grp_parentConstraint1.tg[0].tr";
connectAttr "cineCam.ro" "cineCam_guides_grp_parentConstraint1.tg[0].tro";
connectAttr "cineCam.s" "cineCam_guides_grp_parentConstraint1.tg[0].ts";
connectAttr "cineCam.pm" "cineCam_guides_grp_parentConstraint1.tg[0].tpm";
connectAttr "cineCam_guides_grp_parentConstraint1.w0" "cineCam_guides_grp_parentConstraint1.tg[0].tw"
		;
connectAttr "multMatrix10.o" "decomposeMatrix2.imat";
connectAttr "cineCam_crane_pivot.wm" "multMatrix10.i[0]";
connectAttr "cineCam_crane_top.wim" "multMatrix10.i[1]";
connectAttr "cineCam_focusplane_ctrl.tz" "expression1.in[0]";
connectAttr "cineCam_focusplane_ctrl.msg" "expression1.obm";
connectAttr "cineCam_focusplane_ctrl.tz" "expression2.in[0]";
connectAttr "cineCam_focusplane_ctrl.msg" "expression2.obm";
connectAttr "transformGeometry5.og" "transformGeometry6.ig";
connectAttr "transformGeometry4.og" "transformGeometry5.ig";
connectAttr "polyPlane1.out" "transformGeometry4.ig";
connectAttr "cineCam.ShutterAngle" "unitConversion2.i";
connectAttr "cineCam_cam.fl" "multiplyDivide2.i2x";
connectAttr "multiplyDivide1.ox" "multiplyDivide2.i1x";
connectAttr "cineCam_cam.hfa" "multiplyDivide1.i1x";
connectAttr "cineCam.Grid_vis" "cineCam_viewguide_2x2_visibility.i";
connectAttr "polyPlane6.out" "transformGeometry19.ig";
connectAttr "cineCam.Grid_vis" "cineCam_viewguide_3x3_visibility.i";
connectAttr "polyPlane5.out" "transformGeometry20.ig";
connectAttr "cineCam.Letterbox_vis" "cineCam_letterbox_4x3_visibility.i";
connectAttr "transformGeometry16.og" "deleteComponent7.ig";
connectAttr "transformGeometry13.og" "transformGeometry16.ig";
connectAttr "transformGeometry10.og" "transformGeometry13.ig";
connectAttr "transformGeometry7.og" "transformGeometry10.ig";
connectAttr "deleteComponent5.og" "transformGeometry7.ig";
connectAttr "groupParts2.og" "deleteComponent5.ig";
connectAttr "groupParts1.og" "groupParts2.ig";
connectAttr "groupId3.id" "groupParts2.gi";
connectAttr "polyPlane2.out" "groupParts1.ig";
connectAttr "groupId1.id" "groupParts1.gi";
connectAttr "cineCam.Letterbox_vis" "cineCam_letterbox_2_39_visibility.i";
connectAttr "transformGeometry17.og" "deleteComponent8.ig";
connectAttr "transformGeometry14.og" "transformGeometry17.ig";
connectAttr "transformGeometry11.og" "transformGeometry14.ig";
connectAttr "transformGeometry8.og" "transformGeometry11.ig";
connectAttr "polyTweak1.out" "transformGeometry8.ig";
connectAttr "deleteComponent4.og" "polyTweak1.ip";
connectAttr "deleteComponent3.og" "deleteComponent4.ig";
connectAttr "deleteComponent2.og" "deleteComponent3.ig";
connectAttr "deleteComponent1.og" "deleteComponent2.ig";
connectAttr "groupParts4.og" "deleteComponent1.ig";
connectAttr "groupParts3.og" "groupParts4.ig";
connectAttr "groupId6.id" "groupParts4.gi";
connectAttr "polyPlane3.out" "groupParts3.ig";
connectAttr "groupId4.id" "groupParts3.gi";
connectAttr "cineCam.Letterbox_vis" "cineCam_letterbox_1_90_visibility.i";
connectAttr "transformGeometry18.og" "deleteComponent9.ig";
connectAttr "transformGeometry15.og" "transformGeometry18.ig";
connectAttr "transformGeometry12.og" "transformGeometry15.ig";
connectAttr "transformGeometry9.og" "transformGeometry12.ig";
connectAttr "deleteComponent6.og" "transformGeometry9.ig";
connectAttr "groupParts6.og" "deleteComponent6.ig";
connectAttr "groupParts5.og" "groupParts6.ig";
connectAttr "groupId9.id" "groupParts6.gi";
connectAttr "polyPlane4.out" "groupParts5.ig";
connectAttr "groupId7.id" "groupParts5.gi";
connectAttr "multMatrix10.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "cineCam_letterbox_4xShape3.ciog.cog[0]" ":initialShadingGroup.dsm" 
		-na;
connectAttr "cineCam_letterbox_2_Shape39.ciog.cog[0]" ":initialShadingGroup.dsm"
		 -na;
connectAttr "cineCam_letterbox_1_Shape90.ciog.cog[0]" ":initialShadingGroup.dsm"
		 -na;
connectAttr "groupId2.msg" ":initialShadingGroup.gn" -na;
connectAttr "groupId5.msg" ":initialShadingGroup.gn" -na;
connectAttr "groupId8.msg" ":initialShadingGroup.gn" -na;
// End of camera_template.ma
