**Section-1: Data Preparation and Cleaning**

1.   In this data Analysis We will be using various Libraries such as pandas, Numpy, Seaborn & Matplotlib
2.  Installing The Mentioned Libraries

pip install numpy

pip install pandas

pip install seaborn

pip install matplotlib

import numpy as np 
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

*The Dataset I am using is downloaded from kaggle i.e IPL_Matches_2022.csv* 

*Reading Data using Pandas*

# Import data
df =  pd.read_csv('/content/drive/MyDrive/IPL_Matches_2022.csv')

*Using .info() method we can See the type of values each Column contains
df.info()*

df.info()

*to know number of rows and columns of dataset we will use the .shape method*

df.shape

*# The .describe method gives us the overview of our data i.e data in rows and columns*

df.describe()

*Data Cleaning and Processing*

df

*We wont be using the Umpires Columns ('Umpire1', 'Umpire2') in this analysis so we will remove those fields using .drop() method*

#inplace argument is used to make permanent changes in the dataframe
df.drop(columns=['Umpire1','Umpire2'],inplace=True)

# Exploring all column names in the data frame
df.columns

# Now lets seasons data we have in our dataframe
# we use .unique() method to list the unique items from the selected column
df.Season.unique()

# Now Lets see all the teams that have played so far
df.Team1.unique()

df.Team2.unique()


**From the Above Observations from Data cleaning**

*   This dataset include data of 59 match
* This dataset include only the data of season 2022
* In This season, There are 10 teams
*   Lucknow Super Giants is new team included in this Season
*   Gujarat Titans is also new team which is included in this Season



*Lets Check For Missing Values*

# we can use .isnull() to set Null values to True and then use .sum() to calculate all the null values
df.isnull().sum().sum()

*Above Result Shows we have 59 Null values in our data set. Now we will search For them.*

null_df = df[df.isna().any(axis=1)]
null_df

**From Above Observations**

*   We can See NaN values in Margin Column
*   We Can See this values are at index 0-58


df.loc[0:58]

*We wont be using the margin Column in this analysis so we will remove this fields using .drop() method*

df.drop(columns=['method'],inplace=True)

df.columns

# Lets Check if any any other columns Have NaN values
df.isna().any()

**Section-2: Exploratory Analysis and Visualization**

*   Now We Will Analyse the Data For Different types of Queries



#Lets find total Number of Matches Played till now
df.ID.count()

#Lets See About Cities Where Matches have Been Played
df.City.unique()

*Now Lets See Match count played in each of the above city*

cities = df.groupby('City')[['ID']].count()
cities

*Lets Arrange this data In a More Organised manner*

plt.figaspect
cities.rename(columns={'ID':'Matches'},inplace=True)
cities = cities.sort_values('Matches',ascending=True).reset_index()
cities

*We can See IPL has Altogether 3 Official Locations where matches have been Played in group stage.*


#Lets Plot the Cities in a bar Chart
plt.figure(figsize=(20,5))
plt.grid()
plt.title('Number Of Matches Played In Each City')
sns.barplot(x='Matches',y='City',data=cities);


*It seems Mumbai has been the favourite Location followed by Pune and Navi Mumbai for Group Stage*

*Now Lets See Matches Won by Each Team till now*

df.WinningTeam.unique()

Winner_df = df.groupby('WinningTeam')[['ID']].count()
Winner_df = Winner_df.sort_values('ID', ascending=False).reset_index()

Winner_df.rename(columns = {'ID':'wins','WinningTeam':'Teams'},inplace=True)
Winner_df

*Seems Gujarat Titans Have won the Most matches in IPL 2022 Till Date. Followed by Lucknow Super Giants.*

*   Now Lets Plot These Wins



#Plotting Wins vs Teams
plt.figure(figsize=(25,7))
plt.xlabel('Teams')
plt.ylabel('Wins')
plt.title('Matches Won By Each Team')
plt.bar(Winner_df.Teams,Winner_df.wins)

*Lets Add Colour To Each Team so That we Get A Clear Idea*



*  We can do this by using color argument of the bar() Function





#Plotting Wins vs Teams
#We will be using colour code of teams jersey to make it easily understandable
plt.figure(figsize=(15,5))
plt.legend(Winner_df.Teams,loc=1)
plt.xlabel('Teams',fontweight='bold',fontsize=15)
plt.ylabel('Wins',fontweight='bold',fontsize=15)
plt.tick_params(labelsize=15)
plt.xticks(rotation=90)
plt.title('Matches Won By Each Team',fontweight='bold',fontsize=15)
plt.bar(Winner_df.Teams, Winner_df.wins, color = ['#002147','#96ded1','#f984ef','#64e986','#1f75fe','#000000','#FF0000','#FFA500','#ffff00','#0000FF'])

*From the above Graph its clear Gujarat Titans have won most number of Matches*

Section 3: Questions on dataset ipl 2022:

*   What was the most preferred Decision On winning Toss i.e. Choose To Bat / Choose To Field
*   Which Decision has proved most beneficial i.e Field / Bat
*   Which Venue has hosted the Most Number Of Ipl Matches
*   Who has been awarded with Player Of the Max maximum Number Of Times



#Q1. What was the most preferred Decision On winning Toss i.e. Bat / Field 
# We can see toss decision is either bat/field
df.TossDecision.unique()
decision_df = df.groupby('TossDecision')[['ID']].count()
decision_df = decision_df.sort_values('ID').reset_index()
decision_df.rename(columns={'ID':'Total','TossDecision':'Decision'},inplace=True)
decision_df

#Lets plot the Result
plt.figure(figsize=(10,10))
plt.title("Preferred Decision",fontweight='bold',fontsize=15)
plt.xlabel('Decision',fontweight='bold',fontsize=15)
plt.ylabel('Total',fontweight='bold',fontsize=15)
plt.tick_params(labelsize=20)
plt.grid()
plt.bar(decision_df.Decision, decision_df.Total, color=['#4863A0','#566D7E']);

*The Most Preferred Decision After Winning Toss in the IPL 2022 has been "Choose to Field First"*

#Q2. Which Decision has proved most beneficial i.e Field / Bat
field_df = df.loc[(df['TossWinner'] == df['WinningTeam']) & (df['TossDecision'] == 'field'), ['ID', 'WinningTeam','TossDecision']]
field_df.WinningTeam.count()

bat_df = df.loc[(df['TossWinner'] == df['WinningTeam']) & (df['TossDecision'] == 'bat'), ['ID', 'WinningTeam','TossDecision']]
bat_df.WinningTeam.count()

frames = [bat_df, field_df]
result_df = pd.concat(frames)
result_df = result_df.groupby('TossDecision')[['ID']].count()
result_df

#As from Earlier Analysis we know that ,52 times toss winning Team Choose to Field First and only 7 Times batting was choosen
# Now Lets Plot the New Understanding Regarding the Success of these decisions
result_df = result_df.sort_values('ID').reset_index()
result_df.rename(columns={'ID':'Total','TossDecision':'Decision'},inplace=True)
result_df

plt.figure(figsize=(10,10))
plt.title("Decision Success",fontweight='bold',fontsize=30)
plt.xlabel('Decision',fontweight='bold',fontsize=30)
plt.ylabel('Total',fontweight='bold',fontsize=30)
plt.tick_params(labelsize=20)
plt.bar(decision_df.Decision, decision_df.Total, color=['#4CC552','#4CC552'])
plt.bar(result_df.Decision, result_df.Total, color=['#00FF00','#00FF00'])
plt.legend(['Decision Taken','Decision Proved Right'])

*We can See the Fielding decision on winning toss has been most Preferred one but choosing the bat decision on winning toss have higher number chances of winning match as compare to fielding decison*


*Q3. Which Venue has hosted the Most Number Of Matches*

# Lets see how many venues have hosted the Ipl Matches
df.Venue.unique()

total_venue = list(df.Venue.unique())
len(total_venue)

*We Can See ipl 2022 has hosted the Matches across 4 Different venues in group stages.Lets See Which Venue Hosted the Most Number Of Matches*

venue_df = df.groupby('Venue')[['ID']].count()
venue_df = venue_df.sort_values('ID',ascending=False).reset_index()
venue_df.rename(columns={'ID':'Total_Match','Venue':'Stadium'},inplace=True)
labels = list(venue_df.Stadium)
venue_df

*Graphical Representation :-* 

plt.figure(figsize=(10,10))
plt.title("Total_Matches_played_in_Stadium",fontweight='bold' )
plt.xticks(rotation=90)
plt.yticks(ticks=np.arange(0,25,5))
plt.ylabel('Total_Match')
plt.xlabel('Stadium')
sns.barplot(x=venue_df.Stadium,y=venue_df.Total_Match, alpha=0.6)

plt.figure(figsize=(12,10))
plt.title("Venues",fontweight='bold',fontsize=30)
plt.tick_params(labelsize=40)
plt.pie(venue_df.Total_Match,labels=labels,textprops={'fontsize': 15})

*So We can See the most Number of matches were played at Dr DY Patil Sports Academy Stadium	(18) Followed By Wankhede Stadium (16)*

*Q4. Who has been awarded with Player Of the Match maximum Number Of Times*

#Lets Check how many players have been awarded with player of the match award
len(df.Player_of_Match.unique())

*we can see 47 Players have been awarded with player of the match title*

*Now Among these players lets see who have Got the maximum Player of The Match Awards*

player_df = df.groupby('Player_of_Match')[['ID']].count()
player_df

player_df = player_df.sort_values('ID',ascending=False).reset_index()
player_df

#Now From these Players Lets Extract Top 10 Players
players_df = player_df.head(10).copy()
players_df.rename(columns={'ID':'Total_Awards','Player_of_Match':'Man_Of_The_Match'},inplace=True)
labels1 = list(players_df.Man_Of_The_Match)
players_df

plt.figure(figsize=(12,12))
plt.title("Man_Of_The_Match",fontweight='bold',fontsize=20)
plt.tick_params(labelsize=14)
plt.pie(players_df.Total_Awards,labels=labels1,textprops={'fontsize': 10})

*From the above result it is clear that Kuldeep Yadav has received  "4 Man of The Match Titles" .*

plt.figure(figsize=(20,5))
plt.title("Top 10 Players with Highest Man Of the Match Titles",fontweight='bold' )
plt.xticks(rotation=90)
plt.yticks(ticks=np.arange(0,25,5))
plt.ylabel('No. of Awards')
plt.xlabel('Players')
sns.barplot(x=players_df.Man_Of_The_Match,y=players_df.Total_Awards, alpha=0.6);



#Section 4: Conclusion
In this analysis I used the IPL_Matches_2022.csv file from the kaggle Datasets. Following are my conclusions about it

*   A total of 59 matches have been played 
*   Most number of Matches were played in Dr DY Patil Sports Academy, Mumbai	[18]
*   Most preferable choice after winning toss is to field first  
*   52 times fielding and 7 times batting is choosed by Toss Winner
*   Gujarat Titans Have Won the Most Number of Matches (9) followed by Lukhnow Super Gaints with (8) Matches
*   Dr DY Patil Sports Academy (Stadium) Hosted the Most Number of Matches (18) followed by wankhede Stadium (16)
*   Kuldeep Yadav has been the Man Of The Match Most Number of Times with "4" Awards
