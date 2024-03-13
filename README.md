
# ASTER app

This is a web application built with [streamlit](https://streamlit.io/) and [geemap](https://geemap.org/). geemap is python package for interactive geospatial analysis and visualization with [Google Earth Engine](https://cloud.google.com/earth-engine?hl=en). The application can be accessed through the link [https://aster-app.streamlit.app/](https://aster-app.streamlit.app/). The image processing is carried out using the free tier of my google cloud service account. 


## Brief about the application
The application uses ASTER_LIT data hosted in google earth engine which is available through [this link](https://developers.google.com/earth-engine/datasets/catalog/ASTER_AST_L1T_003). 
The preprocessing steps were done using the code in the github repo [ASTER_preprocessing](https://github.com/Mining-for-the-Future/ASTER_preprocessing) with minor changes to the water masking functions. See the repo for all the image pre processing workflow. Image trimming functions were included to prevent lines appearing in the final output image.
The preprocessing functions uses the [image reducer](https://developers.google.com/earth-engine/guides/reducers_image_collection) functions of earth engine to provide a cloud free image. If there are clouds, if any, present in the processed image, cloud masking function will mask the clouds. 

## Steps for generating the mineral indices map
1. Enter the bounding cordinates of the area in Decimal Degrees and press submit Maximum area that the app can process is limited to 800 sq.km due to free google cloud quota limits set by earth engine.
2. Lines may appear in the final output image due to errors in the ASTER scene edges. Enter trimming distance (100 to 1000 is ideal) for preventing this. Press submit.
3. Enter values to mask vegetation and press submit. If you do not want to mask vegetation, enter 1, otherwise try values between 0.5 and 1.
4. Enter min and max values with which the final output image will be displayed. Skip this step if you wish to open the final image in a GIS software which will be better to visualise than in this app.
5. Enter the image resolution to be downloaded (any value between 30 to 90) or accept the default value of 30. 
5. Finally select the mineral indices from the drop down and wait for the image to appear. If any "User memory limit exceeded" error appears, decrease the resolution in the previous step and try again. If you have skipped the previous step, the image will be displayed with the default min (0) and max(1) values. Download this image and view in any GIS software. Adjust the min/max value settings in the GIS software byy going to the symbology tab. 


## Demo



## Run Locally

Clone the project

```bash
  git clone https://github.com/soorajgeo/ASTER_app.git
```

Go to the project directory

```bash
  cd project_directory
```
Create virtual environment and install dependencies in a virtual environment

```bash
  pip install -r requirements.txt
```

run the python file

```bash
  streamlit run app.py
```

