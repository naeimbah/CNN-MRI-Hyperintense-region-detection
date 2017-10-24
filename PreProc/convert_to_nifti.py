#! /usr/bin/python2.7 -tt

import sys
import os.path
import commands
import dicom
import datetime

def main():
	imdir = os.path.abspath(sys.argv[1])
	outdir = os.path.abspath(sys.argv[2])
	studyID = {}
	print str(datetime.datetime.now()) + " : Creating dictionary"
	for root,_,filenames in os.walk(imdir):
		for filename in filenames:
			if commands.getstatusoutput('dcmftest \''+str(os.path.join(root,filename))+'\'')[1][0] == 'y':
				dcmheader = dicom.read_file(os.path.join(root,filename))				
				if dcmheader.SeriesInstanceUID not in studyID:
					studyID[dcmheader.SeriesInstanceUID] = os.path.join(root,filename)

	for uid in studyID:
		dcm = studyID[uid]
		dcmheader = dicom.read_file(dcm)
		print str(datetime.datetime.now()) + " :  " + dcmheader.PatientID.strip() + " : " + dcmheader.ContentDate.strip()
		commands.getstatusoutput("mri_convert " + dcm + " " + os.path.join(outdir,dcmheader.PatientID.strip()) + "_" + dcmheader.ContentDate.strip() + ".nii")

if __name__ == '__main__':
	main()
