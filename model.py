import numpy as np
import pandas as pd
import pickle

gsheet_id = "10MF3i_pio731qBAo1-uEmMqdsjmeDklLXbX_LVhk5NM"
sheet_name = "DATA"
gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheet_id ,sheet_name)
df = pd.read_csv(gsheet_url)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df["Time_for_reg"] = le.fit_transform(df['Time_for_reg'])
df["Time_for_billing"] = le.fit_transform(df['Time_for_billing'])
#df["Time_for_Consultation"] = le.fit_transform(df['Time_for_Consultation'])
df.loc[(df.Day == 'Monday'), ['Day']] = 1
df.loc[(df.Day == 'Tuesday'), ['Day']] = 2
df.loc[(df.Day == 'Wednesday'), ['Day']] = 3
df.loc[(df.Day == 'Thursday'), ['Day']] = 4
df.loc[(df.Day == 'Friday'), ['Day']] = 5
df.loc[(df.Day == 'Friday '), ['Day']] = 5
df.loc[(df.Day == 'Saturday'), ['Day']] = 6
df.loc[(df.Day == 'saturday'), ['Day']] = 6
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
#df['OPD_Waiting_Time'] = df['OPD_Waiting_Time'].astype('string')

df.loc[ (df['Time_of_reg'] >= '08:00:00') & (df['Time_of_reg'] < '09:00:00'), 'Time_of_reg'] = '01'
df.loc[ (df['Time_of_reg'] >= '09:00:00') & (df['Time_of_reg'] < '10:00:00'), 'Time_of_reg'] = '02'
df.loc[ (df['Time_of_reg'] >= '10:00:00') & (df['Time_of_reg'] < '11:00:00'), 'Time_of_reg'] = '03'
df.loc[ (df['Time_of_reg'] >= '11:00:00') & (df['Time_of_reg'] < '12:00:00'), 'Time_of_reg'] = '04'
df.loc[ (df['Time_of_reg'] >= '12:00:00') & (df['Time_of_reg'] < '13:00:00'), 'Time_of_reg'] = '05'
df.loc[ (df['Time_of_reg'] >= '13:00:00') & (df['Time_of_reg'] < '14:00:00'), 'Time_of_reg'] = '06'
df.loc[ (df['Time_of_reg'] >= '14:00:00') & (df['Time_of_reg'] < '15:00:00'), 'Time_of_reg'] = '07'
df.loc[ (df['Time_of_reg'] >= '15:00:00') & (df['Time_of_reg'] < '16:00:00'), 'Time_of_reg'] = '08'
df.loc[ (df['Time_of_reg'] >= '16:00:00') & (df['Time_of_reg'] < '17:00:00'), 'Time_of_reg'] = '09'
df.loc[ (df['Time_of_reg'] >= '17:00:00') & (df['Time_of_reg'] < '18:00:00'), 'Time_of_reg'] = '10'
df.loc[ (df['Time_of_reg'] >= '18:00:00') & (df['Time_of_reg'] < '19:00:00'), 'Time_of_reg'] = '11'
df.loc[ (df['Time_of_reg'] >= '19:00:00') & (df['Time_of_reg'] < '20:00:00'), 'Time_of_reg'] = '12'
df.loc[ (df['Time_of_reg'] >= '20:00:00') & (df['Time_of_reg'] < '21:00:00'), 'Time_of_reg'] = '13'
df.loc[ (df['Time_of_reg'] >= '21:00:00') & (df['Time_of_reg'] < '22:00:00'), 'Time_of_reg'] = '14'
df.loc[ (df['Time_of_reg'] >= '22:00:00') & (df['Time_of_reg'] < '23:00:00'), 'Time_of_reg'] = '15'

df.loc[ (df['Time_of_billing'] >= '08:00:00') & (df['Time_of_billing'] < '13:00:00'), 'Time_of_billing'] = '1'
df.loc[ (df['Time_of_billing'] >= '13:00:00') & (df['Time_of_billing'] < '18:00:00'), 'Time_of_billing'] = '2'
df.loc[ (df['Time_of_billing'] >= '18:00:00') & (df['Time_of_billing'] < '23:00:00'), 'Time_of_billing'] = '3'

df.loc[ (df['Time_of_Consultation'] >= '08:00:00') & (df['Time_of_Consultation'] < '13:00:00'), 'Time_of_Consultation'] = '1'
df.loc[ (df['Time_of_Consultation'] >= '13:00:00') & (df['Time_of_Consultation'] < '18:00:00'), 'Time_of_Consultation'] = '2'
df.loc[ (df['Time_of_Consultation'] >= '18:00:00') & (df['Time_of_Consultation'] < '23:00:00'), 'Time_of_Consultation'] = '3'

X = df.iloc[:, [2,3,5,10]].values
y = df.iloc[:, 12].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)

from sklearn.metrics import r2_score, mean_squared_error
test_set_rmse = (np.sqrt(mean_squared_error(y_test, y_pred)))

test_set_r2 = r2_score(y_test, y_pred)


regressor.score(X, y)
pickle.dump(regressor,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))