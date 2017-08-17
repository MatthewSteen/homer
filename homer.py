import csv
import os
import pandas as pd
# import beopt_units

"""
A collection of functions for generating and manipulating data for HOMER.
@author Matt Steen
""" 

def annual_hourly_from_monthly_hourly(file_path):
    """Generates annual hourly data from monthly data.
    Read format is 12 col x 24 row (months x hours)
    Write format is 1 col x 8760 row for HOMER.
    """
    
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    file_name_new = file_name.replace('.csv', '_annual.csv')
    #file_path_new = os.path.join(file_dir, file_name_new)

    df = pd.read_csv(file_path, header=None)

    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    with open(file_name_new, 'wb') as fname:    

        for i in range(len(df.columns)):

            col_data = df[i]

            for j in range(days_per_month[i]):

                for k in col_data.iteritems(): 

                    fname.write('%d' % k[1])
                    fname.write('\n')

    return fname
    

def annual_hourly_from_daily_hourly(data_path, col_name):
    """Generates annual hourly data from daily profile.
    Read format is 1 col x 25 row with header.
    Write format is 1 col x 8760 row for HOMER.    
    """
    
    df = pd.read_csv(data_path)
    col_data = df[col_name]
    print type(col_data)
    
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
    
    
def replace_annual_hourly_values(file_path, month, day, day_length, value):
    """Replaces values in an annual hourly file starting at a month and day of the year
    for a specific number of days.
    Read and write format is 1 col x 8760 row for HOMER.
    Write file name is appended with '_#day', where # is the day_length.
    Useful for exploring equipment shutdowns, e.g. setting loads to zero.
    """
    
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    file_name_new = file_name.replace('.csv', '_%s.csv' % (str(day_length)+'day'))
    file_path_new = os.path.join(file_dir, file_name_new)

    file = open(file_path, 'rb')
    file_new = open(file_path_new, 'wb')

    reader = csv.reader(file)
    writer = csv.writer(file_new)

    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    hour_start = sum(days_per_month[:month-1]) * 24 + ((day - 1) * 24)
    hour_end = sum(days_per_month[:month-1]) * 24 + ((day - 1 + day_length) * 24)

    for idx, row in enumerate(reader):

        hour_of_year = idx + 1

        if hour_start <= hour_of_year <= hour_end:
            writer.writerow('%d' % value)
        else: 
            writer.writerow(row)

    file.close()
    file_new.close()