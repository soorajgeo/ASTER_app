import streamlit as st
import geemap.foliumap as geemap
import ee
from utils.preprocessing import temporal_aster_preprocessing
from utils.mask import aster_cloud_mask, aster_ndvi_mask, water_mask_ast, trim_edge
from utils.indices import calculate_indices
import os
from google.oauth2 import service_account


json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

credentials = ee.ServiceAccountCredentials(service_account, key_data=json_data)


ee.Initialize(credentials)
out_dir = os.path.join(os.path.expanduser('~'), 'Downloads')


st.set_page_config(layout="wide")

# Customize page title
st.title("ASTER app")

st.markdown(
    """
    This app helps to generate mineral indices map with ASTER_L1T data and is deployed using [streamlit](https://streamlit.io) and [geemap](https://geemap.org). It is an open-source project and you are very welcome to check the [GitHub repository](https://github.com/soorajgeo/ASTER_app).
    """
)

st.header("General information")

markdown = """
1. Mineral indices used in the app is available in this [pdf](https://aslenv.com/assets/files/ASTER_Processing_for_Mineral_Exploration.pdf) 
2. The preprocessing of ASTER images were done using the github repo [ASTER_preprocessing](https://github.com/Mining-for-the-Future/ASTER_preprocessing) 
3. Indices can be calculated only for areas less than 800 sq.km. Please provide the bounding coordinates accordingly

"""

st.markdown(markdown)
Map = geemap.Map()


if 'selection' not in st.session_state:
  st.session_state.selection = ['ferric[2/1]','ferrous[(5/3)+(1/2)]','laterite/alteration[4/5]','gossan[4/2]',
                                'fe-silicates[5/4]','ferric oxide[4/3]','carb-chl-epi[(7+9)/8]','epi-chl-amp[(6+9)/(7+8)]',
                                'MgOH[(6+9)/8]','amphibole[6/8]','dolomite[(6+8)/7]','carbonate[13/14]','seri-mus-smec[(5+7)/6]',
                                'alun-kaol-pyro[(4+6)/5]','phengite[5/6]','muscovite[7/6]','kaolinite[7/5]','clay[(5*7)/(6*6)]',
                                'quartz rich[14/12]','silica1[(11*11)/(10/12)]','silica2[13/10]','BDI[12/13]','SiO2[13/12]'
                                ]
  

if 'temp_image' not in st.session_state:
  st.session_state.temp_image = None

if 'masked_img' not in st.session_state:
    st.session_state.masked_img = None


  
col1, col2 = st.columns([4,1])


with col1:
    Map.add_basemap('HYBRID')
    if "area" in st.session_state:
        Map.addLayer(st.session_state.area, {}, 'area', opacity=0.5)
        Map.setCenter((st.session_state.minx+st.session_state.maxx)/2, (st.session_state.miny+st.session_state.maxy)/2 )

    vis_params = {'bands':['B05', 'B04', 'B3N'], 'min':0, 'max':0.5}

    with col2:    
        with st.form(key='latlong form'):
            st.write("Enter bounding coordinates in decimal degrees")
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            c1.number_input("MinX ", value=None, placeholder= 'MinX', help = "Min value (DD) for Longitude",label_visibility='collapsed', key='minx')
            c2.number_input("MaxX", value=None, placeholder= 'MaxX', help = "Max value (DD) for Longitude",
                            label_visibility='collapsed', key = 'maxx')
            c3.number_input("MinY", value=None, placeholder= 'MinY', help = "Min value (DD) for latitude",
                            label_visibility='collapsed', key = 'miny')
            c4.number_input("MaxY", value=None, placeholder='MaxY', help = "Max value (DD) for latitude",
                            label_visibility='collapsed', key = 'maxy')
                
            submitted = st.form_submit_button('Submit', help="Click to zoom into your area")
    
        if submitted:
        
            area = ee.Geometry.Rectangle([st.session_state.minx, st.session_state.miny, st.session_state.maxx, st.session_state.maxy])
            sqkm = ee.Number(area.area()).divide(1e6).round().getInfo()
        
            if sqkm> 800:
                st.warning('Please provide smaller area. Refresh the page to continue', icon="⚠️")
                st.stop()
            st.session_state.area = area
            Map.addLayer(area, {}, 'area', opacity=0.5)
            Map.setCenter((st.session_state.minx+st.session_state.maxx)/2, (st.session_state.miny+st.session_state.maxy)/2 )
    
        st.number_input("Trim distance", value=100, help='Enter distance by which ASTER images will be cropped to avoid errors at scene edges', key='trim')

        button_click = st.button("Submit", help='Click to see the processed imagery')

        if button_click:
            with st.spinner('Processing ASTER images...'):
                image = temporal_aster_preprocessing(st.session_state.area, st.session_state.trim)
                st.session_state.temp_image = image['imagery']
                Map.addLayer(st.session_state.temp_image, vis_params, 'Processed image')

        with st.form(key='NDVI form'):
            st.number_input("NDVI mask ", value=1.0, help="If you do not want to mask vegetation, enter 1, otherwise enter values between 0 and 1", key='vegmask')
            
            
            submit = st.form_submit_button('Submit', help='Click to see the NDVI masked image')

        if submit:
            with st.spinner('Applying NDVI mask...'):
                ndvi_mask = aster_ndvi_mask(st.session_state.temp_image, st.session_state.vegmask)
                st.session_state.masked_img = ndvi_mask
                Map.addLayer(ndvi_mask, vis_params, "Masked")

        st.write("Enter min and max values for visualisation")
        c5, c6 = st.columns(2)
        min = c5.number_input("Max",value=0.0,min_value=0.0,max_value=10.0, step=1., placeholder='min',label_visibility='collapsed',key='min')
        max = c6.number_input("Min",value=1.0,min_value=0.0,max_value=10.0, step=1., placeholder='max',label_visibility='collapsed',key='max')

        index = st.selectbox('Select the indices', options=st.session_state.selection, placeholder="Select indices",
                         label_visibility='collapsed',index=None)
        if index:
            with st.spinner('Calculating indices...'):
                index_map = calculate_indices(st.session_state.masked_img, index)
                Map.addLayer(index_map, {'min':min, 'max':max}, index)
        
        download = st.button('Download', help="Images will be saved in your DOWNLOADS folder")
        if download:
            with st.spinner('Downloading...'):
                filename = os.path.join(out_dir, index_map.getInfo()['bands'][0]['id']+'.tif')
                geemap.ee_export_image(
                    index_map, filename=filename, scale=30, region=st.session_state.area, file_per_band=False
                )
                
                st.success('Downloaded', icon="✅")


    Map.to_streamlit()

  
  
 