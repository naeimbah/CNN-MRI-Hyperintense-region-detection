#! /usr/bin/python2.7 -tt

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import os.path
import commands
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import nibabel as nib
import datetime
import numpy as np
import scipy.misc
import cv2
from nipype.interfaces import fsl

def main():
        imdir = os.path.abspath(sys.argv[1])
        outdir = os.path.abspath(sys.argv[2])
        for root,_,filenames in os.walk(imdir):
                for filename in filenames:
                    if filename.endswith('.nii.gz'):
					   nii_filename = os.path.join(root, filename)
					   print nii_filename
					   img = nib.load(nii_filename)
					   img_data = img.get_data()
					   print 'number of slices: ' + str(len(img_data[1,1,:]))
					   for i in range(len(img_data[1,1,:])):
						   print "Slice number: " + str(i)
						   img_data_2d = img_data[:,:,i]
						   rows,cols = img_data_2d.shape
						   M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
						   img_data_2d = cv2.warpAffine(img_data_2d,M,(cols,rows))
						   #imgplot = plt.imshow(img_data_2d, cmap ='gray')
						   #plt.show()
						   normalizedImg = np.zeros((len(img_data[:,1,1]),len(img_data[1,:,1])))
						   img_data_2d = cv2.normalize(img_data_2d,  normalizedImg, 0, 1, cv2.NORM_MINMAX)
						   newx,newy = 4*len(img_data[:,1,1]),4*len(img_data[1,:,1])
 						   newimage = cv2.resize(img_data_2d,(newx,newy))
					 	   cv2.imshow('image',img_data_2d)
						   cv2.imshow('image',newimage)
						   group = raw_input("Press c for control, t for tumor, n for none ...")
						   while group not in ['c', 't', 'n']:
							      print 'You much choose between: c t n'
							      group = raw_input("Press c for control, t for tumor, n for none ...")
						   filename2 = filename.split('.')[-3]
						   if group == 'c':
							   imagename = outdir + '/control/' + group  + '_'  +  filename2 + '_' + str(i+1) + '.jpg'
							   scipy.misc.imsave(imagename, img_data_2d)
							   print "your choice is: control"
							   print 'save slice' + imagename
						   if group == 't':
							   imagename = outdir + '/tumor/' + group  + '_'  +  filename2 + '_' + str(i+1) + '.jpg'
							   scipy.misc.imsave(imagename, img_data_2d)
							   print "your choice is: tumor"
							   print 'save slice' + imagename
						   if group == 'n':
							   imagename = outdir + '/none/' + group + '_'  +  filename2 + '_' + str(i+1) + '.jpg'
							   scipy.misc.imsave(imagename, img_data_2d)
							   print "your choice is: none"	 
							   print 'save slice' + imagename
						   with open(os.path.join(outdir, 'log.txt'), 'a') as text_file:
								print str(group) + ',' + imagename
								text_file.write(imagename + "\n")

						         
if __name__ == '__main__':
        main()

