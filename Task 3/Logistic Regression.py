import pandas as pd
data = pd.read_csv('D:\documents\RoboManipal\week 3\weatherAUS.csv')
data.head()

data.describe()
data.shape
data.info()

data = data.drop(["Evaporation","Sunshine","Cloud9am","Cloud3pm","Location", "Date"], axis =1)
data.head()

data = data.dropna(axis = 0)
data.shape
data.columns

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
data['WindDir9am'] = le.fit_transform(data['WindDir9am'])
data['WindDir3pm'] = le.fit_transform(data['WindDir3pm'])
data['RainToday'] = le.fit_transform(data['RainToday'])
data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

x = data.drop(['RainTomorrow'], axis = 1)
y = data['RainTomorrow']
x.head()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(max_iter=145460)
lr.fit(x_train,y_train)
predictions = lr.predict(x_test)
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
a=predictions[-1]
if a>=0.5:
    b='Yes'
else:
    b='No'
print('will it Rain tomorrow:',b)
print('The accuracy of the model is:',accuracy_score(y_test, predictions))


