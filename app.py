import streamlit as st
import geemap.foliumap as geemap
import ee
import requests
from utils.preprocessing import temporal_aster_preprocessing
from utils.mask import aster_cloud_mask, aster_ndvi_mask, water_mask_ast, trim_edge
from utils.indices import calculate_indices
from google.oauth2 import service_account


json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

credentials = ee.ServiceAccountCredentials(service_account, key_data=json_data)


ee.Initialize(credentials)

st.set_page_config(layout="wide")

# Customize page title
st.title("ASTER app")

st.markdown(
    """
    This app helps to generate mineral indices map with ASTER_L1T data and is deployed using [streamlit](https://streamlit.io) and [geemap](https://geemap.org). It is an open-source project and you are very welcome to check my [GitHub repository](https://github.com/soorajgeo/ASTER_app) for detailed information and demo.
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
  st.session_state.selection = ['ferric[2/1]','ferrous[(5/3)+(1/2)]','alteration[4/5]','gossan[4/2]',
                                'fe_silicates[5/4]','ferric_oxide[4/3]','carb_chl_epi[(7+9)/8]','epi-chl-amp[(6+9)/(7+8)]',
                                'MgOH[(6+9)/8]','amphibole[6/8]','dolomite[(6+8)/7]','carbonate[13/14]','seri_mus_smec[(5+7)/6]',
                                'alun_kaol_pyro[(4+6)/5]','phengite[5/6]','muscovite[7/6]','kaolinite[7/5]','clay[(5*7)/(6*6)]',
                                'quartz_rich[14/12]','silica1[(11*11)/(10/12)]','silica2[13/10]','BDI[12/13]','SiO2[13/12]'
                                ]
  

if 'temp_image' not in st.session_state:
  st.session_state.temp_image = None

if 'masked_img' not in st.session_state:
    st.session_state.masked_img = None


@st.cache_data(show_spinner=False,persist="disk")
def export_image(_image, filename, scale, _area):
    url = _image.getDownloadUrl({
                    'scale': scale,
                    'crs': 'EPSG:4326',
                    'region': _area,
                    'format': 'GEO_TIFF'
                })
    response = requests.get(url)
    
    if response.status_code == 400:
        st.error("User memory limit exceeded. Clear the above select box and rerun using decreased resolution")
        st.cache_data.clear()
        st.stop()
    else:
        with open(filename, 'wb') as fd:
            fd.write(response.content)
            
    


col1, col2 = st.columns([4,1])


with col1:
    Map.add_basemap('HYBRID')
    if "area" in st.session_state:
        Map.addLayer(st.session_state.area, {}, 'area', opacity=0.5)
        Map.setCenter((st.session_state.minx+st.session_state.maxx)/2, (st.session_state.miny+st.session_state.maxy)/2, zoom=11 )
        

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
            Map.setCenter((st.session_state.minx+st.session_state.maxx)/2, (st.session_state.miny+st.session_state.maxy)/2, zoom=11)
    
        st.number_input("Trim distance", value=100, min_value=1, help='Distance (try values between 100-1000) by which ASTER scenes will be cropped to avoid lines in the final output image', key='trim')

        button_click = st.button("Submit", help='Click to see the processed imagery')

        if button_click:
            with st.spinner('Processing ASTER images...'):
                image = temporal_aster_preprocessing(st.session_state.area, st.session_state.trim)
                st.session_state.temp_image = image['imagery']
                Map.addLayer(st.session_state.temp_image, vis_params, 'Processed image')

        with st.form(key='NDVI form'):
            st.number_input("NDVI mask ", value=1.0, min_value=0.2, max_value=1.0, help="If you do not want to mask vegetation, enter 1, otherwise try values between 0.5 and 1", key='vegmask')
            
            
            submit = st.form_submit_button('Submit', help='Click to see the NDVI masked image')

        if submit:
            with st.spinner('Applying NDVI mask...'):
                ndvi_mask = aster_ndvi_mask(st.session_state.temp_image, st.session_state.vegmask)
                st.session_state.masked_img = ndvi_mask
                Map.addLayer(ndvi_mask, vis_params, "NDVI Masked")

        st.write("Enter min and max values OR skip this step to download the selected indices and view in any GIS software.")
        c5, c6 = st.columns(2)
        min = c5.number_input("Min",value=0.0,min_value=0.0,max_value=10.0, step=1., placeholder='min',key='min')
        max = c6.number_input("Max",value=1.0,min_value=0.0,max_value=10.0, step=1., placeholder='max',key='max')

        scale = st.number_input(label="Enter resolution of image to download (30-90)", value=30, min_value=30, max_value=90, key='scale')

        index = st.selectbox('Select the indices', options=st.session_state.selection, placeholder="Select indices",
                         label_visibility='collapsed',index=None)
        

        if index:
            with st.spinner('Calculating indices...'):
                index_map = calculate_indices(st.session_state.masked_img, index)
                Map.addLayer(index_map, {'min':min, 'max':max}, index)
                file_name = index_map.getInfo()['bands'][0]['id']+'.tif'
                
                image = export_image(index_map,file_name, st.session_state.scale, st.session_state.area)
                
      
        if index is not None:
            file_name = index.split('[')[0]+'.tif'
            try:
                with open(file_name, 'rb') as fd:
                    st.download_button('Download',fd,file_name=file_name, mime = "image/tiff")
            except:
                st.error("There seems to be an error. Refresh the page")
                st.stop()
                        
                
    Map.to_streamlit()