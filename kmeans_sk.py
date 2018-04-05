from os import listdir
import numpy as np
from sklearn.cluster import KMeans
np.random.seed(0)

# Loading image names and vectors 
print("Loading data...")
data_dir_query = '/scratch/ss8464/landmark/test'
data_dir_database = '/scratch/ss8464/landmark/index'

feature_dir_query = 'feature_query_np.npy'
feature_dir_database = 'feature_test_np.npy'

imgs_query = [i[:-4] for i in listdir(data_dir_query)]
imgs_database = [i[:-4] for i in listdir(data_dir_database)]

k = len(imgs_query)
query = np.load(feature_dir_query)
feature_size = query.shape[-1]
query = query.reshape(k, feature_size)
database = np.load(feature_dir_database).reshape(len(imgs_database), feature_size)

# Performing kmeans
print("Clustering...")
kmeans = KMeans(n_clusters=k, init=query, random_state=0, n_init=1).fit(database)
pred = np.concatenate([kmeans.predict(query), kmeans.labels_])

# Gathering clusters...
print("Collecting clusters...")
clusters = [None] * k
overwrites = 0
idx = 0
for img in imgs_query:
	cluster_id = pred[idx]
	if clusters[cluster_id] != None:
		overwrites += 1
 	
	clusters[cluster_id] = [img]
	idx += 1

failures = 0
for img in imgs_database:
	cluster_id = pred[idx]
	if clusters[cluster_id] != None:
		clusters[cluster_id].append(img)
	else:
		failures += 1
	idx += 1
		
print("Overwrites =",overwrites)
print("Failures =",failures)

# Saving clusters
print("Writing to csv...")

file = open("submission.csv","w")
file.write("id,images")
clusters = [c for c in clusters if c != None]

for cluster in clusters:
	query_img = cluster[0]
	test_imgs = cluster[1:]
	line = '\n' + query_img+',' + ' '.join(test_imgs)
	file.write(line)    

file.close()
print("Rows =",len(clusters))
print("Done")
