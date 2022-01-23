from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy
from sklearn.linear_model import LinearRegression

#Variables
size_image = Image.open('CONTAX_85mm_f1,4_@5,6\StarM 1.png', 'r')
levels =20
threshold = 0
avgThree=np.full((3, 3), 1.0/9)
avgFive=np.full((5, 5), 1.0/25)
stacked = np.ndarray(shape=(size_image.size[0], size_image.size[1], 11))  # empty array
sphStacked = np.ndarray(shape=(size_image.size[0]*2, size_image.size[1]*2, 11))  # empty array
vectors =  np.ndarray(shape=(size_image.size[0]*2,levels))
linearResult =  np.ndarray(shape=(size_image.size[1]*2,levels+1,2))  # 3 per lvl Intenistà, inclinazione retta e intercetta
step = 12

#STACK IMAGES INTO 3D MATRIX
#stacking images in a 3d matrix
for s in range(11):
    s = s + 1
    source = Image.open('CONTAX_85mm_f1,4_@5,6\StarM ' + str(s) + '.png', 'r').convert('L')  # open image convertiung it to grayscal
    m = np.asarray(source)  # convert image to array
    #print(m.shape)  # print array shape
    stacked[:, :, s - 1] = m

#UNRAVEL PHI
#change of coordinate: from xyz (cartesian), to rho,phi,theta(cylindrical coordinate)
for x in range(stacked[:,1,1].size):
    x-1
    for y in range(stacked[1,:,1].size):
        y-1
        for z in range(stacked[1,1,:].size):
            z-1
            xx=x-stacked[:,1,1].size/2
            yy=y-stacked[1,:,1].size/2
            zz=z
            if (xx==0):
                xx=0.00001
            rho = math.sqrt(xx * xx + yy * yy)
            theta = np.arctan(yy / xx)

            rho = int(rho*2)
            theta = int(theta * int(stacked[1,:,1].size)/(3.1415/2) )

            if (zz < 6):
                rho=-rho
            sphStacked[rho + int(stacked[:,1,1].size/2),theta  ,int(zz)] = stacked[x,y,z]

#FIT FOR I LEVELS EACH PHI
#for each phi, select the values for intensity in i*25, then proceede to compute the average, finally linear regression is computed and the data is fitted
model=LinearRegression()
for j in range(sphStacked[1,:,1].size): #rho

    print("inizio calcolo phi Nr: ",j)
    for i in range(sphStacked[:,1,1].size):  #phi  b
        X = []
        y = []
        for l in range(sphStacked[1,1,:].size): #11 images
            for int in range(levels):   #intensity level

                pos = 0
                index = 0
                avgPos = 0
                interesting = (sphStacked[:, j, l])
                # print("interesting", interesting)
                interesting = interesting[(interesting > int * step) & (interesting < (int + 1) * step)]
                if (len(interesting) > 0):
                    # print("interesting filtered", interesting)
                    avg = np.mean(interesting)
                    # print ("avg", avg)
                    index = np.where((sphStacked[:, j, l] < ((int + 1) * step)) & (
                            sphStacked[:, j, l] > (int * step)))
                    # print("index", index)
                    pos = np.sum(index)
                    # print("pos", pos)
                    # print("Not empty: 1" ,j,l)
                    #print(index)
                    avgPos = pos / len(index[0])
                    X.append((avgPos, l))
                    #print("X:", X )
                    y.append(avg)
                    # print("y : ", y)
                    if (len(X) > 4):
                        for i in range(int):
                            model = LinearRegression().fit(X, y)
                            linearResult[j, l, 0] = model.intercept_   # here we have the density and distibution of samples  NOTE: the constant is to make the wortk easier in blender
                            #print('modelIntercept',model.intercept_)
                            linearResult[j, l, 1] = model.coef_[0] +1.1 # vector slope before changind cooridate
                            #print('modelcoef', model.coef_[0])

        del X [:]
        del y [:]



#REMOVING EMPTY LINES
removeList=[]
for line in range(linearResult[:,1,1].size):
    print("ciclo: ", line)
    if ( np.all(linearResult[line,:,1]==0)):
        print("trovata linea 0s")
        removeList.append(line)

linearCoef = np.delete(linearResult[:,:,1],removeList, 0)
linearIntercept = np.delete(linearResult[:, :, 0], removeList, 0)
linearInterceptWeighted = np.ndarray(shape = (linearIntercept[:,1].size, linearIntercept[1,:].size) )


for lvl in range(linearCoef[1,:].size):
    for line in range(linearCoef[:,1].size):
        deltaZ = linearCoef[line,lvl] * (step/2) + linearIntercept[line,lvl]
        linearInterceptWeighted[line,lvl] = (deltaZ * 10) / 6 #10 empirically determined from graphics; 6 for normalization (6th plane star focused)



#DENOISING
scipy.ndimage.median_filter(linearInterceptWeighted, size=(3,3),  output=linearInterceptWeighted, mode='nearest')

fig = plt.figure()

#PLOTTING STACKED IMAGES
#          &
#PLOTTING UNRAVELD PSF
'''
x,y,z =(stacked >  50).nonzero() #gets >100 values from stacked
ax = fig.add_subplot(221, projection='3d')
ax.scatter(x, y, z,c=stacked[x,y,z],cmap="plasma",alpha=0.2)
plt.xlabel("x px")
plt.ylabel("y px")

r,t,p =(sphStacked >10 ).nonzero()
ax = fig.add_subplot(222, projection='3d')
ax.scatter(r,t,p,c=sphStacked[r,t,p], cmap="plasma",alpha=0.1)
plt.xlabel("Rho")
plt.ylabel("Theta")'''

#PLOTTING LINEAR REGRESSION
ax = fig.add_subplot(111,projection="3d")
count =0
for phi in range(linearCoef[:,1].size):
    for i in range(linearCoef[phi,:].size):
        if (linearCoef[phi, i] != 0  and linearIntercept[phi, i] !=0 ):
            w = np.linspace(0, 11, 2)
            v = ((linearCoef[phi, i]) * w *10 + linearIntercept[phi, i])
            ax.plot(v, w, zs=phi, alpha=0.8,color =(i/(levels+2),0,0))
            plt.ylabel("Z")
            plt.xlabel("Rho")
            #count = count+1
            #print ('Count ray:', count)


#SAVING DATA

#np.savetxt('model Coef.txt', linearCoef)
#np.savetxt('model Intercept.txt', linearIntercept)

np.savetxt('intercept weighted - matrDisp Rayfit_7.4 .txt', linearInterceptWeighted, fmt='%.2f',delimiter=',', newline = '},\n{', header = '{{', footer='}}')  #THIS for D.z Variations
np.savetxt('intercept weighted - matrDisp Rayfit_7.4  SIZE.txt', linearInterceptWeighted.shape, fmt='%.0f')

interceptX= np.divide( -linearIntercept, linearCoef,  out=np.zeros_like(linearIntercept), where=linearCoef!=0)

#DENOISE INTERCEPTX
#scipy.ndimage.convolve(interceptX,avgThree,interceptX)

#scipy.ndimage.convolve(interceptX,avgThree,interceptX)
scipy.ndimage.median_filter(interceptX, size=(3,3), output=interceptX, mode='nearest')
#scipy.ndimage.median_filter(interceptX, size=(5,5), output=interceptX, mode='reflect')

np.savetxt('interceptX-matrConv Rayfit_7.4.txt',interceptX, fmt='%.2f',delimiter=',', newline = '},\n{', header = '{{', footer='}}')                        #THIS for lensuv.xy displacement
np.savetxt('interceptX-matrConv Rayfit_7.4 SIZE.txt',interceptX.shape, fmt='%.0f')

plt.show()

