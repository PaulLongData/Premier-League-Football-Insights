# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:22:16 2023

@author: pauly
"""

import pandas as pd
from scipy.stats import ttest_ind #T Test Unpaired
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway 

#Note:
#When looking through the variable explorer, the insights are keyed with:
    # card - first insight
    # goal - second insight
    # bet - third insight
    # shots - fourth insight
#This may make it easier to find each variable in the folder.
#Also, at the end of this Python file, I deleted anything that wasn't necessary
# that was already contained elsewhere (ie., if I joined two dataframes into one, 
# I kept the copy and deleted the previous two.)
# Again, this was for ease of access, but anything that's cannot be found is at 
# the bottom of the file. 

football = pd.concat([pd.read_csv("C:/Users//Downloads/season-1617.csv"), 
                      pd.read_csv("C:/Users//Downloads/season-1718.csv"), 
                      pd.read_csv("C:/Users//Downloads/season-1819.csv")], 
                     ignore_index=True)

#______________________________________________________________________________
#Pre-Processing
print("__________________________________________________________\nPre-Processing\n")

#Rename each column for ease of use, as some were difficult to understand. 
football.rename(columns = {'HomeTeam':'Home Team'}, inplace = True) 
football.rename(columns = {'AwayTeam':'Away Team'}, inplace = True) 
football.rename(columns = {'FTHG':'Full Time Home Goals'}, inplace = True) 
football.rename(columns = {'FTAG':'Full Time Away Goals'}, inplace = True) 
football.rename(columns = {'HTHG':'Half Time Home Goals'}, inplace = True) 
football.rename(columns = {'HTAG':'Half Time Away Goals'}, inplace = True) 
football.rename(columns = {'FTR':'Full Time Winner'}, inplace = True) 
football.rename(columns = {'HTR':'Half Time Winner'}, inplace = True) 
football.rename(columns = {'HS':'Home Strikes'}, inplace = True) 
football.rename(columns = {'AS':'Away Strikes'}, inplace = True) 
football.rename(columns = {'HST':'Home Strikes on Target'}, inplace = True) 
football.rename(columns = {'AST':'Away Strikes on Target'}, inplace = True) 
football.rename(columns = {'HF':'Home Fouls'}, inplace = True) 
football.rename(columns = {'AF':'Away Fouls'}, inplace = True) 
football.rename(columns = {'HC':'Home Corners'}, inplace = True) 
football.rename(columns = {'AC':'Away Corners'}, inplace = True) 
football.rename(columns = {'HY':'Home Yellow Cards'}, inplace = True) 
football.rename(columns = {'AY':'Away Yellow Cards'}, inplace = True) 
football.rename(columns = {'HR':'Home Red Cards'}, inplace = True) 
football.rename(columns = {'AR':'Away Red Cards'}, inplace = True) 
football.rename(columns = {'B365H':'Bet365 Home Winner Odds'}, inplace = True) 
football.rename(columns = {'B365D':'Bet365 Draw Odds'}, inplace = True) 
football.rename(columns = {'B365A':'Bet365 Away Winner Odds'}, inplace = True) 
football.rename(columns = {'LBH':'Ladbrokes Home Winner Odds'}, inplace = True) 
football.rename(columns = {'LBD':'Ladbrokes Draw Odds'}, inplace = True) 
football.rename(columns = {'LBA':'Ladbrokes Away Winner Odds'}, inplace = True) 
football.rename(columns = {'WHH':'William Hill Home Winner Odds'}, inplace = True) 
football.rename(columns = {'WHD':'William Hill Draw Odds'}, inplace = True) 
football.rename(columns = {'WHA':'William Hill Away Winner Odds'}, inplace = True) 
football.rename(columns = {'BWH':'Betway Home Winner Odds'}, inplace = True) 
football.rename(columns = {'BWD':'Betway Draw Odds'}, inplace = True) 
football.rename(columns = {'BWA':'Betway Away Winner Odds'}, inplace = True) 
football.rename(columns = {'PSH':'Poker Stars Home Winner Odds'}, inplace = True) 
football.rename(columns = {'PSD':'Poker Stars Draw Odds'}, inplace = True) 
football.rename(columns = {'PSA':'Poker Stars Away Winner Odds'}, inplace = True) 
football.rename(columns = {'IWH':'Interwetten Home Winner Odds'}, inplace = True) 
football.rename(columns = {'IWD':'Interwetten Draw Odds'}, inplace = True) 
football.rename(columns = {'IWA':'Interwetten Away Winner Odds'}, inplace = True) 

#Delete Extraneous Betting Data
football.drop('Date', axis = 'columns', inplace = True)
football.drop('Referee', axis = 'columns', inplace = True)
football.drop('Div', axis = 'columns', inplace = True)
football.drop('VCH', axis = 'columns', inplace = True)
football.drop('VCD', axis = 'columns', inplace = True)
football.drop('VCA', axis = 'columns', inplace = True)
football.drop('PSCH', axis = 'columns', inplace = True)
football.drop('PSCD', axis = 'columns', inplace = True)
football.drop('PSCA', axis = 'columns', inplace = True)
football.drop('Bb1X2', axis = 'columns', inplace = True)
football.drop('BbMxH', axis = 'columns', inplace = True)
football.drop('BbAvH', axis = 'columns', inplace = True)
football.drop('BbMxD', axis = 'columns', inplace = True)
football.drop('BbAvD', axis = 'columns', inplace = True)
football.drop('BbMxA', axis = 'columns', inplace = True)
football.drop('BbAvA', axis = 'columns', inplace = True)
football.drop('BbOU', axis = 'columns', inplace = True)
football.drop('BbMx>2.5', axis = 'columns', inplace = True)
football.drop('BbAv>2.5', axis = 'columns', inplace = True)
football.drop('BbMx<2.5', axis = 'columns', inplace = True)
football.drop('BbAv<2.5', axis = 'columns', inplace = True)
football.drop('BbAH', axis = 'columns', inplace = True)
football.drop('BbAHh', axis = 'columns', inplace = True)
football.drop('BbMxAHH', axis = 'columns', inplace = True)
football.drop('BbAvAHH', axis = 'columns', inplace = True)
football.drop('BbMxAHA', axis = 'columns', inplace = True)
football.drop('BbAvAHA', axis = 'columns', inplace = True)


#______________________________________________________________________________
#Insight 1
print("__________________________________________________________\nInsight 1\n")

print("The goal for the first insight is to investigate how impactful", 
      " being at home vs being away is, when receiving a red card. ",
      "\nI also calculated the proportion of home to away red cards. ")

#Create a temporary dataframe which adds all the home red cards and all the away 
# red cards, to reference against later. 
card_Red_Total = pd.DataFrame({'Total Red Cards': football['Away Red Cards'] + football['Home Red Cards']})

#This told me the maximum red cards in each game.  
print("The most red cards in one game was:", card_Red_Total.max()[0])

card_football = pd.concat([football, card_Red_Total.reindex(football.index)], axis=1)

card_1_Red = card_football.loc[card_football['Total Red Cards']==1]
#Factor out if both teams have had a red card to ensure we only look at 
# imbalanaced games
card_2_Red = card_football.loc[card_football['Total Red Cards']==2]
#It's only necessary to look at when home teams aren't = 1, as it necessitates
# home teams having 0 or 2, meaning the same for away teams. 
card_2_Red_1_Team= card_2_Red.loc[card_2_Red['Home Red Cards']!=1]

#Get a list of total games where one team ended the game with more players than the other
card_Red = pd.concat([card_1_Red, card_2_Red_1_Team])

#This gave me a list games where teams had one or omre players sent off. 
#This was a resource I used here :https://www.dataquest.io/blog/settingwithcopywarning/
card_Red_Home = card_Red.loc[card_Red['Home Red Cards']>=1].copy()
card_Red_Away = card_Red.loc[card_Red['Away Red Cards']>=1].copy()

#Change the Results to Integers, to facilitate T Test
card_Red_Home['Full Time Winner'] = card_Red_Home['Full Time Winner'].replace(['Full Time Winner','D'], 0)
card_Red_Home['Full Time Winner'] = card_Red_Home['Full Time Winner'].replace(['Full Time Winner','H'], 1)
card_Red_Home['Full Time Winner'] = card_Red_Home['Full Time Winner'].replace(['Full Time Winner','A'], -1)
card_Red_Away['Full Time Winner'] = card_Red_Away['Full Time Winner'].replace(['Full Time Winner','D'], 0)
card_Red_Away['Full Time Winner'] = card_Red_Away['Full Time Winner'].replace(['Full Time Winner','H'], -1)
card_Red_Away['Full Time Winner'] = card_Red_Away['Full Time Winner'].replace(['Full Time Winner','A'], 1)

#Conduct T Test. 

#Null and Alternative Hypothesis.
print("\nRed Card Test Null Hypothesis: There is no difference between the", 
      " means of when an away team and a home team lose a player.", 
      "\nRed Card Test Alternative Hypothesis: There is a difference",
      " between the means of when an away team and a home team lose a player.",
      "\n\nWe Will Use a Two Sided T Test, with a confidence interval of 5%.")
#Compute T Test Values
card_t_test_t_value, card_t_test_p_value = ttest_ind(card_Red_Home['Full Time Winner'], card_Red_Away['Full Time Winner'])
print("\nt value for the Red Card T Test: " + str(card_t_test_t_value))
print("\np value for the Red Card T Test: " + str(card_t_test_p_value))
#If else condition for if p value meets condition. 
if card_t_test_p_value <0.05:
    print("P value meets the threshold. \nTherefore, we reject",
          "the null hypothesis.",
          "\nThus, it appears that there is no difference between the",
          " average results of when an away team and a home team lose a player. ")    
else: 
    print("P value does not meet the threshold. Therefore, we fail to",
          "reject the null hypothesis",
          "\nThus, it appears that there is a difference between the",
          " average results of when an away team and a home team lose a player. ")


#______________________________________________________________________________
#Insight 2
print("__________________________________________________________\nInsight 2\n")

print("The goal for the second insight is to investigate the goals scored", 
      " after half time vs the goals after full time for the big six clubs,",
      " using scatter plots and linear regression. ")

#Create a function for swapping columns
#https://www.statology.org/swap-columns-pandas/
def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df


#Liverpool
#This involved seperating out the games Liverpool played, both home and away. 
goal_LiverpoolGamesHome = football.loc[football['Home Team']=='Liverpool']
goal_LiverpoolGamesAwayTemp = football.loc[football['Away Team']=='Liverpool']

#This involved swapping the various different columns so that I could have one
# column full of only Liverpool games. I put all their games into the 'Home' 
# column. 
goal_LiverpoolGamesAwayTemp = swap_columns(goal_LiverpoolGamesAwayTemp, 'Home Team', 'Away Team')
goal_LiverpoolGamesAwayTemp.rename(columns = {'Home Team':'HomeTeam'}, inplace = True) 
goal_LiverpoolGamesAwayTemp.rename(columns = {'Away Team':'Home Team'}, inplace = True) 
goal_LiverpoolGamesAwayTemp.rename(columns = {'HomeTeam':'Away Team'}, inplace = True) 

goal_LiverpoolGamesAwayTemp = swap_columns(goal_LiverpoolGamesAwayTemp, 'Full Time Home Goals', 'Full Time Away Goals')
goal_LiverpoolGamesAwayTemp.rename(columns = {'Full Time Home Goals':'Full Time Home Goal'}, inplace = True) 
goal_LiverpoolGamesAwayTemp.rename(columns = {'Full Time Away Goals':'Full Time Home Goals'}, inplace = True) 
goal_LiverpoolGamesAwayTemp.rename(columns = {'Full Time Home Goal':'Full Time Away Goals'}, inplace = True) 

goal_LiverpoolGamesAwayTemp = swap_columns(goal_LiverpoolGamesAwayTemp, 'Half Time Home Goals', 'Half Time Away Goals')
goal_LiverpoolGamesAwayTemp.rename(columns = {'Half Time Home Goals':'Half Time Home Goal'}, inplace = True) 
goal_LiverpoolGamesAwayTemp.rename(columns = {'Half Time Away Goals':'Half Time Home Goals'}, inplace = True) 
goal_LiverpoolGamesAwayTemp.rename(columns = {'Half Time Home Goal':'Half Time Away Goals'}, inplace = True) 

goal_LiverpoolGamesHT = pd.concat([goal_LiverpoolGamesHome, goal_LiverpoolGamesAwayTemp])

#Getting the various different elements for the linear regression
goal_li_slope, goal_li_intercept, goal_li_r_value, goal_li_p_value, goal_li_std_error = stats.linregress(goal_LiverpoolGamesHome['Half Time Home Goals'], goal_LiverpoolGamesHome['Full Time Home Goals'])
def goal_li_regression(x):
    return goal_li_slope * x + goal_li_intercept
#Plotting the linear regression map
goal_li_model = list(map(goal_li_regression, goal_LiverpoolGamesHT['Half Time Home Goals']))

#Creating a Scatter plot of goals scored at half time and goals scored at full time, that we can lay the linear regression over. 
plt.scatter(goal_LiverpoolGamesHT['Half Time Home Goals'], goal_LiverpoolGamesHT['Full Time Home Goals'])
plt.title("Liverpool Goals Half Time vs. Full Time")
plt.xlabel("Half Time")
plt.ylabel("Full Time")
plt.plot(goal_LiverpoolGamesHT['Half Time Home Goals'], goal_li_model)
plt.show()


#Man United
goal_ManUnitedGamesHome = football.loc[football['Home Team']=='Man United']
goal_ManUnitedGamesAwayTemp = football.loc[football['Away Team']=='Man United']

goal_ManUnitedGamesAwayTemp = swap_columns(goal_ManUnitedGamesAwayTemp, 'Home Team', 'Away Team')
goal_ManUnitedGamesAwayTemp.rename(columns = {'Home Team':'HomeTeam'}, inplace = True) 
goal_ManUnitedGamesAwayTemp.rename(columns = {'Away Team':'Home Team'}, inplace = True) 
goal_ManUnitedGamesAwayTemp.rename(columns = {'HomeTeam':'Away Team'}, inplace = True) 

goal_ManUnitedGamesAwayTemp = swap_columns(goal_ManUnitedGamesAwayTemp, 'Full Time Home Goals', 'Full Time Away Goals')
goal_ManUnitedGamesAwayTemp.rename(columns = {'Full Time Home Goals':'Full Time Home Goal'}, inplace = True) 
goal_ManUnitedGamesAwayTemp.rename(columns = {'Full Time Away Goals':'Full Time Home Goals'}, inplace = True) 
goal_ManUnitedGamesAwayTemp.rename(columns = {'Full Time Home Goal':'Full Time Away Goals'}, inplace = True) 

goal_ManUnitedGamesAwayTemp = swap_columns(goal_ManUnitedGamesAwayTemp, 'Half Time Home Goals', 'Half Time Away Goals')
goal_ManUnitedGamesAwayTemp.rename(columns = {'Half Time Home Goals':'Half Time Home Goal'}, inplace = True) 
goal_ManUnitedGamesAwayTemp.rename(columns = {'Half Time Away Goals':'Half Time Home Goals'}, inplace = True) 
goal_ManUnitedGamesAwayTemp.rename(columns = {'Half Time Home Goal':'Half Time Away Goals'}, inplace = True) 

goal_ManUnitedGamesHT = pd.concat([goal_ManUnitedGamesHome, goal_ManUnitedGamesAwayTemp])

goal_mu_slope, goal_mu_intercept, goal_mu_r_value, goal_mu_p_value, goal_mu_std_error = stats.linregress(goal_ManUnitedGamesHome['Half Time Home Goals'], goal_ManUnitedGamesHome['Full Time Home Goals'])
def goal_mu_regression(x):
    return goal_mu_slope * x + goal_mu_intercept
goal_mu_model = list(map(goal_mu_regression, goal_ManUnitedGamesHT['Half Time Home Goals']))

plt.scatter(goal_ManUnitedGamesHT['Half Time Home Goals'], goal_ManUnitedGamesHT['Full Time Home Goals'])
plt.title("Man United Goals Half Time vs. Full Time")
plt.xlabel("Half Time")
plt.ylabel("Full Time")
plt.plot(goal_ManUnitedGamesHT['Half Time Home Goals'], goal_mu_model)
plt.show()


#Man City
goal_ManCityGamesHome = football.loc[football['Home Team']=='Man City']
goal_ManCityGamesAwayTemp = football.loc[football['Away Team']=='Man City']

goal_ManCityGamesAwayTemp = swap_columns(goal_ManCityGamesAwayTemp, 'Home Team', 'Away Team')
goal_ManCityGamesAwayTemp.rename(columns = {'Home Team':'HomeTeam'}, inplace = True) 
goal_ManCityGamesAwayTemp.rename(columns = {'Away Team':'Home Team'}, inplace = True) 
goal_ManCityGamesAwayTemp.rename(columns = {'HomeTeam':'Away Team'}, inplace = True) 

goal_ManCityGamesAwayTemp = swap_columns(goal_ManCityGamesAwayTemp, 'Full Time Home Goals', 'Full Time Away Goals')
goal_ManCityGamesAwayTemp.rename(columns = {'Full Time Home Goals':'Full Time Home Goal'}, inplace = True) 
goal_ManCityGamesAwayTemp.rename(columns = {'Full Time Away Goals':'Full Time Home Goals'}, inplace = True) 
goal_ManCityGamesAwayTemp.rename(columns = {'Full Time Home Goal':'Full Time Away Goals'}, inplace = True) 

goal_ManCityGamesAwayTemp = swap_columns(goal_ManCityGamesAwayTemp, 'Half Time Home Goals', 'Half Time Away Goals')
goal_ManCityGamesAwayTemp.rename(columns = {'Half Time Home Goals':'Half Time Home Goal'}, inplace = True) 
goal_ManCityGamesAwayTemp.rename(columns = {'Half Time Away Goals':'Half Time Home Goals'}, inplace = True) 
goal_ManCityGamesAwayTemp.rename(columns = {'Half Time Home Goal':'Half Time Away Goals'}, inplace = True) 

goal_ManCityGamesHT = pd.concat([goal_ManCityGamesHome, goal_ManCityGamesAwayTemp])

goal_mc_slope, goal_mc_intercept, goal_mc_r_value, goal_mc_p_value, goal_mc_std_error = stats.linregress(goal_ManCityGamesHome['Half Time Home Goals'], goal_ManCityGamesHome['Full Time Home Goals'])
def goal_mc_regression(x):
    return goal_mc_slope * x + goal_mc_intercept
goal_mc_model = list(map(goal_mc_regression, goal_ManCityGamesHT['Half Time Home Goals']))

plt.scatter(goal_ManCityGamesHT['Half Time Home Goals'], goal_ManCityGamesHT['Full Time Home Goals'])
plt.title("Man City Goals Half Time vs. Full Time")
plt.xlabel("Half Time")
plt.ylabel("Full Time")
plt.plot(goal_ManCityGamesHT['Half Time Home Goals'], goal_mc_model)
plt.show()


#Chelsea
goal_ChelseaGamesHome = football.loc[football['Home Team']=='Chelsea']
goal_ChelseaGamesAwayTemp = football.loc[football['Away Team']=='Chelsea']

goal_ChelseaGamesAwayTemp = swap_columns(goal_ChelseaGamesAwayTemp, 'Home Team', 'Away Team')
goal_ChelseaGamesAwayTemp.rename(columns = {'Home Team':'HomeTeam'}, inplace = True) 
goal_ChelseaGamesAwayTemp.rename(columns = {'Away Team':'Home Team'}, inplace = True) 
goal_ChelseaGamesAwayTemp.rename(columns = {'HomeTeam':'Away Team'}, inplace = True) 

goal_ChelseaGamesAwayTemp = swap_columns(goal_ChelseaGamesAwayTemp, 'Full Time Home Goals', 'Full Time Away Goals')
goal_ChelseaGamesAwayTemp.rename(columns = {'Full Time Home Goals':'Full Time Home Goal'}, inplace = True) 
goal_ChelseaGamesAwayTemp.rename(columns = {'Full Time Away Goals':'Full Time Home Goals'}, inplace = True) 
goal_ChelseaGamesAwayTemp.rename(columns = {'Full Time Home Goal':'Full Time Away Goals'}, inplace = True) 

goal_ChelseaGamesAwayTemp = swap_columns(goal_ChelseaGamesAwayTemp, 'Half Time Home Goals', 'Half Time Away Goals')
goal_ChelseaGamesAwayTemp.rename(columns = {'Half Time Home Goals':'Half Time Home Goal'}, inplace = True) 
goal_ChelseaGamesAwayTemp.rename(columns = {'Half Time Away Goals':'Half Time Home Goals'}, inplace = True) 
goal_ChelseaGamesAwayTemp.rename(columns = {'Half Time Home Goal':'Half Time Away Goals'}, inplace = True) 

goal_ChelseaGamesHT = pd.concat([goal_ChelseaGamesHome, goal_ChelseaGamesAwayTemp])

goal_ch_slope, goal_ch_intercept, goal_ch_r_value, goal_ch_p_value, goal_ch_std_error = stats.linregress(goal_ChelseaGamesHT['Half Time Home Goals'], goal_ChelseaGamesHT['Full Time Home Goals'])
def goal_ch_regression(x):
    return goal_ch_slope * x + goal_ch_intercept
goal_ch_model = list(map(goal_ch_regression, goal_ChelseaGamesHT['Half Time Home Goals']))
plt.scatter(goal_ChelseaGamesHT['Half Time Home Goals'], goal_ChelseaGamesHT['Full Time Home Goals'])
plt.title(" Chelsea Goals Half Time vs. Full Time")
plt.xlabel("Half Time")
plt.ylabel("Full Time")
plt.plot(goal_ChelseaGamesHT['Half Time Home Goals'], goal_ch_model)
plt.show()


#Arsenal
goal_ArsenalGamesHome = football.loc[football['Home Team']=='Arsenal']
goal_ArsenalGamesAwayTemp = football.loc[football['Away Team']=='Arsenal']

goal_ArsenalGamesAwayTemp = swap_columns(goal_ArsenalGamesAwayTemp, 'Home Team', 'Away Team')
goal_ArsenalGamesAwayTemp.rename(columns = {'Home Team':'HomeTeam'}, inplace = True) 
goal_ArsenalGamesAwayTemp.rename(columns = {'Away Team':'Home Team'}, inplace = True) 
goal_ArsenalGamesAwayTemp.rename(columns = {'HomeTeam':'Away Team'}, inplace = True) 

goal_ArsenalGamesAwayTemp = swap_columns(goal_ArsenalGamesAwayTemp, 'Full Time Home Goals', 'Full Time Away Goals')
goal_ArsenalGamesAwayTemp.rename(columns = {'Full Time Home Goals':'Full Time Home Goal'}, inplace = True) 
goal_ArsenalGamesAwayTemp.rename(columns = {'Full Time Away Goals':'Full Time Home Goals'}, inplace = True) 
goal_ArsenalGamesAwayTemp.rename(columns = {'Full Time Home Goal':'Full Time Away Goals'}, inplace = True) 

goal_ArsenalGamesAwayTemp = swap_columns(goal_ArsenalGamesAwayTemp, 'Half Time Home Goals', 'Half Time Away Goals')
goal_ArsenalGamesAwayTemp.rename(columns = {'Half Time Home Goals':'Half Time Home Goal'}, inplace = True) 
goal_ArsenalGamesAwayTemp.rename(columns = {'Half Time Away Goals':'Half Time Home Goals'}, inplace = True) 
goal_ArsenalGamesAwayTemp.rename(columns = {'Half Time Home Goal':'Half Time Away Goals'}, inplace = True) 

goal_ArsenalGamesHT = pd.concat([goal_ArsenalGamesHome, goal_ArsenalGamesAwayTemp])

goal_ar_slope, goal_ar_intercept, goal_ar_r_value, goal_ar_p_value, goal_ar_std_error = stats.linregress(goal_ArsenalGamesHT['Half Time Home Goals'], goal_ArsenalGamesHT['Full Time Home Goals'])
def goal_ar_regression(x):
    return goal_ar_slope * x + goal_ar_intercept
goal_ar_model = list(map(goal_ar_regression, goal_ArsenalGamesHT['Half Time Home Goals']))
plt.scatter(goal_ArsenalGamesHT['Half Time Home Goals'], goal_ArsenalGamesHT['Full Time Home Goals'])
plt.title(" Arsenal Goals Half Time vs. Full Time")
plt.xlabel("Half Time")
plt.ylabel("Full Time")
plt.plot(goal_ArsenalGamesHT['Half Time Home Goals'], goal_ar_model)
plt.show()


#Tottenham
goal_TottenhamGamesHome = football.loc[football['Home Team']=='Tottenham']
goal_TottenhamGamesAwayTemp = football.loc[football['Away Team']=='Tottenham']

goal_TottenhamGamesAwayTemp = swap_columns(goal_TottenhamGamesAwayTemp, 'Home Team', 'Away Team')
goal_TottenhamGamesAwayTemp.rename(columns = {'Home Team':'HomeTeam'}, inplace = True) 
goal_TottenhamGamesAwayTemp.rename(columns = {'Away Team':'Home Team'}, inplace = True) 
goal_TottenhamGamesAwayTemp.rename(columns = {'HomeTeam':'Away Team'}, inplace = True) 

goal_TottenhamGamesAwayTemp = swap_columns(goal_TottenhamGamesAwayTemp, 'Full Time Home Goals', 'Full Time Away Goals')
goal_TottenhamGamesAwayTemp.rename(columns = {'Full Time Home Goals':'Full Time Home Goal'}, inplace = True) 
goal_TottenhamGamesAwayTemp.rename(columns = {'Full Time Away Goals':'Full Time Home Goals'}, inplace = True) 
goal_TottenhamGamesAwayTemp.rename(columns = {'Full Time Home Goal':'Full Time Away Goals'}, inplace = True) 

goal_TottenhamGamesAwayTemp = swap_columns(goal_TottenhamGamesAwayTemp, 'Half Time Home Goals', 'Half Time Away Goals')
goal_TottenhamGamesAwayTemp.rename(columns = {'Half Time Home Goals':'Half Time Home Goal'}, inplace = True) 
goal_TottenhamGamesAwayTemp.rename(columns = {'Half Time Away Goals':'Half Time Home Goals'}, inplace = True) 
goal_TottenhamGamesAwayTemp.rename(columns = {'Half Time Home Goal':'Half Time Away Goals'}, inplace = True) 

goal_TottenhamGamesHT = pd.concat([goal_TottenhamGamesHome, goal_TottenhamGamesAwayTemp])

goal_tt_slope, goal_tt_intercept, goal_tt_r_value, goal_tt_p_value, goal_tt_std_error = stats.linregress(goal_TottenhamGamesHT['Half Time Home Goals'], goal_TottenhamGamesHT['Full Time Home Goals'])
def goal_tt_regression(x):
    return goal_tt_slope * x + goal_tt_intercept
goal_tt_model = list(map(goal_tt_regression, goal_TottenhamGamesHT['Half Time Home Goals']))
plt.scatter(goal_TottenhamGamesHT['Half Time Home Goals'], goal_TottenhamGamesHT['Full Time Home Goals'])
plt.title(" Tottenham Goals Half Time vs. Full Time")
plt.xlabel("Half Time")
plt.ylabel("Full Time")
plt.plot(goal_TottenhamGamesHT['Half Time Home Goals'], goal_tt_model)
plt.show()

#Put them all into one graph. 
plt.plot(goal_LiverpoolGamesHT['Half Time Home Goals'], goal_li_model, color='red', label='Liverpool') 
plt.plot(goal_ManCityGamesHT['Half Time Home Goals'], goal_mc_model, color='paleturquoise', label='Man City') 
plt.plot(goal_ManUnitedGamesHT['Half Time Home Goals'], goal_mu_model, color='orange', label='Man United') 
plt.plot(goal_ChelseaGamesHT['Half Time Home Goals'], goal_ch_model, color='blue', label='Chelsea') 
plt.plot(goal_ArsenalGamesHT['Half Time Home Goals'], goal_ar_model, color='pink', label='Arsenal') 
plt.plot(goal_TottenhamGamesHT['Half Time Home Goals'], goal_tt_model, color='navy', label='Tottenham') 
plt.legend(fontsize=13,loc='upper left')
plt.show()

#Print conclusions from results.
print(
      "From this, we can deduce that Man City are the team likely to score the",
      " most goals in the second half, regardless of the first half.",
      "\nThey are also the most likely to score in the first half. ",
      "\n\nThen, Liverpool are a close second.", 
      "\n\nChelsea seems to score fewer goals when there are no goals scored",
      "in the first half when compared to Man United, & Arsenal, but they ",
      "comfortably take the lead once there have been two or more goals scored.",
      "This would seem to suggest that Chelse are a team that are more impacted",
      "ny momentum. ",
      "\n\nIt's also worth noting that Chelsea are the only big 6 team",
      "to not score 4 goals in the first half at any point in the season."
      )


#______________________________________________________________________________
#Insight 3
print("__________________________________________________________\nInsight 3\n")

print("The goal for the third insight is to investigate the commonality in the odds",
      " being given by various different betting agencies, by using ANOVA test & t Test.",
      "\nThere was an issue here in that Ladbrokes didn't have data for the 18/19 season.",
      "\nIt felt inappropriate to try to impune the data, given how much was",
      " missing. \nI chose instead to only focus on the 16/17 and 17/18 seasons. \n\n")

#Get rid of the 18/19 season. 
bet_football = football.copy()
bet_football = bet_football.drop(range(760,1140))

#Create the correlation variables for Home Win, Draw and Away Win Odds. 
bet_corr_H = football[['Bet365 Home Winner Odds', 
                       'William Hill Home Winner Odds', 
                       'Ladbrokes Home Winner Odds', 
                       'Betway Home Winner Odds', 
                       'Interwetten Home Winner Odds', 
                       'Poker Stars Home Winner Odds']].corr()
bet_corr_D = football[['Bet365 Draw Odds', 
                       'William Hill Draw Odds', 
                       'Ladbrokes Draw Odds', 
                       'Betway Draw Odds', 
                       'Interwetten Draw Odds', 
                       'Poker Stars Draw Odds']].corr()
bet_corr_A = football[['Bet365 Away Winner Odds', 
                       'William Hill Away Winner Odds', 
                       'Ladbrokes Away Winner Odds', 
                       'Betway Away Winner Odds', 
                       'Interwetten Away Winner Odds', 
                       'Poker Stars Away Winner Odds']].corr()
bet_corr_fig1, bet_ax1 = plt.subplots(figsize=(12,10)) 
bet_corr_fig2, bet_ax2 = plt.subplots(figsize=(12,10)) 
bet_corr_fig3, bet_ax3 = plt.subplots(figsize=(12,10)) 


#Plot the correlations using seaborn heatmap 
sns.heatmap(bet_corr_H, cmap="hot", ax=bet_ax1, annot=True, cbar=False)
sns.heatmap(bet_corr_D, cmap="hot", ax=bet_ax2, annot=True, cbar=False)
sns.heatmap(bet_corr_A, cmap="hot", ax=bet_ax3, annot=True, cbar=False)
sns.set(font_scale=2)
plt.show()

print("As we can see, these have an extremely close correllation across the board.",
      "\nThis makes sense as they all use professionals to predict the outcomes. ")

#Complete the ANOVA Tests to see if there is a significant difference between
# the odds offered by each bookie. 

#Home
bet_home_f_value, bet_home_p_value = f_oneway(bet_football['Bet365 Home Winner Odds'], 
                                              bet_football['William Hill Home Winner Odds'], 
                                              bet_football['Ladbrokes Home Winner Odds'], 
                                              bet_football['Poker Stars Home Winner Odds'],
                                              bet_football['Interwetten Home Winner Odds'], 
                                              bet_football['Betway Home Winner Odds'])
print("Bet Win F-score: " + str(bet_home_f_value))
print("Bet Win p value: " + str(bet_home_p_value))
if bet_home_p_value < 0.05:
    print("Bet Home p value meets the threshold. Therefore, we reject the",
          " null hypothesis")    
else: 
    print("Bet Home p value does not meet the threshold. Therefore, we fail",
          " to reject the null hypothesis")

#Draw
bet_draw_f_value, bet_draw_p_value = f_oneway(bet_football['Bet365 Draw Odds'], 
                                              bet_football['William Hill Draw Odds'], 
                                              bet_football['Ladbrokes Draw Odds'], 
                                              bet_football['Poker Stars Draw Odds'], 
                                              bet_football['Interwetten Draw Odds'], 
                                              bet_football['Betway Draw Odds'])
print("\nBet Draw F-score: " + str(bet_draw_f_value))
print("Bet Draw p value: " + str(bet_draw_p_value))
if bet_draw_p_value < 0.05:
    print("Bet Draw p value meets the threshold. Therefore, we reject the",
          " null hypothesis")    
else: 
    print("Bet Draw p value does not meet the threshold. Therefore, we fail",
          " to reject the null hypothesis")

#Away
bet_away_f_value, bet_away_p_value = f_oneway(bet_football['Bet365 Away Winner Odds'], 
                                              bet_football['William Hill Away Winner Odds'], 
                                              bet_football['Ladbrokes Away Winner Odds'], 
                                              bet_football['Poker Stars Away Winner Odds'], 
                                              bet_football['Interwetten Away Winner Odds'], 
                                              bet_football['Betway Away Winner Odds'])
print("\nBet Away F-score: " + str(bet_away_f_value))
print("Bet Away p value: " + str(bet_away_p_value))
if bet_away_p_value < 0.05:
    print("Bet Away p value meets the threshold. Therefore, we reject the ",
          "null hypothesis")    
else: 
    print("Bet Away p value does not meet the threshold. Therefore, we fail",
          " to reject the null hypothesis")

print("\nFrom this analysis, we can see that there is a significant difference",
      " in the means between the bettings odds for draws and away wins. ",
      "\n\nWe can also see that there is no significant difference ",
      "betwen the means for the Home wins.",
      "\n\nThus, we can see that there is much more consensus on the likelihood ",
      "of home winners vs away winners.\n ")

#______________________________________________________________________________
#Insight 4
print("__________________________________________________________\nInsight 4\n")

print("The goal for the fourth insight is to investigate the different",
      " statistics emerging from shots taken per game."
      "\n\nI briefly looked at shots on target vs off target while",
      " home and away, to see if there was anything significant. ",
      "\n\nI also looked at the correlation between corner kicks and shots on target",
      " not scored. "
      "\n\nFinally, I looked at the proportion of corner kicks coming as a result of",
      " shots on target not scored. ")

#Create empty lists to seperate out shots not on target at home and away. 
shots_NOTH = []
shots_NOTA = []

#Fill these up with the necessary data. 
for i in range(0, len(football['Home Strikes on Target'])):    
    OT = football['Home Strikes'][i] - football['Home Strikes on Target'][i]
    shots_NOTH.append(OT) 
    
for i in range(0,len(football['Away Strikes on Target'])):    
    OT = football['Away Strikes'][i] - football['Away Strikes on Target'][i]
    shots_NOTA.append(OT)

#Turn the lists into dataframes. 
shots_NOTH = pd.DataFrame(shots_NOTH)
shots_NOTA = pd.DataFrame(shots_NOTA)

#I used this as a resource here: https://www.kdnuggets.com/2022/11/4-ways-rename-pandas-columns.html
#Rename the columns. 
shots_NOTH.set_axis(['Home'], axis='columns', inplace=True)
shots_NOTA.set_axis(['Away'], axis='columns', inplace=True)

#Concat these into one dataframe for ease of graphing. 
shots_NOT = pd.concat([shots_NOTH['Home'], shots_NOTA['Away']], axis=1)

#Graph violin plots of home on target, home not on target, away on target and away not on target. 
#
#Try as I could, I couldn't get a manual label to give me this information on
# the plot. I had to do it manually via the text file. 
#This is the resource I used, but I couldn't do it successfully: 
#https://stackoverflow.com/questions/33864578/matplotlib-making-labels-for-violin-plots
plt.violinplot(football[['Home Strikes on Target', 'Away Strikes on Target']], showmeans=True, showmedians=True, showextrema=True)
plt.violinplot(shots_NOT[['Home', 'Away']], showmeans=True, showmedians=True, showextrema=True)
plt.title("Violin Plot of Home vs Away Strikes \non Target vs Off Target")
plt.xticks([1, 2], ['Home', 'Away'])
plt.text(1.25, 13, 'On Target=Blue\nOff Target=Orange', fontsize=15)
plt.show()

#Print Conclusions from the graph. 
print("As we can see from the plot, the home teams seem to take",
      " slightly more shots than away teams, both on target and off target.",
      "This would indicate that there is a slight advantage towards the home sides")

#Create empty lists for home and away shots on target not scored.
shots_OTNSH = []
shots_OTNSA = []

#Fill these up with the necessary data. 
i=0
while i < len(football['Home Strikes on Target']):
    OTNSH = football['Home Strikes on Target'][i]-football['Full Time Home Goals'][i]
    shots_OTNSH.append(OTNSH)
    i += 1
j=0
while j < len(football['Away Strikes on Target']):
    OTNSA = football['Away Strikes on Target'][j]-football['Full Time Away Goals'][j]
    shots_OTNSA.append(OTNSA)
    j += 1

#Turn the lists into dataframes. 
shots_OTNSH = pd.DataFrame(shots_OTNSH)
shots_OTNSA = pd.DataFrame(shots_OTNSA)

#Rename the columns. 
shots_OTNSH.set_axis(['Home Shots'], axis='columns', inplace=True)
shots_OTNSA.set_axis(['Away Shots'], axis='columns', inplace=True)

#Concat these into one dataframe for ease of graphing. 
shots_OTNS = pd.concat([shots_OTNSH['Home Shots'], shots_OTNSA['Away Shots']], axis=1)
#Create a dataframe consisting of home and away corners
shots_Corners = pd.concat([football['Home Corners'], football['Away Corners']], axis=1)
#Merge these two dataframes into one dataframe for ease of computing correlation. 
shots_OTNS_Corners = pd.concat([shots_OTNS, shots_Corners], axis=1)
#Swap columns around, for ease of correlation. 
shots_OTNS_Corners = swap_columns(shots_OTNS_Corners, 'Home Corners', 'Away Shots')

#Compute correllation of all 4 vs 4, the 2 Home Columns, and the 2 Away Columns. 
shots_corr_total = shots_OTNS_Corners.corr()
shots_corr_home = shots_OTNS_Corners[['Home Shots', 'Home Corners']].corr()
shots_corr_away = shots_OTNS_Corners[['Away Shots', 'Away Corners']].corr()

print(shots_corr_total)
print(shots_corr_home)
print(shots_corr_away)

#Print Conclusions. 
print("\nAs we can see, this is quite a low correlation coefficients - 0.41",
      " at home and 0.32 when away.")

#Create empty variables to compute total number of shots on target not scored
# across the three seasons. 
shots_OTNSH_Sum = 0
shots_OTNSA_Sum = 0
shots_OTNSH_Corners_Sum = 0
shots_OTNSA_Corners_Sum = 0

#For each value, add that to it's corresponding variable created previously. 
for i in range(0, len(shots_OTNS_Corners['Home Shots'])):
    shots_OTNSH_Sum += shots_OTNS_Corners['Home Shots'][i]

for i in range(0, len(shots_OTNS_Corners['Away Shots'])):
    shots_OTNSA_Sum += shots_OTNS_Corners['Away Shots'][i]

for i in range(0, len(shots_OTNS_Corners['Home Corners'])):
    shots_OTNSH_Corners_Sum += shots_OTNS_Corners['Home Corners'][i]

for i in range(0, len(shots_OTNS_Corners['Home Corners'])):
    shots_OTNSA_Corners_Sum += shots_OTNS_Corners['Away Corners'][i]

#Add up total shots on target not scored. 
shots_OTNS_Total = shots_OTNSH_Sum + shots_OTNSA_Sum
#Add up total corners. 
shots_OTNS_Corner_Total = shots_OTNSH_Corners_Sum + shots_OTNSA_Corners_Sum 
#Divide them both to get the proportion. 
shots_OTNS_Corner_Proportion = shots_OTNS_Total/shots_OTNS_Corner_Total

#Print conclusions from results. 
print("\nThe proportion of Shots On Target Not Scored to Corner Kicks is: ", shots_OTNS_Corner_Proportion*100, "%.")
print("\nSo, assuming that every shot on target not scored resulted in a corner kick\n", 
      shots_OTNS_Corner_Proportion*100, "% of corners would have come from goal kicks. ",
      "\n\nThus, we can deduce that, at maximum, a little over half of all corner kicks",
      "would have come from shots taken. ",
      "\n\nAccounting for shots on target that were rebounded out by the goalkeeper",
      "and blocks by defenders, etc., this number would certainly be lower. ",
      "\n\nTherefore, assuming that the blocks from defenders, goalkeepers saving back out, etc., account for over ", 
      (1-(0.5/shots_OTNS_Corner_Proportion))*100, "% of these shots on target not scored, we can say that the majority ",
      "of corner kicks don't come from shots taken. ",
      "\n\nSimilarly, even if the percentage is lower than ", (1-(0.5/shots_OTNS_Corner_Proportion))*100, "%, "
      "the corner kicks are only just over 50%. "
      "\n\nThus, at minimum, we can say that corners resulting from non-shot taking incidents "
      "account for a large plurality of the corners taken. ")

#______________________________________________________________________________
# Post Processing
#This was just to get rid of any unneccessary files for ease of reading for 
# grader. 
#Anything that was deleted is already encompassed in another dataframe.
#I left a lot of Card variables in as anything that was only used temporarily still 
# seemd important to keep. 

del goal_ArsenalGamesAwayTemp
del goal_ArsenalGamesHome
del goal_ChelseaGamesAwayTemp
del goal_ChelseaGamesHome
del goal_LiverpoolGamesAwayTemp
del goal_LiverpoolGamesHome
del goal_ManUnitedGamesAwayTemp
del goal_ManUnitedGamesHome
del goal_ManCityGamesAwayTemp
del goal_ManCityGamesHome
del goal_TottenhamGamesAwayTemp
del goal_TottenhamGamesHome
del bet_ax1
del bet_ax2
del bet_ax3
del bet_corr_fig1
del bet_corr_fig2
del bet_corr_fig3
del i
del j
del shots_OTNS_Total
del shots_OTNS_Corner_Total
del shots_OTNSH_Sum 
del shots_OTNSA_Sum
del shots_OTNSH_Corners_Sum 
del shots_OTNSA_Corners_Sum 
del shots_OTNS
del shots_OTNSH
del shots_OTNSA
del shots_NOTA
del shots_NOTH
del shots_corr_away
del shots_corr_home
del shots_Corners


