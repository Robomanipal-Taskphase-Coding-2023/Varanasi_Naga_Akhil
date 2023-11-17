
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd


data = pd.read_csv(r'D:\documents\RoboManipal\week 3\weatherAUS.csv')
data = data.dropna(axis = 0)

y = data['RainTomorrow']
X = data.drop('RainTomorrow', axis=1)
X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

classifier = DecisionTreeClassifier()

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

date = input("Enter Date (DD-MM-YYYY): ")
location = input("Enter Location: ")
min_temp = float(input("Enter MinTemp: "))
max_temp = float(input("Enter MaxTemp: "))
rainfall = float(input("Enter Rainfall: "))
evaporation = float(input("Enter Evaporation: "))
sunshine = float(input("Enter Sunshine: "))
wind_gust_dir = input("Enter WindGustDir(N,NNE,NE,ENE,E,ESE,SE,SSE,S,SSW,SW,WSW,W,WNW,NW,NNW): ")
wind_gust_speed = int(input("Enter WindGustSpeed: "))
wind_dir_9am = input("Enter WindDir9am(N,NNE,NE,ENE,E,ESE,SE,SSE,S,SSW,SW,WSW,W,WNW,NW,NNW): ")
wind_dir_3pm = input("Enter WindDir3pm(N,NNE,NE,ENE,E,ESE,SE,SSE,S,SSW,SW,WSW,W,WNW,NW,NNW): ")
wind_speed_9am = int(input("Enter WindSpeed9am: "))
wind_speed_3pm = int(input("Enter WindSpeed3pm: "))
humidity_9am = int(input("Enter Humidity9am: "))
humidity_3pm = int(input("Enter Humidity3pm: "))
pressure_9am = float(input("Enter Pressure9am: "))
pressure_3pm = float(input("Enter Pressure3pm: "))
cloud_9am = int(input("Enter Cloud9am: "))
cloud_3pm = int(input("Enter Cloud3pm: "))
temp_9am = float(input("Enter Temp9am: "))
temp_3pm = float(input("Enter Temp3pm: "))
rain_today = input("Enter RainToday (Yes/No): ")

new_data = pd.DataFrame({
    'Date': [date],
    'Location': [location],
    'MinTemp': [min_temp],
    'MaxTemp': [max_temp],
    'Rainfall': [rainfall],
    'Evaporation': [evaporation],
    'Sunshine': [sunshine],
    'WindGustDir': [wind_gust_dir],
    'WindGustSpeed': [wind_gust_speed],
    'WindDir9am': [wind_dir_9am],
    'WindDir3pm': [wind_dir_3pm],
    'WindSpeed9am': [wind_speed_9am],
    'WindSpeed3pm': [wind_speed_3pm],
    'Humidity9am': [humidity_9am],
    'Humidity3pm': [humidity_3pm],
    'Pressure9am': [pressure_9am],
    'Pressure3pm': [pressure_3pm],
    'Cloud9am': [cloud_9am],
    'Cloud3pm': [cloud_3pm],
    'Temp9am': [temp_9am],
    'Temp3pm': [temp_3pm],
    'RainToday': [rain_today]
})
prediction = classifier.predict(new_data)
print("Predicted Rain Tomorrow:", prediction)
