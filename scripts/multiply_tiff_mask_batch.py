#@ File    (label = "Tiff directory", style = "directory") tiffFile
#@ File	   (label = "Mask directory", style = "directory") maskFile
#@ File    (label = "Output directory", style = "directory") dstFile
#@ File	   (label = "LUT file", style = "file") lutFile

import os
from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator, LutLoader

def run():
	tiffDir = tiffFile.getAbsolutePath()
	maskDir = maskFile.getAbsolutePath()
	dstDir = dstFile.getAbsolutePath()
	lutDir = lutFile.getAbsolutePath()
	process(tiffDir, maskDir, dstDir, lutDir)

def process(tiffDir, maskDir, dstDir, lutDir):
	for fileName in sorted(os.listdir(tiffDir)):
		print "Processing:"
		
		# Opening the image
		print "Open image file", fileName
		tiff_imp = IJ.openImage(os.path.join(tiffDir, fileName))
		mask_imp = IJ.openImage(os.path.join(maskDir, fileName))
		mult_imp = ImageCalculator.run(tiff_imp, mask_imp, "multiply stack")
		lut = LutLoader.openLut(lutDir)
		mult_imp.setLut(lut)
		
		if not os.path.exists(dstDir):
			os.makedirs(dstDir)
		
		print "Saving to", dstDir
		IJ.saveAs(mult_imp, "Tiff", os.path.join(dstDir, fileName))
		tiff_imp.close()
		mask_imp.close()
		mult_imp.close()

run()