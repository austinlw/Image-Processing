# Image-Processing
Image processing scripts

Biological application:
The project uses a ratiometric sensor (mTFP and mCherry) that is under three tissue-specific promoters (neurons, tissues, intestines) in C. elegans. There are multiple lines for each tissue. The sensor is trafficked to lysosomes. mTFP changes fluorescence intensity in the physiological lysosome pH range. Therefore, a ratio of mTFP/mCherry provides a relative pH measurement (pH curve pending).

Aging_subtraction.txt:
This is a macro script used in Fiji/ImageJ. All image file in a project are opened manually before the script is run. The macro script auto creates tissue-specific subfolders. Each tissue folder contains strain-specific subfolders. Each strain-specific folder has a sample specific folder. For each image, a mask is created from mCherry and the mask is then used to extract mCherry and mTFP values. Each channel's value are saved as separate .csv files in the sample-specific folder. There are additional extra channels (ie, autofluorescence channel, brightfield, and DIC channel).

Excel handling v2.py:
This is a python script coded in Ananconda Python 3 (coded in Spyder IDE). This script goes through each tissue and strain folder, extracts the mTFP and mCherry values from the .csv files, and calculates the ratio. An aggregated excel document is created and stored in the strain folder. The program then creates various bar plots and histograms stored in the tissue-specific folders. No statistical analysis is currently used.
