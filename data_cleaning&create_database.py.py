import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

'''The first step is to clean the university towns data'''
def univ_town():
    state = None
    state_towns = []
    #open the university_towns file
    with open('/Users/francescadimatteo/Desktop/university_towns.txt') as file:
        for line in file:
            #remove the space from the end line
            text = line[:-1]
            #each state ends with [edit]
            if text[-6:] == '[edit]':
                state = text[:-6]
                continue
            #some towns will have brackets, which I need to remove to have a neat table
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

#GDP table is needed to evaluate when the recession starts and ends after 2000, which will be needed to understand which towns will have higher impact during recession
def gdp():
    GDP = (pd.read_excel('gdplev.xls',skiprows = 7').rename(columns={'Unnamed: 4':'Quarter','Unnamed: 5':'GDP','Unnamed: 6':'GDP2009'})
             .drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 7'],axis=1))
    #set Quarter as index
    GDP = GDP.set_index('Quarter')
    #drop all the quarters before 2000
    GDP = GDP.loc['2000q1':,:]
    print(GDP)
gdp()
           
def recession_start():
    
           

#The City_Zhvi_AllHomes file has the data for each non university town     
def convert_quarterly_data():
    quarterly_data = (pd.readcsv('City_Zhvi_AllHomes.csv').drop(['RegionID','Metro','CountyName','SizeRank'],axis=1)
                        .sort_values(['State','RegionName'],ascending=[True,True]))
    quarterly_data.set_index(['State','RegionName'],inplace=True)
    quarterly_data.drop(quarterly_data.columns[0:45],axis=1,inplace=True)                 
    quarterly_data = quarterly_data.groupby(pd.PeriodIndex(quarterly_data.columns,freq='Q'),axis=1).mean()
    print(quarterly_data)
    
convert_quarterly_data()
          
def run_ttest():
    hd = convert_housing_data_to_quarters().iloc[:,33:38]
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
    p = list(ttest_ind(Univ, NotUniv))[1]
    
    if p<0.01:
        final = (True,p,better)
    else:
        final = (False,p,better)
    print(final)
run_ttest()
           
