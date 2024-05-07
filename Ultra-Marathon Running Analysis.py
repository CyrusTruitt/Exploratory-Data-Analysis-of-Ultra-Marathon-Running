#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# https://www.kaggle.com/datasets/aiaiaidavid/the-big-dataset-of-ultra-marathon-running/discussion/420633


# In[ ]:


#import libraries


# In[7]:


import pandas as pd


# In[8]:


import seaborn as sns


# In[10]:


df = pd.read_csv("C:/Users/Truit/OneDrive/Desktop/Projects/Python/Ultra-marathon running/TWO_CENTURIES_OF_UM_RACES.csv")


# In[ ]:


#See the data that's been imported


# In[11]:


df.head(10)


# In[12]:


df.shape


# In[14]:


df.dtypes


# In[ ]:


#Clean up data


# In[ ]:


#Only wants USA races, 50k or 50Mi, 2020


# In[ ]:


#Step 1 show 50Mi or 50k
#50km
#50mi


# In[19]:


df[df['Event distance/length'] == '50mi']


# In[ ]:


#combine 50k/50mi with isin


# In[20]:


df[df['Event distance/length'].isin(['50km','50mi'])]


# In[21]:


df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020)]


# In[26]:


df[df['Event name'] == 'Everglades 50 Mile Ultra Run (USA)']['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)


# In[55]:


df[ df["Event name"].str.contains(r"\(USA\)")]


# In[ ]:


#combine all filters together


# In[56]:


df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020) & (df["Event name"].str.contains(r"\(USA\)"))]


# In[59]:


df2 = df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020) & (df["Event name"].str.contains(r"\(USA\)"))]


# In[60]:


df2.head(10)


# In[61]:


df2.shape


# In[ ]:


#Remove (USA) from event name


# In[62]:


df2['Event name'].str.split('(').str.get(0)


# In[63]:


df2['Event name'] = df2['Event name'].str.split('(').str.get(0)


# In[64]:


df2.head()


# In[ ]:


#clean up athlete age


# In[67]:


df2['athlete_age'] = 2020 - df2['Athlete year of birth']


# In[ ]:


#remove h from athlete performance


# In[70]:


df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)


# In[71]:


df2.head(5)


# In[ ]:


#drop columns: Athlete Club, Athlete Country, Athlete year of birth, Athlete Age Category


# In[74]:


df2 = df2.drop(['Athlete club', 'Athlete country', 'Athlete year of birth', 'Athlete age category'], axis = 1)


# In[75]:


df2.head()


# In[ ]:


#Clean up null values


# In[77]:


df2.isna().sum()


# In[78]:


df2[df2['athlete_age'].isna()==1]


# In[80]:


df2 = df2.dropna()


# In[81]:


df2.shape


# In[ ]:


#check for dupes


# In[82]:


df2[df2.duplicated() == True]


# In[ ]:


#Reset index


# In[83]:


df2.reset_index(drop = True)


# In[ ]:


#Fix Types


# In[85]:


df2.dtypes


# In[86]:


df2['athlete_age'] = df2['athlete_age'].astype(int)


# In[87]:


df2['Athlete average speed'] = df2['Athlete average speed'].astype(float)


# In[88]:


df2.dtypes


# In[89]:


df2.head()


# In[ ]:


#rename columns


# In[ ]:


#Year of event                  int64
#Event dates                   object
#Event name                    object
#Event distance/length         object
#Event number of finishers      int64
#Athlete performance           object
#Athlete gender                object
#Athlete average speed        float64
#Athlete ID                     int64



# In[116]:


df2 = df2.rename(columns = {'Year of event': 'year',
                            'Event dates': 'race_day',
                            'Event name': 'race_name',
                            'Event distance/length':'race_length',
                            'Event number of finishers':'race_number_of_finishers',
                            'Athlete performance':'athlete_performance',
                            'Athlete gender':'athlete_gender',
                            'Athlete average speed':'athlete_average_speed',
                            'Athlete ID':'athlete_id'
                        })


# In[117]:


df2.head()


# In[ ]:


#reorder columns


# In[118]:


df3 = df2[['race_day', 'race_name','race_length', 'race_number_pf_finishers', 'athlete_id', 'athlete_gender', 'athlete_age', 'athlete_performance', 'athlete_average_speed']]


# In[119]:


df3.head()


# In[ ]:


#find 2 races that my friend ran in 2020 - Sarasota | Everglades


# In[123]:


df3[df3['race_name'] == 'Everglades 50 Mile Ultra Run '] 


# In[ ]:


#222509


# In[124]:


df3[df3['athlete_id'] == 222509]


# In[ ]:


#charts and graphs


# In[125]:


sns.histplot(df3['race_length'])


# In[126]:


sns.histplot(df3, x = 'race_length', hue = 'athlete_gender')


# In[127]:


sns.displot(df3[df3['race_length'] == '50mi']['athlete_average_speed'])


# In[129]:


sns.violinplot(data = df3, x= 'race_length', y= 'athlete_average_speed', hue = 'athlete_gender', split = True, inner = 'quart',
              linewidth = 1)


# In[132]:


sns.lmplot(data=df3, x= 'athlete_age', y= 'athlete_average_speed', hue = 'athlete_gender')


# In[ ]:


#Questions I want to find out from the data


# In[ ]:


#race_day
#race_name
#race_length
#race_number_pf_finishers
#athlete_id
#athlete_gender
#athlete_age
#athlete_performance
#athlete_average_speed


# In[ ]:


#Difference in speed for the 50k, 50mi male to female


# In[134]:


df3.groupby(['race_length', 'athlete_gender'])['athlete_average_speed'].mean()


# In[ ]:


#What age groups are best in the 50m Race (20 + race min)


# In[136]:


df3.query('race_length == "50mi"').groupby('athlete_age')['athlete_average_speed'].agg(['mean', 'count']).sort_values(
'mean', ascending = False).query('count>19')


# In[ ]:


#What age groups are worst in the 50m Race (20 + race min)


# In[138]:


df3.query('race_length == "50mi"').groupby('athlete_age')['athlete_average_speed'].agg(['mean', 'count']).sort_values(
'mean', ascending = True).query('count>19')


# In[ ]:


#Seasons for the data -> Slower in summer than winter?

#spring 3-5
#summer 6-8
#fall 9-11
#winter 12-2

#Split between two decimals


# In[139]:


df3['race_month'] = df3['race_day'].str.split('.').str.get(1).astype(int)


# In[141]:


df3.head(25)


# In[144]:


df3['race_season'] = df3['race_month'].apply(
    lambda x: 'Winter' if x > 11 else 'Fall' if x > 8 else 'Summer' if x > 5 else 'Spring' if x > 2 else 'Winter'
)


# In[145]:


df3.head(25)


# In[148]:


df3.groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[ ]:


#50 miler only


# In[149]:


df3.query('race_length == "50mi"').groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending = False)


# In[ ]:





# In[ ]:





# In[ ]:




