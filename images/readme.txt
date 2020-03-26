
Pivoted due to lack of hardware components:

Indoor Autonomous Navigation Solution Using CCTV footage and Cloud Compute:

The aim is to enable Indoor Autonomous Navigation for Robots in Facilities like Hospitals and  Shopping Malls while the Indoor Environment is covered by CCTV surveillance.
The facilities just need to invest in Robot chassis and Raspberry Pi Zero for mobility and controls and Cloud subscription for Computation.

The environment will be covered by CCTV, which will be used for Mapping and Localization, hence we do not need any additional new sensors on the robot.
The computation of trajectories is also moved to cloud with Azure Containers, which receive image frames using Azure Queue and estimates trajectories of the robot and puts them on a different Azure Queue for the Physical Robot to access.
The solution also comes with a web application to add and remove multiple robots as required by the facility and check robot health status.
The map generated of the facility can be stored using Azure Blob.

This is a cost effective solution as upfront investments on Compute units like Nvidia Jeson and Stereo Camera is mitigated by using Cloud Compute and CCTV cameras.

Assumptions:
The facilities have their floor area covered under CCTV and Wifi Access Point Range. 

Use Case:
Automated stretchers to carry patients to different wards of the Hospitals.
Automated carts in shopping malls for auto billing which can save customer time.
Automate Food Carts at Food Courts of Malls.
