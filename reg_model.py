import numpy as np
import pandas as pd
import pickle

gsheet_id = "1mymPRVXp3g1PUTCL8c8TSzFjUhrAuxHI"
sheet_name = "Data"
gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheet_id ,sheet_name)
df = pd.read_csv(gsheet_url)

df.loc[ (df['Time_of_reg'] >= '08:00:00') & (df['Time_of_reg'] < '08:30:00'), 'Time_of_reg'] = '01'
df.loc[ (df['Time_of_reg'] >= '08:30:00') & (df['Time_of_reg'] < '09:00:00'), 'Time_of_reg'] = '02'
df.loc[ (df['Time_of_reg'] >= '09:00:00') & (df['Time_of_reg'] < '09:30:00'), 'Time_of_reg'] = '03'
df.loc[ (df['Time_of_reg'] >= '09:30:00') & (df['Time_of_reg'] < '10:00:00'), 'Time_of_reg'] = '04'
df.loc[ (df['Time_of_reg'] >= '10:00:00') & (df['Time_of_reg'] < '10:30:00'), 'Time_of_reg'] = '05'
df.loc[ (df['Time_of_reg'] >= '10:30:00') & (df['Time_of_reg'] < '11:00:00'), 'Time_of_reg'] = '06'
df.loc[ (df['Time_of_reg'] >= '11:00:00') & (df['Time_of_reg'] < '11:30:00'), 'Time_of_reg'] = '07'
df.loc[ (df['Time_of_reg'] >= '11:30:00') & (df['Time_of_reg'] < '12:00:00'), 'Time_of_reg'] = '08'
df.loc[ (df['Time_of_reg'] >= '12:00:00') & (df['Time_of_reg'] < '12:30:00'), 'Time_of_reg'] = '09'
df.loc[ (df['Time_of_reg'] >= '12:30:00') & (df['Time_of_reg'] < '13:00:00'), 'Time_of_reg'] = '10'
df.loc[ (df['Time_of_reg'] >= '13:00:00') & (df['Time_of_reg'] < '13:30:00'), 'Time_of_reg'] = '11'
df.loc[ (df['Time_of_reg'] >= '13:30:00') & (df['Time_of_reg'] < '14:00:00'), 'Time_of_reg'] = '12'
df.loc[ (df['Time_of_reg'] >= '14:00:00') & (df['Time_of_reg'] < '14:30:00'), 'Time_of_reg'] = '13'
df.loc[ (df['Time_of_reg'] >= '14:30:00') & (df['Time_of_reg'] < '15:00:00'), 'Time_of_reg'] = '14'
df.loc[ (df['Time_of_reg'] >= '15:00:00') & (df['Time_of_reg'] < '15:30:00'), 'Time_of_reg'] = '15'
df.loc[ (df['Time_of_reg'] >= '15:30:00') & (df['Time_of_reg'] < '16:00:00'), 'Time_of_reg'] = '16'
df.loc[ (df['Time_of_reg'] >= '16:00:00') & (df['Time_of_reg'] < '16:30:00'), 'Time_of_reg'] = '17'
df.loc[ (df['Time_of_reg'] >= '16:30:00') & (df['Time_of_reg'] < '17:00:00'), 'Time_of_reg'] = '18'
df.loc[ (df['Time_of_reg'] >= '17:00:00') & (df['Time_of_reg'] < '17:30:00'), 'Time_of_reg'] = '19'
df.loc[ (df['Time_of_reg'] >= '17:30:00') & (df['Time_of_reg'] < '18:00:00'), 'Time_of_reg'] = '20'
df.loc[ (df['Time_of_reg'] >= '18:00:00') & (df['Time_of_reg'] < '18:30:00'), 'Time_of_reg'] = '21'
df.loc[ (df['Time_of_reg'] >= '18:30:00') & (df['Time_of_reg'] < '19:00:00'), 'Time_of_reg'] = '22'
df.loc[ (df['Time_of_reg'] >= '19:00:00') & (df['Time_of_reg'] < '19:30:00'), 'Time_of_reg'] = '23'
df.loc[ (df['Time_of_reg'] >= '19:30:00') & (df['Time_of_reg'] < '20:00:00'), 'Time_of_reg'] = '24'
df.loc[ (df['Time_of_reg'] >= '20:00:00') & (df['Time_of_reg'] < '20:30:00'), 'Time_of_reg'] = '25'
df.loc[ (df['Time_of_reg'] >= '20:30:00') & (df['Time_of_reg'] < '21:00:00'), 'Time_of_reg'] = '26'

df.loc[(df.Day == 'Monday'), ['Day']] = 1
df.loc[(df.Day == 'Tuesday'), ['Day']] = 2
df.loc[(df.Day == 'Wednesday'), ['Day']] = 3
df.loc[(df.Day == 'Thursday'), ['Day']] = 4
df.loc[(df.Day == 'Friday'), ['Day']] = 5
df.loc[(df.Day == 'Saturday'), ['Day']] = 6
df.loc[(df.Day == 'Sunday'), ['Day']] = 7

df.loc[(df.Name_of_Dr == 'A'), ['Name_of_Dr']] = 1
df.loc[(df.Name_of_Dr == 'B'), ['Name_of_Dr']] = 2
df.loc[(df.Name_of_Dr == 'C'), ['Name_of_Dr']] = 3
df.loc[(df.Name_of_Dr == 'D'), ['Name_of_Dr']] = 4
df.loc[(df.Name_of_Dr == 'E'), ['Name_of_Dr']] = 5
df.loc[(df.Name_of_Dr == 'F'), ['Name_of_Dr']] = 6
df.loc[(df.Name_of_Dr == 'G'), ['Name_of_Dr']] = 7
df.loc[(df.Name_of_Dr == 'H'), ['Name_of_Dr']] = 8
df.loc[(df.Name_of_Dr == 'I'), ['Name_of_Dr']] = 9
df.loc[(df.Name_of_Dr == 'J'), ['Name_of_Dr']] = 10
df.loc[(df.Name_of_Dr == 'K'), ['Name_of_Dr']] = 11
df.loc[(df.Name_of_Dr == 'L'), ['Name_of_Dr']] = 12

df.loc[(df.Time_for_reg == '00:01:00'), ['Time_for_reg']] = 1
df.loc[(df.Time_for_reg == '00:02:00'), ['Time_for_reg']] = 2
df.loc[(df.Time_for_reg == '00:03:00'), ['Time_for_reg']] = 3
df.loc[(df.Time_for_reg == '00:04:00'), ['Time_for_reg']] = 4
df.loc[(df.Time_for_reg == '00:05:00'), ['Time_for_reg']] = 5
df.loc[(df.Time_for_reg == '00:06:00'), ['Time_for_reg']] = 6
df.loc[(df.Time_for_reg == '00:07:00'), ['Time_for_reg']] = 7
df.loc[(df.Time_for_reg == '00:08:00'), ['Time_for_reg']] = 8
df.loc[(df.Time_for_reg == '00:09:00'), ['Time_for_reg']] = 9
df.loc[(df.Time_for_reg == '00:10:00'), ['Time_for_reg']] = 10

X = df.iloc[:, [2,3]].values
y = df.iloc[:, 5].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.linear_model import LinearRegression
regressor1 = LinearRegression()
regressor1.fit(X_train, y_train)

y_pred = regressor1.predict(X_test)
np.set_printoptions(precision=2)
pickle.dump(regressor1,open('reg_model.pkl','wb'))
reg_model=pickle.load(open('reg_model.pkl','rb'))