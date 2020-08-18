import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

'''The first step is to clean the university towns data. In the txt file, there is a list
of Regions followed by all the towns, which are part of the Region.
Each Region ends with '[edit]'.'''
def univ_town():
    state = None
    state_towns = []
    with open('/Users/francescadimatteo/Desktop/university_towns.txt') as file:
        for line in file:
            text = line[:-1]
            if text[-6:] == '[edit]':
                state = text[:-6]
                continue
            if '(' in line:
                town = text[:text.index('(')-1]
                state_towns.append([state,town])
            else:
                town = text
                state_towns.append([state,town])
    university_towns = pd.DataFrame(state_towns,columns= ['State','RegionName'])
    return university_towns
