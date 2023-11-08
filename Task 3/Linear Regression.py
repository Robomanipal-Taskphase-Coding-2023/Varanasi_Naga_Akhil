import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from numpy.linalg import LinAlgError

# Load the dataset
data = pd.read_csv("D:\documents\RoboManipal\week 3\linear_regression_dataset.csv")
data.dropna(inplace=True)

# Extract features and target variable
X = data[['AGE', 'FEMALE', 'LOS', 'RACE', 'APRDRG']].values
y = data['TOTCHG'].values

# Standardize the features
X = (X - X.mean(axis=0)) / X.std(axis=0)

# Split the data into training and testing sets
split_ratio = 0.2
num_samples = len(y)
split_index = int((1 - split_ratio) * num_samples)

X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Add a column of ones for the intercept term
X_train = np.column_stack((np.ones(len(X_train)), X_train))
X_test = np.column_stack((np.ones(len(X_test)), X_test))

# Perform Linear Regression
try:
    weights = np.dot(np.dot(inv(np.dot(X_train.T, X_train)), X_train.T), y_train)
    y_pred_test = np.dot(X_test, weights)
    
    # Calculate evaluation metrics
    mse = np.mean((y_test - y_pred_test) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_test - y_pred_test))
    ssr = np.sum((y_test - y_pred_test) ** 2)
    sst = np.sum((y_test - np.mean(y_test)) ** 2)
    r2 = 1 - (ssr / sst)
    
    print("Mean Squared Error (MSE):", mse)
    print("Root Mean Squared Error (RMSE):", rmse)
    print("Mean Absolute Error (MAE):", mae)
    print("R-squared (R^2):", r2)
    
    # Plot the results
    plt.scatter(y_test, y_pred_test, c='blue', label='Predicted', alpha=0.5)
    plt.scatter(y_test, y_test, c='red', label='Actual', alpha=0.5)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='black', linewidth=2, label='Regression Line')
    plt.xlabel("TOTCHG")
    plt.ylabel("TOTCHG")
    plt.title("Actual vs. Predicted TOTCHG")
    plt.legend()
    plt.show()
except LinAlgError:
    print("Singular matrix - cannot compute linear regression.")

