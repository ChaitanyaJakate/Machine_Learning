# -*- coding: utf-8 -*-
"""Dataset_31_march_2025.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fdIPrj-Fa1Lwt_8v5vMEU8c7CyyytYSl
"""

import pandas as pd
import numpy as np

df=pd.read_csv('/content/Survey data_Inflight Satisfaction Score.csv')

df

'''import requests
from bs4 import BeautifulSoup'''

#site=requests.get('https://www.indiaopd.com/')

#site.status_code

#site.content

#soup=BeautifulSoup(site.content,'html.parser')

#print(soup.prettify())

#soup.find_all('div', class_='doctor-card')

'''doctor_cards = soup.find_all('div', class_='doctor-card')

for card in doctor_cards:
    doctor_name = card.find('h2', class_='doctor-name').text.strip()
    specialization = card.find('p', class_='specialization').text.strip()
    hospital_name = card.find('p', class_='hospital-name').text.strip()
    location = card.find('p', class_='location').text.strip()
    available_slots = card.find('p', class_='available-slots').text.strip()
    print(f"Doctor: {doctor_name}")
    print(f"Specialization: {specialization}")
    print(f"Hospital: {hospital_name}")
    print(f"Location: {location}")
    print(f"Available Slots: {available_slots}")
    print("-" * 40)'''

#doctor_name

df.info()

df.isnull().sum()

df.isnull().mean()*100

df.describe()

import seaborn as sns
import matplotlib.pyplot as plt

df.select_dtypes(exclude='object')

for i in df.select_dtypes(exclude='object'):
  plt.figure(figsize=(6,6))
  sns.boxplot(x=df[i])
  plt.title(f'Boxplot of : {i}')
  plt.plot()

#pd.pivot(data=df,columns=['flight_number','actual_flown_miles'])

cols=df[['flight_number','actual_flown_miles']].copy()

def out_rem():
  for i in cols:
    perc25=cols[i].quantile(0.25)
    perc75=cols[i].quantile(0.75)
    iqr=perc75-perc25
    upper_limit=perc75+1.5*iqr
    lower_limit=perc25-1.5*iqr
    cols[i]=np.where(cols[i]>upper_limit,
                   upper_limit,
                   np.where(cols[i]<lower_limit,
                            lower_limit,
                            cols[i]
                            )
                   )
  return cols

df2=out_rem()
sns.boxplot(df2['actual_flown_miles'])

#df['actual_flown_miles'].describe(), df2['actual_flown_miles'].describe(), df333['actual_flown_miles'].describe()

for i in df2:
  plt.figure(figsize=(6,6))
  sns.boxplot(x=df2[i])
  plt.title(f'Boxplot of : {i}')
  plt.plot()

df.drop(columns=['flight_number','actual_flown_miles'],inplace=True)

new_df=pd.concat([df,df2],axis=1)

new_df.shape

df.shape

sns.heatmap(pd.crosstab(df['international_domestic_indicator'],df['hub_spoke']))

df['entity'].value_counts().plot(kind='pie',autopct='%.2f')

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import TargetEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest,chi2,f_classif
from mlxtend.feature_selection import SequentialFeatureSelector as SFSML
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,r2_score,log_loss,hinge_loss,mean_absolute_error,mean_squared_error

new_df.shape

x=new_df.iloc[:,:28:]
y=new_df.iloc[:,28]

y

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

x_train.shape

y_train.shape

ohe=OneHotEncoder(drop='first',handle_unknown='ignore',sparse_output=False)
te=TargetEncoder()
le=LabelEncoder()
ss=StandardScaler()
ms=MinMaxScaler()
si1=SimpleImputer()
si2=SimpleImputer(strategy='most_frequent')

for i in x_train.select_dtypes(include='object'):
  if x_train[i].nunique()<20:
    print(f'{i} : {x_train[i].unique()}')



#question_text,satisfaction_type ,driver_sub_group1 , fleet_usage, ua_uax , international_domestic_indicator , response_group ,media_provider

for i in x_train.select_dtypes(include='object'):
  if x_train[i].nunique()<20:
    print(f'{i} : {x_train[i].nunique()}')

x_train['arrival_gate']

for i in x_train.select_dtypes(include='object'):
  if x_train[i].nunique()>20:
    print(f'{i} : {x_train[i].unique()}')

[i for i in x_train.select_dtypes(include='object') if x_train[i].isnull().any()]

[i for i in x_train.select_dtypes(exclude='object') if x_train[i].isnull().any()]

"""# **Imputation**"""

imp_cols_tr=x_train[['satisfaction_type','cabin_name','entity','loyalty_program_level','departure_gate','arrival_gate','media_provider']]
imp_cols_te=x_test[['satisfaction_type','cabin_name','entity','loyalty_program_level','departure_gate','arrival_gate','media_provider']]

from sklearn import utils

imp_train=si2.set_output(transform='pandas').fit_transform(imp_cols_tr)
imp_test=si2.set_output(transform='pandas').transform(imp_cols_te)

imp_train['departure_gate'].nunique()

x_train.drop(columns=['satisfaction_type','cabin_name','entity','loyalty_program_level','departure_gate','arrival_gate','media_provider'],inplace=True)
x_test.drop(columns=['satisfaction_type','cabin_name','entity','loyalty_program_level','departure_gate','arrival_gate','media_provider'],inplace=True)

"""# **One Hot Encoding**"""

x_train.select_dtypes(include='object').shape



def cat_cols_sel_tr(x_train):
  selected_cols_tr=[i for i in x_train.select_dtypes(include='object') if x_train[i].nunique()<20]
  return x_train[selected_cols_tr]

def cat_cols_sel_te(x_test):
  selected_cols_te=[i for i in x_test.select_dtypes(include='object') if x_test[i].nunique()<20]
  return x_test[selected_cols_te]

train_cols=pd.concat([cat_cols_sel_tr(x_train),imp_train],axis=1)
test_columns=pd.concat([cat_cols_sel_te(x_test),imp_test],axis=1)

train_cols.drop(columns=['arrival_delay_group','seat_factor_band','loyalty_program_level','generation'],inplace=True)

test_columns.drop(columns=['arrival_delay_group','seat_factor_band','loyalty_program_level','generation'],inplace=True)

trc1=train_cols.drop(columns=['arrival_gate','departure_gate','haul_type'])
tec1=test_columns.drop(columns=['arrival_gate','departure_gate','haul_type'])

train_cols.isnull().sum()

trc1.shape

ohe_tr=pd.DataFrame(ohe.fit_transform(trc1),columns=ohe.get_feature_names_out(trc1.columns))
ohe_te=pd.DataFrame(ohe.transform(tec1),columns=ohe.get_feature_names_out(tec1.columns))

trc1.columns

"""# **Ordinal Encoder**"""

from sklearn.preprocessing import OrdinalEncoder

imp_train['loyalty_program_level'].unique()

oe1=OrdinalEncoder(categories=[['non-elite', 'NBK', 'premier silver', 'premier gold',
               'premier platinum', 'premier 1k', 'global services']])
oe2=OrdinalEncoder(categories=[['0 to 70', '70+','80+','90+']])
oe3=OrdinalEncoder(categories=[['Short','Medium','Long']])
oe4=OrdinalEncoder(categories=[['Greatest', 'Silent', 'Boomer', 'Gen X', 'Millennial', 'Gen Z', 'NBK']])

imp_train['loyalty_program_level']=oe1.fit_transform(imp_train[['loyalty_program_level']])
imp_test['loyalty_program_level']=oe1.transform(imp_test[['loyalty_program_level']])



x_train['generation']=oe4.fit_transform(x_train[['generation']])
x_test['generation']=oe4.transform(x_test[['generation']])

x_train['seat_factor_band']=oe2.fit_transform(x_train[['seat_factor_band']])
x_test['seat_factor_band']=oe2.transform(x_test[['seat_factor_band']])

x_train['haul_type']=oe3.fit_transform(x_train[['haul_type']])
x_test['haul_type']=oe3.transform(x_test[['haul_type']])

x_train['seat_factor_band'].unique()

x_train['haul_type'].unique()

"""# **LabelEncoder**"""

y_train=le.fit_transform(y_train)
y_test=le.transform(y_test)

"""# **TargetEncoder**"""

#te.fit_transform(x_train[['origin_station_code']],y_train)

#pd.Series(te.set_output(transform='pandas').fit_transform(x_train[['origin_station_code']], y_train).values.ravel()).unique()

x_train['origin_station_code']=te.fit_transform(x_train[['origin_station_code']],y_train)
x_test['origin_station_code']=te.transform(x_test[['origin_station_code']])

x_train['destination_station_code']=te.fit_transform(x_train[['destination_station_code']],y_train)
x_test['destination_station_code']=te.transform(x_test[['destination_station_code']])



imp_tr_ag=pd.DataFrame(te.fit_transform(imp_cols_tr[['arrival_gate']],y_train),columns=te.get_feature_names_out(['arrival_gate']))
imp_te_ag=pd.DataFrame(te.transform(imp_cols_te[['arrival_gate']]),columns=te.get_feature_names_out(['arrival_gate']))

imp_tr_dg=pd.DataFrame(te.fit_transform(imp_cols_tr[['departure_gate']],y_train),columns=te.get_feature_names_out(['departure_gate']))
imp_te_dg=pd.DataFrame(te.transform(imp_cols_te[['departure_gate']]),columns=te.get_feature_names_out(['departure_gate']))



imp_cols_tr['arrival_gate']



imp_cols_tr1=imp_train[['loyalty_program_level']]
imp_cols_te1=imp_test[['loyalty_program_level']]

imp_cols_tr.columns,trc1.columns

x_train['scheduled_departure_day']=pd.to_datetime(x_train['scheduled_departure_date']).dt.day
x_train['scheduled_departure_month']=pd.to_datetime(x_train['scheduled_departure_date']).dt.month
x_train['scheduled_departure_year']=pd.to_datetime(x_train['scheduled_departure_date']).dt.year

x_test['scheduled_departure_day']=pd.to_datetime(x_test['scheduled_departure_date']).dt.day
x_test['scheduled_departure_month']=pd.to_datetime(x_test['scheduled_departure_date']).dt.month
x_test['scheduled_departure_year']=pd.to_datetime(x_test['scheduled_departure_date']).dt.year

x_train.drop(columns=['scheduled_departure_day','fleet_type_description'],inplace=True)
x_test.drop(columns=['scheduled_departure_day','fleet_type_description'],inplace=True)

new_df['seat_factor_band'].unique()

new_df['cabin_code_desc'].unique()

imp_cols_tr.columns,trc1.columns



new_df.select_dtypes(include='object').columns

x_train.select_dtypes(include='object').columns

x_train.drop(columns=['origin_station_code','destination_station_code','record_locator','scheduled_departure_date','cabin_code_desc'])

imp_cols_tr1

imp_tr_ag

imp_tr_dg



new_train=pd.concat([x_train.select_dtypes(exclude='object').reset_index(),ohe_tr.reset_index(),imp_cols_tr1.reset_index(),imp_tr_ag.reset_index(),imp_tr_dg.reset_index()],axis=1).drop(columns=['index'])
new_test=pd.concat([x_test.select_dtypes(exclude='object').reset_index(),ohe_te.reset_index(),imp_cols_te1.reset_index(),imp_te_ag.reset_index(),imp_te_dg.reset_index()],axis=1).drop(columns=['index'])

#new_df.select_dtypes(exclude='object')

#x_train['arrival_delay_minutes']



"""# **StandardScaler**"""

new_train_ss=ss.fit_transform(new_train)
new_test_ss=ss.transform(new_test)

"""# **MinMaxScaler**"""

new_train_ms=ms.fit_transform(new_train)
new_test_ms=ms.transform(new_test)

"""# **Feature_Selection**"""

# Variance Threshold
from sklearn.feature_selection import VarianceThreshold
vrt=VarianceThreshold(threshold=0.04)
vrt_train=vrt.fit_transform(new_train_ss,y_train)
vrt_test=vrt.transform(new_test_ss)

# ANOVA
anova=SelectKBest(f_classif,k=12)
anova_train=anova.fit_transform(vrt_train,y_train)
anova_test=anova.transform(vrt_test)

# chi_square
chi_square=SelectKBest(chi2,k=12)
chi_square_train=chi_square.fit_transform(new_train_ms,y_train)
chi_square_test=chi_square.transform(new_test_ms)

"""# **Estimators**"""

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

lr=LogisticRegression()
svm=SVC(C=1.0,kernel='rbf')
rfc=RandomForestClassifier(n_estimators=200,bootstrap=True,random_state=12)
adaboost=AdaBoostClassifier(estimator=LogisticRegression,n_estimators=100,random_state=12)
dt=DecisionTreeClassifier(random_state=12)

# Backward Elimination
modelll=SFSML(svm,k_features=12,forward=False,cv=3,verbose=2,n_jobs=-1)

pok=modelll.fit(anova_train,y_train)

pok.k_score_

"""# **Model_Selection And Training**"""

svm.fit(new_train_ss,y_train)

y_pred=svm.predict(new_test_ss)

accuracy_score(y_test,y_pred)

cross_val_score(svm,new_train_ss,y_train,cv=3).mean()

"""# **Random Forest**"""

rfc.fit(vrt_train,y_train)

y_pred1=rfc.predict(vrt_test)
accuracy_score(y_test,y_pred1)

"""# **Artificial Neural Network**"""

import tensorflow
from tensorflow import keras
from keras import Sequential
from keras import regularizers
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.layers import Dense,BatchNormalization,Dropout
from keras.callbacks import LearningRateScheduler

model=Sequential()
model.add(Dense(12,activation='relu',input_dim=vrt_train.shape[1],kernel_initializer='he_normal'))
model.add(BatchNormalization())
model.add(Dense(24,activation='relu',kernel_initializer='he_normal'))
model.add(BatchNormalization())
model.add(Dense(36,activation='relu',kernel_initializer='he_normal'))
model.add(BatchNormalization())
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(loss='bce',optimizer='adam',metrics=['accuracy'])

history=model.fit(vrt_train,y_train,validation_data=(vrt_test,y_test),epochs=30,callbacks=[EarlyStopping(patience=2,verbose=2,monitor='loss')])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

"""# **Pytorch**"""

import torch
from torch.utils.data import Dataset,DataLoader
import torch.nn as nn

class CustomDataset(Dataset):
  def __init__(self,features,labels):
    self.features=torch.tensor(features,dtype=torch.float32)
    self.labels=torch.tensor(labels,dtype=torch.long)
  def __len__(self):
    return len(self.features)

  def __getitem__(self,index):
    return self.features[index], self.labels[index]

train_dt=CustomDataset(new_train_ss,y_train)
test_dt=CustomDataset(new_test_ss,y_test)

train_loader=DataLoader(train_dt,batch_size=32,shuffle=True)
test_loader=DataLoader(test_dt,batch_size=32,shuffle=True)

class NN(nn.Module):
  def __init__(self,num_features):
    super().__init__()
    self.model=nn.Sequential(
        nn.Linear(num_features,12),
        nn.ReLU(),
        nn.Linear(12,24),
        nn.ReLU(),
        nn.Linear(24,2)
    )
  def forward(self,x):
    return self.model(x)

epochs=30

model1=NN(new_train_ss.shape[1])
criterion=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model1.parameters())

for epoch in range(epochs):
  total_epoch_loss=0
  for batch_features,batch_labels in train_loader:
    outputs=model1(batch_features)
    loss=criterion(outputs,batch_labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    total_epoch_loss+=loss.item()
  avg_loss=total_epoch_loss/len((train_loader))
  print(f'Epochs : {epoch+1} : avg loss of {epoch+1} is {avg_loss}')

