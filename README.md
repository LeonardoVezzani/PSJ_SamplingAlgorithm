# PSJ_SamplingAlgorithm
Point Spread Jitter is a sampling algorithm for Point Spread Function implementation in Blender. In this repository you will find both the python code to sample any given PSF and the modified cycles kernel to build blender with.

HOW TO USE THIS REPOSITORY
1) Sample several (11 is raccomanded) PSJ from a laser/star with any lens changing the laser's position while keeping the focus plane at the same distance. Remember to move the laser evenly.
2) ccrop the images as shown in the CONTAX_85mm_f1,4_@5,6 folder ( keep star proportions and a 300x300 px size).
3) in the Rayfit.py algorithm change the path for the new folder of images and run. 
4) the result will be two table that you need to copy and paste in kernel_camera.h in matrDisp and matrConv that you can find in this repository.
5) follow the instruction at "blender" to download the repository and chnge the kernel_camera with the one you just modified.
6) build the software 
7) set the sampling to CMJ, activate defocus
8) render 


