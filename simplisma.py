import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

#generate some sample data array
#create random normalised gaussian functions
ncomp = 5

x0 = np.zeros(ncomp)
sigma = np.zeros(ncomp)
for i in range(ncomp):
	x0[i] = random.uniform(-100, 100)
	sigma[i] = random.uniform(3, 25)

x = np.linspace(start = -120, stop = 120, num = 2000)

gx = np.zeros((len(x),5))
plt.subplot(2, 1, 1)
for i in range(5):
	gx[:,i] = np.exp(-(x-x0[i])**2/(2*sigma[i]**2))/np.sqrt(2*np.pi*sigma[i]**2)
	plt.plot(x, gx[:,i])

#create array with random normalised linear combination of gaussian functions
nspec = 200
array = np.zeros((len(x), nspec))
idx = list(range(ncomp))

for i in range(nspec):
	randj = np.zeros(ncomp)
	random.shuffle(idx)
	for j in range(ncomp):
		randj[j] = random.uniform(0, 1-np.sum(randj))
		array[:,i] = gx[:,idx[j]]*randj[j]

#Main Algorithm
def pure(d, nr, error):

	def wmat(c,imp,irank,jvar):
		dm=np.zeros((irank+1, irank+1))
		dm[0,0]=c[jvar,jvar]
		
		for k in range(irank):
			kvar=np.int(imp[k])
			
			dm[0,k+1]=c[jvar,kvar]
			dm[k+1,0]=c[kvar,jvar]
			
			for kk in range(irank):
				kkvar=np.int(imp[kk])
				dm[k+1,kk+1]=c[kvar,kkvar]
		
		return dm

	nrow,ncol=d.shape
	
	dl = np.zeros((nrow, ncol))
	imp = np.zeros(nr)
	mp = np.zeros(nr)
	
	w = np.zeros((nr, ncol))
	p = np.zeros((nr, ncol))
	s = np.zeros((nr, ncol))
	
	error=error/100
	mean=np.mean(d, axis=0)
	error=np.max(mean)*error
	
	s[0,:]=np.std(d, axis=0)
	w[0,:]=(s[0,:]**2)+(mean**2)
	p[0,:]=s[0,:]/(mean+error)

	imp[0] = np.int(np.argmax(p[0,:]))
	mp[0] = p[0,:][np.int(imp[0])]
	
	l=np.sqrt((s[0,:]**2)+((mean+error)**2))

	for j in range(ncol):
		dl[:,j]=d[:,j]/l[j]
		
	c=np.dot(dl.T,dl)/nrow
	
	w[0,:]=w[0,:]/(l**2)
	p[0,:]=w[0,:]*p[0,:]
	s[0,:]=w[0,:]*s[0,:]
	
	print('purest variable 1: ', np.int(imp[0]+1))

	for i in range(nr-1):
		for j in range(ncol):
			dm=wmat(c,imp,i+1,j)
			w[i+1,j]=np.linalg.det(dm)
			p[i+1,j]=w[i+1,j]*p[0,j]
			s[i+1,j]=w[i+1,j]*s[0,j]
			
		imp[i+1] = np.int(np.argmax(p[i+1,:]))
		mp[i+1] = p[i+1,np.int(imp[i+1])]
		
		print('purest variable '+str(i+2)+': ', np.int(imp[i+1]+1))
		
	sp=np.zeros((nrow, nr))
			
	for i in range(nr):
		sp[0:nrow,i]=d[0:nrow,np.int(imp[i])]
		
	plt.subplot(2, 1, 2)
	plt.plot(sp)
	plt.show()
	
#Number of Spectral Components
nPure = 5
#Allowed Noise Percentage
noise = 5	

#Run Simplisma
pure(array, nPure, noise)




