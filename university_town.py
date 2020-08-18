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
    
