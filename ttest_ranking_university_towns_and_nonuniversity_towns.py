import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

'''The first step is to clean the university towns data and create a dataframe of University towns'''
def univ_town():
    state = None  
    state_towns = [] #create a list of states
    #open the university_towns file
    with open('/Users/francescadimatteo/Desktop/university_towns.txt') as file:
        for line in file:
            #remove the space from the end line
            text = line[:-1]
            #each state ends with [edit], this is how it's possible to figure out which one is a state
            if text[-6:] == '[edit]':
                state = text[:-6]
                continue
            #some towns will have brackets, which needs to be removed to have a neat table
            if '(' in line:
                town = text[:text.index('(')-1]
                state_towns.append([state,town])
            else:
                town = text
                state_towns.append([state,town])
    #create the dataframe with the state and region, made by only neat names
    university_towns = pd.DataFrame(state_towns,columns= ['State','RegionName'])
    print(university_towns)
    
univ_town()  

#GDP table is needed to evaluate when the recession starts and ends after 2000, which will be needed to understand which towns will affected the most during recession
def gdp():
    #skip the firsts 7 rows, rename the columns with specific names
    GDP = (pd.read_excel('gdplev.xls',skiprows = 7').rename(columns={'Unnamed: 4':'Quarter','Unnamed: 5':'GDP','Unnamed: 6':'GDP2009'})
             .drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 7'],axis=1))
    #set Quarter as index
    GDP = GDP.set_index('Quarter')
    #drop all the quarters before 2000
    GDP = GDP.loc['2000q1':,:]
    print(GDP)
gdp()
           
def recession_start():
    '''Returns the year and quarter of the recession start time as a string value in a format such as 2005q3'''
    #In order to detect where the recession starts, we need to create a new column with the GDP difference between one quarter and the previous one
    #import data from gdplev file, drop first 4 columns and rename last columns
    GDP = gdp()
    #same GDP table, the values were shifted one unit down
    GDP_shift = GDP.shift(1)
    #Calculate the difference between GDP of two consecutive years
    GDP['Difference_of_GDP'] = GDP.iloc[:,1] - GDP_shift.iloc[:,1]
    
    recession_list = GDP['Difference_of_GDP'].tolist()
    recession_start = list()
    #Iterate through the list to find out whether there is recession or not. Recession is defined as a period starting with two consecutive periods of GDP decline
    for i in range(0,len(recession_list)):
        if recession_list[i] < 0 and recession_list[i+1]<0:
            recession_start.append(True)
        else:
            recession_start.append(False)

    GDP['recession'] = recession_start
    GDP_recession = GDP.where(GDP['recession'] == True).dropna()
    GDP_recession = GDP_recession.reset_index()
    print(GDP_recession['Quarter'][0])
get_recession_start() 
           
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a string value in a format such as 2005q3'''
    GDP = gdp()   #recall GDP table
    recession_start = get_recession_start()   #recall the recession_start calculated in the previous function
    GDP = GDP.set_index('Quarter')  #set Quarters as index
    GDP = GDP.loc[recession_start:,:]   #we need to evaluate from the start of the recession period
    GDP_shift = GDP.shift(1)
           
    GDP['Difference_of_GDP'] = GDP.iloc[:,1] - GDP_shift.iloc[:,1]  #evaluate the difference in GDPs
    
    recession_list = GDP['Difference_of_GDP'].tolist()
    recession_bottom = list()
    #recession_end is defined as a period having two consecutive periods of GDP growth after the decline
    for i in range(0,len(recession_list)):
        if (recession_list[i] > 0 and recession_list[i-1] > 0):
            recession_bottom.append(True)
        else:
            recession_bottom.append(False)

    GDP['recession'] = recession_bottom
    GDP_recession = GDP.where(GDP['recession'] == True).dropna()
    GDP_recession = GDP_recession.reset_index()
    
    print(GDP_recession['Quarter'][0])
get_recession_end()
           
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a string value in a format such as 2005q3'''
    GDP = gdp()
    #Recession bottom is the quarter within a recession that will have the minimum GDP
    recession_start = get_recession_start()
    recession_end = get_recession_end()
    GDP = GDP.set_index('Quarter')
    GDP = GDP.loc[recession_start:recession_end,:]  #we need to evaluate the bottom within the recession period
    recession_bottom = GDP['GDP'].min() #we need to know which is the lowest GDP evaluated
    GDP = GDP.where(GDP['GDP'] == recession_bottom).dropna()
    GDP = GDP.reset_index()
    
    print(GDP['Quarter'][0])
get_recession_bottom()

#The City_Zhvi_AllHomes file has the data for each non university town     
def convert_quarterly_data():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].'''
           
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 
          'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 
          'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 
          'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 
          'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 
          'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 
          'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 
          'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 
          'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 
          'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 
          'ND': 'North Dakota', 'VA': 'Virginia'}
           
    quarterly_data = (pd.readcsv('City_Zhvi_AllHomes.csv').drop(['RegionID','Metro','CountyName','SizeRank'],axis=1)
                        .sort_values(['State','RegionName'],ascending=[True,True]))
    quarterly_data['State'] = quarterly_data['State'].map(states)
    quarterly_data.set_index(['State','RegionName'],inplace=True)
    quarterly_data.drop(quarterly_data.columns[0:45],axis=1,inplace=True)                 
    quarterly_data = quarterly_data.groupby(pd.PeriodIndex(quarterly_data.columns,freq='Q'),axis=1).mean()
    print(quarterly_data)
    
convert_quarterly_data()
          
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. '''
    recession_start = get_recession_start()
    recession_end = get_recession_end()
    #Create a hd table with the data within the recession
    hd = convert_housing_data_to_quarters().loc[:,recession_start:recession_end]
    
    hd.columns =hd.columns.to_series().astype(str)
    hd = hd.reset_index().dropna()
    
    university_towns = get_list_of_university_towns()
    univtowns = university_towns['RegionName'].tolist()
    non_univtowns = hd['RegionName'].tolist()
    #check if the town is a university town or not
    hd['UnivTown'] = hd.RegionName.isin(univtowns)
    
    #get the column of mean values
    Univ = hd.where(hd['UnivTown'] == True).dropna().drop(['UnivTown'],axis=1)
    Univ['Mean'] = Univ.mean(axis=1)
    NotUniv = hd.where(hd['UnivTown'] == False).dropna().drop(['UnivTown'],axis=1)
    NotUniv['Mean'] = NotUniv.mean(axis=1)
    
    #get a mean of the column for each dataframe
    ValUniv = Univ['Mean'].mean()
    ValNotUniv = NotUniv['Mean'].mean()
    Univ = Univ['Mean']
    NotUniv = NotUniv['Mean']
    
    #compare to see what is better
    if ValUniv < ValNotUniv:
         better='university town'
    else:
         better='mon-university town'
    
    better
    #evaluate p
    p = list(ttest_ind(Univ, NotUniv))[1]
    
    if p<0.01:
        final = (True,p,better)
    else:
        final = (False,p,better)
    print(final)
run_ttest()
