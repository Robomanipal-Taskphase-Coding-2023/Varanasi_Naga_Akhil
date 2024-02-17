import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'D:\\documents\\RoboManipal\\week 3\\weatherAUS.csv'
df = pd.read_csv(file_path)

# For simplicity, let's use only a subset of features and remove missing values
df = df[['Rainfall', 'Humidity3pm', 'Pressure9am', 'RainTomorrow']].dropna()

# Convert categorical values to numerical
df['RainTomorrow'] = df['RainTomorrow'].map({'No': 0, 'Yes': 1})

# Standardize numerical features
df[['Rainfall', 'Humidity3pm', 'Pressure9am']] = (
    df[['Rainfall', 'Humidity3pm', 'Pressure9am']] - df[['Rainfall', 'Humidity3pm', 'Pressure9am']].mean()
) / df[['Rainfall', 'Humidity3pm', 'Pressure9am']].std()

# Add a bias term
df['Bias'] = 1

# Split the dataset into features and target
X = df[['Bias', 'Rainfall', 'Humidity3pm', 'Pressure9am']].values
y = df['RainTomorrow'].values

# Define sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Define the cost function
def cost_function(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    return -1 / m * (y @ np.log(h) + (1 - y) @ np.log(1 - h))

# Define gradient descent function
def gradient_descent(X, y, theta, learning_rate, epochs):
    m = len(y)
    cost_history = []

    for _ in range(epochs):
        h = sigmoid(X @ theta)
        gradient = X.T @ (h - y) / m
        theta -= learning_rate * gradient
        cost = cost_function(X, y, theta)
        cost_history.append(cost)

    return theta, cost_history

# Initialize parameters
theta_initial = np.zeros(X.shape[1])

# Set hyperparameters
learning_rate = 0.01
epochs = 1000

# Run gradient descent
theta_final, cost_history = gradient_descent(X, y, theta_initial, learning_rate, epochs)

# Plot the cost over iterations
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(range(epochs), cost_history)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.title('Cost Function Over Iterations')

# Plot the sigmoid function
plt.subplot(1, 2, 2)
z_values = np.linspace(-10, 10, 100)
sigmoid_values = sigmoid(z_values)
plt.plot(z_values, sigmoid_values, color='red')
plt.xlabel('z')
plt.ylabel('sigmoid(z)')
plt.title('Sigmoid Function')

plt.show()

# Print the final parameters
print('Final Parameters:', theta_final)

# Make predictions
predictions = sigmoid(X @ theta_final)
predictions_binary = (predictions >= 0.5).astype(int)

# Print accuracy
accuracy = np.mean(predictions_binary == y)
print('Accuracy:', accuracy)
