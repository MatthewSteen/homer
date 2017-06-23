import csv
import os
import pandas as pd
# import beopt_units

"""
A collection of functions for generating and manipulating data for HOMER.
@author Matt Steen
""" 

def annual_hourly_from_monthly(data_path):
    """Generates annual hourly data from monthly data.
    Read format is... 
    Write format is 1 col x 8760 row for HOMER.
    """
    
    #TODO
    
  
def annual_hourly_from_daily_hourly(data_path, col_name):
    """Generates annual hourly data from daily profile.
    Read format is 1 col x 25 row with header.
    Write format is 1 col x 8760 row for HOMER.    
    """
    
    df = pd.read_csv(data_path)
    col_data = df[col_name]
#     print type(col_data)
    
    with open(col_name + '.csv', 'wb') as fname:    

        for i in range(365):

            for j in col_data.iteritems(): 

                fname.write('%d,' % j[1])
                fname.write('\n')

    return fname
  
def annual_hourly_from_annual_daily(data_path, col_name):
    """Generates annual hourly data from annual daily data.
    Read format is 1 col x 366 row with header.
    Write format is 1 col x 8760 row for HOMER.
    """
    
    df = pd.read_csv(data_path)
    col_data = df[col_name]
    
    with open(col_name + '.csv', 'wb') as fname:    
        
        for row in col_data:
          
            for i in range(24):
              
                fname.write('%f' % row) #beopt_units.ft32liter(row)
                fname.write('\n')

    return fname
   
    
def annual_hourly_from_hour(file_name, hour_value):
    """Generates annual hourly data from single hour value.
    Read format is none.
    Write format is 1 col x 8760 row for HOMER.
    """
    
    with open(file_name + '.csv', 'wb') as fname:
      
        for i in range(8760):
          
            fname.write('%d' % hour_value)
            fname.write('\n')
            
    return fname

  
def dview(file_path):
    """Generates a file in DView format from a HOMER simulation results CSV file.
    https://beopt.nrel.gov/downloadDView
    https://beopt.nrel.gov/sites/beopt.nrel.gov/files/exes/DataFileTemplate.pdf
    """

    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    dview_file_name = file_name.replace('.csv', '.dview')
    dview_file_path = os.path.join(file_dir, dview_file_name)

    homer_file = open(file_path, 'rb')
    dview_file = open(dview_file_path, 'wb')

    reader = csv.reader(homer_file)
    writer = csv.writer(dview_file)

    for idx, line in enumerate(reader):

        # delete first column, which is the "End Time" timestamp
        del line[0]

        if idx == 0:

            # skip first row, which only has "sep="
            continue

        elif idx == 2:

            # TODO replace degree symbol in third row (units)
            for s in line:

                s.replace('\xc2\xb0', 'deg')

        # write line to new file
        writer.writerow(line)

    # close files
    homer_file.close()
    dview_file.close()