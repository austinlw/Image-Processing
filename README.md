# Image-Processing
Image processing scripts

Aging_subtraction.txt:
This is a macro script used in Fiji/ImageJ. For each image, a mask is created from mCherry and the mask is then used to extract mCherry and mTFP values. Each channel's value are saved as separate .csv files. There are additional extra channels (ie, autofluorescence channel, brightfield, and DIC channel).

Excel handling v2.py:
This is a python script coded in Ananconda Python 3 (coded in Spyder IDE). This script extracts the mTFP and mCherry values from the .csv files for each sample and calculates the ratio. An aggregated excel document is created and stored in the strain folder. The program then creates various bar plots and histograms stored in the tissue-specific folders. No statistical analysis is currently used.
