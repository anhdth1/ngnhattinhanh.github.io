import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

img = plt.imread("a.jpeg")

width = img.shape[0]
height = img.shape[1]
print(img.shape)

img = img.reshape(width * height, 3)	#doi thanh list 1 chieu

kmeans = KMeans(n_clusters = 9).fit(img)
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

# Cach 1: Dung Ham:
# img2 = np.zeros_like(img)

# for i in range(len(img2)):
# 	img2[i] = clusters[labels[i]] 

# img2 = img2.reshape(width, height, 3)


# Cach 2: Lam thu cong:
img2 = np.zeros((width, height, 3), dtype = np.uint8)
index = 0
for i in range(width):
	for j in range(height):
		img2[i][j] = clusters[labels[index]]
		index += 1 

plt.imshow(img2)
plt.show()
