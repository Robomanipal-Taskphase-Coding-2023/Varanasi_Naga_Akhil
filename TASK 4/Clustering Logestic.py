import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd


data = pd.read_csv(r'D:\documents\RoboManipal\week 3\weatherAUS.csv')


non_numeric_columns = data.select_dtypes(exclude=[np.number]).columns


numeric_data = data.drop(columns=non_numeric_columns)


numeric_data = numeric_data.dropna()


scaler = StandardScaler()
numeric_data_std = scaler.fit_transform(numeric_data)

def find_optimal_clusters(data, max_k):
    inertias = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
    
    return inertias

max_clusters = int(input('Enter Max number of clusters:'))#10
inertias = find_optimal_clusters(numeric_data_std, max_clusters)


plt.plot(range(1, max_clusters + 1), inertias, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia (Sum of squared cluster distances)')
plt.title('Elbow Method for Optimal k')
plt.show()


optimal_k = 4

kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(numeric_data_std)

print("Cluster Centers:")
print(scaler.inverse_transform(kmeans.cluster_centers_))


