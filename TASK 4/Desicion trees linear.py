from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

data = pd.read_csv("D:\documents\RoboManipal\week 3\linear_regression_dataset.csv")

y = data["TOTCHG"]

X = data[['AGE', 'FEMALE', 'LOS', 'RACE', 'APRDRG']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regressor = DecisionTreeRegressor()

regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

Age=int(input('Enter Age:'))
Female=int(input('Enter if male 0 ,if female 1:'))
Los=int(input('Enter LOS:'))
Race=1
Aprdrg=int(input('Enter APRDRG:'))

new_data = [[Age,Female,Los,Race,Aprdrg]]
prediction = regressor.predict(new_data)

print("Predicted TOTCHG:", prediction)
