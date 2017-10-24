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
from scipy.stats.stats import pearsonr

def main():
        imdir = os.path.abspath(sys.argv[1])
	outdir = os.path.abspath(sys.argv[2])
	if not os.path.exists(outdir):	
		os.makedirs(outdir)
	
	print str(datetime.datetime.now())  + " Loading reference volume.... " 
	refvol = nib.load('....nii.gz')
	refvoldata = refvol.get_data()	
	refvoldata = refvoldata[refvoldata > 0]
	refvoldata = refvoldata.flatten()
	hist_ref, bins_ref = np.histogram(refvoldata)

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
			   		   imgdata_nonzero_scale = imgdata_nonzero * get_scale_factor(imgdata_nonzero, hist_ref, bins_ref, 0, 500)
					   imgdata[idx] = imgdata_nonzero_scale
					   img2 = nib.Nifti1Image(imgdata, affine = img1.affine)
					   print str(datetime.datetime.now()) + " Saving output file...." + os.path.join(outdir, filename[:filename.find('.gz')])
					   img2.to_filename(os.path.join(outdir, filename[:filename.find('.gz')]))

def get_scale_factor(imvec, hc_ref, hv_ref, minval, maxval):
	sf_best = 1
	scalevec = [0.5, 0.1, 0.05, 0.01]	
	for id1 in scalevec:
		sfvec = sf_best*np.logspace(-id1,id1,21)
		costvec = np.full(sfvec.shape, np.nan)
		ivec = np.asarray([i for i,v in enumerate(hv_ref) if (v>=minval and v <= maxval)])
		for id1,val in enumerate(sfvec):
			hc,bins = np.histogram(val*imvec,hv_ref)
			rho,p = pearsonr(hc[ivec],hc_ref[ivec])
			costvec[id1] = 1 - rho
		sf_best = sfvec[costvec == min(costvec)]
		
	return sf_best
			

					         
if __name__ == '__main__':
        main()

