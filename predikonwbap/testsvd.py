from flask import jsonify, send_from_directory
from flask import g
import sqlite3
import os
import numpy as np
from numpy import array
from numpy import diag
from numpy import zeros
from scipy.linalg import svd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA




db = sqlite3.connect('predikon.db')
 



def query_db(query, args=(), one=False):
    cur = db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


res = query_db('SELECT municipality.id as mcp_id, vote.id as vote_id, ROUND(result.num_yes * 100.0 / result.num_total, 1)/100 AS percentage  FROM result, municipality, vote where result.municipality_id == municipality.id AND vote.id == result.vote_id ')
rows = np.zeros(len(res)).astype(np.int64)
cols = np.zeros(len(res)).astype(np.int64)
vals = np.zeros(len(res))
voteMatrix = np.zeros((2222,328))
for vote in res:
    voteMatrix[vote[0]-1,vote[1]-1] = vote[2]
print((voteMatrix[0][0]))

pca = PCA(n_components=2)
pca.fit(voteMatrix)
print(pca.components_)

def draw_vector(v0, v1, ax=None):
    ax = ax or plt.gca()
    arrowprops=dict(arrowstyle='->',
                    linewidth=2,
                    shrinkA=0, shrinkB=0)
   # ax.annotate('', v1, v0, arrowprops=arrowprops)

# plot data
plt.scatter(voteMatrix[:, 0], voteMatrix[:, 1], alpha=0.2)
for length, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(length)
    draw_vector(pca.mean_, pca.mean_ + v)
plt.axis('equal')
#voteMatrix = voteMatrix.transpose()
# Singular-value decomposition
#U, s, VT = svd(voteMatrix)
# create m x n Sigma matrix
#Sigma = zeros((voteMatrix.shape[0], voteMatrix.shape[1]))
# populate Sigma with n x n diagonal matrix
#Sigma[:voteMatrix.shape[0], :voteMatrix.shape[0]] = diag(s)
# select
#n_elements = 2
#Sigma = Sigma[:, :n_elements]
#VT = VT[:n_elements, :]
# reconstruct
#B = U.dot(Sigma.dot(VT))
#print(B)
# transform
#T = U.dot(Sigma)
#print(T)
#T = voteMatrix.dot(VT.T)
#print(T)