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

	print str(datetime.datetime.now())  + " Loading reference volume.... " 
	refvol = nib.load('....nii.gz')
	refvoldata = refvol.get_data()	
	refvoldata = refvoldata[refvoldata > 0]
	refvoldata = refvoldata.flatten()		

        for root,_,filenames in os.walk(imdir):
                for filename in filenames:
                    if filename.endswith('.nii.gz') or filename.endswith('.nii'):
					   nii_filename = os.path.join(root, filename)
					   print str(datetime.datetime.now()) + " Working on....." +  nii_filename
					   img1 = nib.load(nii_filename)
					   imgdata = img1.get_data()
					   idx = imgdata > 0
					   imgdata_nonzero = imgdata[idx]
					   imgdata_nonzero = imgdata_nonzero.flatten()
					   imgdata_nonzero_histmatch = hist_match(imgdata_nonzero, refvoldata)
					   imgdata[idx] = imgdata_nonzero_histmatch
					   img2 = nib.Nifti1Image(imgdata, affine = img1.affine)
					   print str(datetime.datetime.now()) + " Saving output file...." + os.path.join(outdir, filename[:filename.find('.gz')])
 			                   img2.to_filename(os.path.join(outdir, filename[:filename.find('.gz')]))

	

def hist_match(source, template):

	oldshape = source.shape
	source = source.ravel()
	template = template.ravel()

	# get the set of unique pixel values and their corresponding indices and
	# counts
	s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
				    return_counts=True)
	t_values, t_counts = np.unique(template, return_counts=True)

	# take the cumsum of the counts and normalize by the number of pixels to
	# get the empirical cumulative distribution functions for the source and
	# template images (maps pixel value --> quantile)
	s_quantiles = np.cumsum(s_counts).astype(np.float64)
	s_quantiles /= s_quantiles[-1]
	t_quantiles = np.cumsum(t_counts).astype(np.float64)
	t_quantiles /= t_quantiles[-1]

	# interpolate linearly to find the pixel values in the template image
	# that correspond most closely to the quantiles in the source image
	interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

	return interp_t_values[bin_idx].reshape(oldshape)
					         
if __name__ == '__main__':
        main()

