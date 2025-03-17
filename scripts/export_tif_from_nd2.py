#@ File    (label = "ND2 directory", style = "directory") nd2file
#@ File    (label = "Output tif directory", style = "directory") dstFile

import os
from ij import IJ, ImagePlus
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

def run():
	nd2Dir = nd2file.getAbsolutePath()
	dstDir = dstFile.getAbsolutePath()
	process(nd2Dir, dstDir)

def process(nd2Dir, dstDir):
	for fileName in sorted(os.listdir(nd2Dir)):
		print "Processing:"
		
		# Opening the image
		print("Open nd2 file", fileName)
		options = ImporterOptions()
		options.setOpenAllSeries(True)
		options.setSplitChannels(True)
		options.setAutoscale(True)
		options.setWindowless(True)
		options.setId(os.path.join(nd2Dir, fileName))
		nd2_imps = BF.openImagePlus(options)
		# create destination dir if it dooesn't exist
		if not os.path.exists(dstDir):
			os.makedirs(dstDir)
		for nd2_imp in nd2_imps:
			nd2_imp_name = "_".join(nd2_imp.getTitle().replace(" ", "").replace(".nd2", "").split("-")[1:]).replace("(series", "_(series")
			print("Saving tiff file", nd2_imp_name)
			IJ.saveAs(nd2_imp, "Tiff", os.path.join(dstDir, nd2_imp_name))

run()