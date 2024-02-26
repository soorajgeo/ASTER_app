import ee
from utils.data_conversion import aster_radiance, aster_reflectance, aster_brightness_temp
from utils.mask import aster_ndvi_mask, aster_snow_mask, aster_cloud_mask, trim_edge, water_mask_ast

def aster_bands_present_filter(collection):
    """
    Takes an image collection, assumed to be ASTER imagery.
    Returns a filtered image collection that contains only
    images with all nine VIR/SWIR bands and all 5 TIR bands.
    """
    return collection.filter(ee.Filter.And(
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B01'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B02'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B3N'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B04'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B05'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B06'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B07'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B08'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B09'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B10'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B11'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B12'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B13'),
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B14')
))

def temporal_aster_preprocessing(geom,buffer):
    """
    Takes a geometry (ee.ComputedObject, ee.FeatureCollection, or ee.Geometry).
    Collects ASTER satellite imagery that intersects the geometry and
    implements all available preprocessing functions.
    Reduces resulting ImageCollection to a single Image object
    by calculating the median pixel value.
    Clips the image to the geometry.
    Returns a dictionary containing the processed image along with 
    the crs and crs_transform metadata of the first image in the
    ImageCollection that intersects the geometry.
    """
    coll = ee.ImageCollection("ASTER/AST_L1T_003")
    coll = coll.filterBounds(geom)
    coll = aster_bands_present_filter(coll)
    crs = coll.first().select('B01').projection().getInfo()['crs']
    transform = coll.first().select('B01').projection().getInfo()['transform']
    coll = coll.map(aster_radiance)
    coll = coll.map(aster_reflectance)
    coll = coll.map(aster_brightness_temp) 
    
    coll = coll.map(aster_cloud_mask)
    coll = coll.map(aster_snow_mask)
    coll = coll.map(trim_edge(buffer))
    # coll = coll.map(aster_ndvi_mask)
    coll = coll.median().clip(geom)
    coll = water_mask_ast(coll)
    
    
    return {'imagery': coll, 'crs': crs, 'transform': transform}


def spatial_aster_preprocessing(geom, cloudcover):
    
    '''
    Takes a geometry (ee.ComputedObject, ee.FeatureCollection, or ee.Geometry).
    Collects ASTER satellite imagery that intersects the geometry and
    implements all available preprocessing functions.
    Filters by cloud cover and then sort.
    Returns a dictionary containing the processed image along with 
    the crs and crs_transform metadata of the first image in the
    ImageCollection that intersects the geometry.
    '''
    coll = ee.ImageCollection("ASTER/AST_L1T_003").filter(ee.Filter.lt('CLOUDCOVER',cloudcover))
    coll = coll.filterBounds(geom)
    coll = aster_bands_present_filter(coll)
    
    crs = coll.first().select('B01').projection().getInfo()['crs']
    transform = coll.first().select('B01').projection().getInfo()['transform']

    coll = coll.map(aster_radiance)
    coll = coll.map(aster_reflectance)
    coll = coll.map(aster_brightness_temp)

    
    coll = coll.sort('CLOUDCOVER')
    
    
    return {'imagery': coll, 'crs': crs, 'transform': transform}