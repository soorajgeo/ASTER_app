def calculate_indices(image, index):
  if index == 'ferric[2/1]':
    ferric = image.expression('B2 / B1',{
          'B1': image.select('B02'),
          'B2': image.select('B01')
      }).rename('ferric')
    return ferric
  
  elif index == 'ferrous[(5/3)+(1/2)]':
    ferrous = image.expression('(B5/B3) + (B1/B2)',{
          'B1': image.select('B01'),
          'B2': image.select('B02'),
          'B3': image.select('B3N'),
          'B5': image.select('B05'),
      }).rename('ferrous')
    
    return ferrous
  
  elif index == 'alteration[4/5]':
    laterite = image.expression('B4/B5',{
          'B4': image.select('B04'),
          'B5': image.select('B05'),
          }).rename('alteration')
    
    return laterite
  
  elif index == 'gossan[4/2]':
    gossan = image.expression('B4/B2',{
          'B2': image.select('B02'),
          'B4': image.select('B04'),
          }).rename('gossan')
    
    return gossan
  
  elif index == 'fe_silicates[5/4]':
    fesilicate = image.expression('B5/B4',{
          'B4': image.select('B04'),
          'B5': image.select('B05'),
          }).rename('fe_silicates')
    
    return fesilicate
  
  elif index == 'ferric_oxide[4/3]':
    feoxide = image.expression('B4/B3',{
          'B3': image.select('B3N'),
          'B4': image.select('B04'),
          }).rename('ferric_oxide')
    
    return feoxide
  
  elif index == 'carb_chl_epi[(7+9)/8]':
    carchlepi = image.expression('(B7+B9)/B8',{
          'B7': image.select('B07'),
          'B8': image.select('B08'),
          'B9': image.select('B09'),
          }).rename('carb_chl_epi')
    
    return carchlepi
  
  elif index == 'epi-chl-amp[(6+9)/(7+8)]':
    epidote = image.expression('(B6+B9)/(B7+B8)',{
          'B6': image.select('B06'),
          'B7': image.select('B07'),
          'B8': image.select('B08'),
          'B9': image.select('B09'),
          }).rename('epi-chl-amp')
    
    return epidote
  
  elif index == 'MgOH[(6+9)/8]':
    mgoh = image.expression('(B6+B9)/B8',{
          'B6': image.select('B06'),
          'B8': image.select('B08'),
          'B9': image.select('B09'),
          }).rename('MgOH')
    
    return mgoh
  
  elif index == 'amphibole[6/8]':
    amphi = image.expression('B6/B8',{
          'B6': image.select('B06'),
          'B8': image.select('B08'),
          }).rename('amphibole')
    
    return amphi
  
  elif index == 'dolomite[(6+8)/7]':
    dolomite = image.expression('(B6+B8)/B7',{
          'B6': image.select('B06'),
          'B7': image.select('B07'),
          'B8': image.select('B08'),
          }).rename('dolomite')
    
    return dolomite
  
  elif index == 'carbonate[13/14]':
    carbonate = image.expression('B13/B14',{
          'B13': image.select('B13'),
          'B14': image.select('B14'),
          }).rename('carbonate')
    
    return carbonate
  
  elif index == 'seri_mus_smec[(5+7)/6]':
    sermusmec = image.expression('(B5+B7)/B6',{
          'B5': image.select('B05'),
          'B6': image.select('B06'),
          'B7': image.select('B07'),
          }).rename('seri_mus_smec')
    
    return sermusmec
  
  elif index == 'alun_kaol_pyro[(4+6)/5]':
    alukaopyro = image.expression('(B4+B6)/B5',{
          'B4': image.select('B04'),
          'B5': image.select('B05'),
          'B6': image.select('B06'),
          }).rename('alun_kaol_pyro')
    
    return alukaopyro
  
  elif index == 'phengite[5/6]':
    phengite = image.expression('B5/B6',{
          'B5': image.select('B05'),
          'B6': image.select('B06'),
          }).rename('phengite')
    
    return phengite
  
  
  elif index == 'muscovite[7/6]':
    muscovite = image.expression('B7 / B6',{
          'B6': image.select('B06'),
          'B7': image.select('B07')
      }).rename('muscovite')
   
    return muscovite
  
  elif index == 'kaolinite[7/5]':
    kaolinite = image.expression('B7 / B5',{
          'B5': image.select('B05'),
          'B7': image.select('B07')
      }).rename('kaolinite')
    
    return kaolinite
  
  elif index == 'clay[(5*7)/(6*6)]':
    clay = image.expression('(B5*B7) / (B6*B6)',{
          'B5': image.select('B05'),
          'B6': image.select('B06'),
          'B7': image.select('B07'),
      }).rename('clay')
    
    return clay
  
  elif index == 'quartz_rich[14/12]':
    quartz = image.expression('B14/B12',{
          'B12': image.select('B12'),
          'B14': image.select('B14'),
          'B7': image.select('B07'),
      }).rename('quartz_rich')
    
    return quartz
  
  elif index == 'silica1[(11*11)/(10/12)]':
    silica1 = image.expression('(B11*B11)/(B10/B12)',{
          'B10': image.select('B10'),
          'B11': image.select('B11'),
          'B12': image.select('B12'),
      }).rename('silica1')
    
    return silica1
  
  elif index == 'silica2[13/10]':
    silica2 = image.expression('B13/B10',{
          'B10': image.select('B10'),
          'B13': image.select('B13'),
      }).rename('silica2')
    
    return silica2
  
  elif index == 'BDI[12/13]':
    BDI = image.expression('B12/B13',{
          'B12': image.select('B12'),
          'B13': image.select('B13'),
      }).rename('BDI')
    
    return BDI
  
  elif index == 'SiO2[13/12]':
    SiO2 = image.expression('B13/B12',{
          'B12': image.select('B12'),
          'B13': image.select('B13'),
      }).rename('SiO2')
    
    return SiO2
  
      
  
  
   
  