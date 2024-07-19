#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

population_data = {
    'State': ['State1', 'State2', 'State3'],
    'Population': [1000000, 2000000, 1500000]
}
literacy_rate_data = {
    'State': ['State1', 'State2', 'State3'],
    'LiteracyRate': [85, 78, 90]
}
area_data = {
    'State': ['State1', 'State2', 'State3'],
    'Area': [50000, 75000, 60000]
}

population_df = pd.DataFrame(population_data)
literacy_rate_df = pd.DataFrame(literacy_rate_data)
area_df = pd.DataFrame(area_data)

merged_df = population_df.merge(literacy_rate_df, on='State').merge(area_df, on='State')
print(merged_df)


# In[2]:


from sklearn.cluster import KMeans

crime_data = {
    'State': ['State1', 'State2', 'State3'],
    'TotalCrimes': [1000, 1500, 1200],
    'Population': [1000000, 2000000, 1500000],
    'LiteracyRate': [85, 78, 90]
}

crime_df = pd.DataFrame(crime_data)

kmeans = KMeans(n_clusters=3)
crime_df['Cluster'] = kmeans.fit_predict(crime_df[['TotalCrimes', 'Population', 'LiteracyRate']])
print(crime_df)


# In[ ]:




