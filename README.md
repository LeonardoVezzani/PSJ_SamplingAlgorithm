# PSJ_SamplingAlgorithm
Point Spread Jitter is a sampling algorithm for Point Spread Function implementation in Blender. In this repository you will find both the python code to sample any given PSF and the modified cycles kernel to build blender with.

HOW TO USE THIS REPOSITORY:

1) Sample several (11 is raccomanded) PSFs from a laser/star with any lens as indicated in the "Adding defocusing and third-order aberrations to Ray Tracing with thePSJ algorithm" paper.

2) use the Rayfit.py algorithm ro generate the correspondinf LUTs: change line 11 and 26 to find your images.

3) copy the LUTs in kernel_camera.h in matrDisp and matrConv that you can find in this repository.

4) go at https://wiki.blender.org/wiki/Building_Blender and follow the instruction to download and build blender. Remember to substitute the kernel_camera.h found in this repo to the one in ``` C:\blender-git\blender\intern\cycles\kernel ```.

5) open the blender version you just build.

6) load any scene you want, set the sampling to CMJ, activate defocus and render (for more details check the "Adding defocusing and third-order aberrations to Ray Tracing with thePSJ algorithm" paper).


