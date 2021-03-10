import matplotlib.pyplot as plt
import numpy as np
import pickle


with open('oi.pickle','rb') as file:
    df = pickle.load(file) 


df = df.iloc[:,:]

dat = df.to_numpy()
col = np.linspace(1,len(df.columns),len(df.columns))
ind = np.linspace(0,len(df.index)-1,len(df.index))


X = np.array([[i for e in col] for i in ind])
Y = np.array([col for i in ind])
Z = dat

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
plt.show()
