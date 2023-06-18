#!/usr/bin/env python
# coding: utf-8



# In[2]:


import pickle
import pandas as pd
import sys

# In[3]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[6]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[42]:


year = int(sys.argv[1])
month = int(sys.argv[2])


# In[43]:


df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')


# In[ ]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[ ]:


y_pred.std()


# In[ ]:


df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[ ]:


df['predictions'] = y_pred

print(y_pred.mean())

# In[ ]:


df_result = df[['ride_id', 'predictions']]


# In[33]:


output_file = "./saved_predictions.parquet"


# In[34]:


df_result


# In[35]:


df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[ ]:




