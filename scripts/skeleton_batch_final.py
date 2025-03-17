#@ File    (label = "Input directory", style = "directory") srcFile
#@ File	   (label = "Original directory", style = "directory") origFile
#@ File    (label = "Output directory", style = "directory") dstFile

import os
from os.path import join
from ij import IJ, ImagePlus, WindowManager
from ij.plugin.filter import Analyzer
from ij.process.ImageProcessor import BLACK_AND_WHITE_LUT
import csv

thlow = 5
thup = 255

def run():
	srcDir = srcFile.getAbsolutePath()
	origDir = origFile.getAbsolutePath()
	dstDir = dstFile.getAbsolutePath()
	process(srcDir, origDir, dstDir)

def process(srcDir, origDir, dstDir):
	
	# create destination dir if it dooesn't exist
	if not os.path.exists(dstDir):
		os.makedirs(dstDir)
		
	with open(join(dstDir, 'results.csv'), 'a') as f:
	
		# open csv for writing results and write header
		csvWriter = csv.writer(f, delimiter=',')
		csvWriter.writerow(['name', 'axon density', 'axon length', 'volume'])
	
		for fileName in sorted(os.listdir(srcDir)):
			print "Processing:"
			
			IJ.run("Select None")
			IJ.run("Clear Results")
			
			# Opening the image
			print "Open image file", fileName
			IJ.open(os.path.join(origDir, fileName))
			orig_imp = WindowManager.getCurrentImage()
			orig_imp_title = orig_imp.getTitle()
			
			IJ.open(os.path.join(srcDir, fileName))
			src_imp = WindowManager.getCurrentImage()
			src_imp_title = src_imp.getTitle()
			
			# calculate volume in physical units
			w, h, _, sl, _ = ImagePlus.getDimensions(src_imp)
			cal = src_imp.getCalibration()
			w_phys, h_phys, sl_phys = cal.getX(w), cal.getY(h), cal.getZ(sl)
			vol = w_phys * h_phys * sl_phys
			
			# run tubeness filtering
			IJ.run(src_imp, "Tubeness", "sigma=0.32 use")
			tub_imp = WindowManager.getCurrentImage()
			tub_imp_title = tub_imp.getTitle()
			
			# convert to 8-bit
			bD = tub_imp.getProcessor().getBitDepth()
			if bD > 8:
				IJ.run(tub_imp, "8-bit", "")
				tub_eightbit_imp = WindowManager.getCurrentImage()
			
			# bilateral filtering
			IJ.run(tub_imp, "Bilateral Filter", "spatial=15 range=200")
			bilat_imp = WindowManager.getCurrentImage()
			bilat_imp_title = bilat_imp.getTitle()
	
			# thresholding and creating mask
			bilat_imp.getProcessor().setThreshold(thlow, thup, BLACK_AND_WHITE_LUT)
			Analyzer.setOption("BlackBackground", False)
			IJ.run(bilat_imp, "Convert to Mask", "method=Default background=Dark black")
			mask_imp = WindowManager.getCurrentImage()
			mask_imp_title = mask_imp.getTitle()
			
			# creating skeleton
			IJ.run("Skeletonize (2D/3D)")
			skelet_imp = WindowManager.getCurrentImage()
			skelet_imp_title = skelet_imp.getTitle()
				
			dilate_imps = []
			dilate_imp_titles = []
			for i in range(2):
				IJ.run(skelet_imp, "Dilate (3D)", "iso=255")
				dilate_imps.append(WindowManager.getCurrentImage())
				dilate_imp_titles.append(dilate_imps[i].getTitle())
			
			IJ.run("Skeletonize (2D/3D)")
			skelet_final_imp = WindowManager.getCurrentImage()
			skelet_final_imp_title = skelet_final_imp.getTitle()
			IJ.saveAs(skelet_final_imp, "Tiff", os.path.join(dstDir, fileName.split('.')[0] + '_skelet'))
			
			IJ.run("Analyze Skeleton (2D/3D)", "prune=none show")
			table = WindowManager.getActiveTable().getResultsTable()
			table_title = table.getTitle()
			table.sort("Branch length")
			length = 0
			
			for row in range(len(table.getColumn(1))):
				length = length + table.getColumn(1)[row]
			
			print "Saving to", dstDir
				
			# write axon densitites, lengths and volumes
			csvWriter.writerow([fileName, str(1000. * length / vol), str(length), str(vol)])
			
			# select original image, z project and save
			IJ.selectWindow(orig_imp_title)
			IJ.run("Z Project...", "projection=[Max Intensity]")
			IJ.run("8-bit", "")
			orig_z_imp = WindowManager.getCurrentImage()
			orig_z_imp_title = orig_z_imp.getTitle()
			
			# select original image, z project and save
			IJ.selectWindow(fileName.split('.')[0] + '_skelet.tif')
			IJ.run("Z Project...", "projection=[Max Intensity]")
			skelet_final_z_imp = WindowManager.getCurrentImage()
			skelet_final_z_imp_title = skelet_final_z_imp.getTitle()
			
			IJ.run("Merge Channels...", "c1="+ skelet_final_z_imp_title + " c2=" + orig_z_imp_title + " create");
			merge_imp = WindowManager.getCurrentImage()
			IJ.saveAs(merge_imp, "Tiff", os.path.join(dstDir, fileName.split('.')[0] + '_merge'))
			
			
			close_window(src_imp)
			close_window(orig_imp)
			close_window(tub_imp)
			close_window(tub_eightbit_imp)
			close_window(bilat_imp)
			close_window(mask_imp)
			close_window(skelet_imp)
			for i in range(2):
				close_window(dilate_imps[i])
			close_window(skelet_final_imp)
			close_window(orig_z_imp)
			close_window(skelet_final_z_imp)
			close_window(merge_imp)
			IJ.selectWindow("Branch information")
			IJ.run("Close")
			IJ.selectWindow("Results")
			IJ.run("Close")
			IJ.selectWindow("Tagged skeleton")
			IJ.run("Close")

def close_window(imp):
	imp.changes = False
	imp.close()

run()