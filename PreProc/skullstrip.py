
from __future__ import print_function
from builtins import str
from builtins import range

import os                                   

import nipype.interfaces.io as nio           
import nipype.interfaces.fsl as fsl          


fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

#meanfuncmask = pe.Node(interface=fsl.BET(mask=True, no_output=True,frac=0.3),name='meanfuncmask')
#preproc.connect(meanfunc, 'out_file', meanfuncmask, 'in_file')

  from nipype.interfaces import fsl
  from nipype.testing import  example_data
  btr = fsl.BET()
  btr.inputs.in_file = example_data('xxx.nii')
  btr.inputs.frac = 0.3
  res = btr.run()

