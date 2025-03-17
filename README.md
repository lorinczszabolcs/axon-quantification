# Axon quantification
Repository for bouton elimination and axon skeletonization, as well as axon statistics calculation.

## Requirements

Unzip the zip containing FIJI that is attached to the latest release and open ImageJ-win64.exe from Fiji.app folder. Use this FIJI (instead of possibly already existing ones) to avoid incompatibility issues.

## Recommended file structure

```
axon_quantification - included in source .zip
│   README.md - included in source .zip, contains instructions for usage
│   LUT.csv - included in source .zip
│
└───models
│   │   .gitkeep - can be ignored (**do not delete**)
│   │   classifier_vm.model - needs to be downloaded from releases and placed here
|   |   classifier_po.model - needs to be downloaded from releases and placed here
│   
└───scripts
|   │   bouton_segmentation_batch.bsh - included in source .zip, used for creating bouton segmentation masks
|   │   multiply_tiff_mask_batch.py - included in source .zip, used for eliminating boutons based on bouton segmentation masks resulting from previous script
|   |   skeleton_batch_final.py - included in source .zip, used for creating axon skeletons on the bouton eliminated slices and calculating statistics
│   
└───data - needs to be created, contains raw isovoxel .tif files for PO and VM
|   |
|   └───nd2 - place .nd2 files here
|   |
|   └───tiff_po - needs to be created, contains raw isovoxel tif files for PO
|   |   |   MB28_01_01.tif - isovoxel tif file from animal MB28 from slice 01 and sampling site 01 (PO).
|   |   |   MB28_01_02.tif - isovoxel tif file from animal MB28 from slice 01 and sampling site 02 (PO).
|   |   |   ...
|   |
|   └───tiff_vm - needs to be created, contains raw isovoxel .tif files for VM
|   |   |   MB67_01_01.tif - isovoxel tif file from animal MB67 from slice 01 and sampling site 01 (VM).
|   |   |   MB67_01_02.tif - isovoxel tif file from animal MB67 from slice 01 and sampling site 02 (VM).
|   |   |   ...
|
└───segmentations - needs to be created, contains bouton segmentation masks for PO and VM after using bouton_segmentation_batch.bsh
|   |
|   └───segmentations_po - needs to be created, contains bouton segmentation masks for PO
|   |   |   MB28_01_01.tif - contains bouton segmentation masks from animal MB28 from slice 01 and sampling site 01 (PO).
|   |   |   MB28_01_02.tif - contains bouton segmentation masks from animal MB28 from slice 01 and sampling site 02 (PO).
|   |   |   ...
|   |
|   └───segmentations_vm - needs to be created, contains bouton segmentation masks for VM
|   |   |   MB67_01_01.tif - contains bouton segmentation masks from animal MB67 from slice 01 and sampling site 01 (VM).
|   |   |   MB67_01_02.tif - contains bouton segmentation masks from animal MB67 from slice 01 and sampling site 02 (VM).
|   |   |   ...
|
└───bouton_elim - needs to be created, contains bouton eliminated .tif files for PO and VM after using bouton_segmentation_batch.bsh and multiply_tiff_mask_batch.py
|   |
|   └───bouton_elim_po - needs to be created, contains bouton eliminated .tif files for PO
|   |   |   MB28_01_01.tif - bouton eliminated tif file from animal MB28 from slice 01 and sampling site 01 (PO).
|   |   |   MB28_01_02.tif - bouton eliminated tif file from animal MB28 from slice 01 and sampling site 02 (PO).
|   |   |   ...
|   |
|   └───bouton_elim_vm - needs to be created, contains raw isovoxel .tif files for VM
|   |   |   MB67_01_01.tif - isovoxel tif file from animal MB67 from slice 01 and sampling site 01 (VM).
|   |   |   MB67_01_02.tif - isovoxel tif file from animal MB67 from slice 01 and sampling site 02 (VM).
|   |   |   ...
|
└───skeletons - needs to be created, contains skeletons, merged max-z projections and axon statistics for PO and VM after using bouton_segmentation_batch.bsh, multiply_tiff_mask_batch.py and skeleton_batch_final.py
|   |
|   └───skeletons_po - needs to be created, contains skeletons, merged max-z projections and axon statistics for PO
|   |   |   MB28_01_01_merge.tif - merged max-z projection of original tif file and skeletons from animal MB28 from slice 01 and sampling site 01 (PO)
|   |   |   MB28_01_01_skelet.tif - 3D skeleton from animal MB28 from slice 01 and sampling site 01 (PO).
|   |   |   ...
|   |   |   results.csv - axon statistics csv file for all PO slices
|   |
|   └───skeletons_vm - needs to be created, contains skeletons, merged max-z projections and axon statistics for VM
|   |   |   MB76_01_01_merge.tif - merged max-z projection of original tif file and skeletons from animal MB67 from slice 01 and sampling site 01 (VM)
|   |   |   MB76_01_01_skelet.tif - 3D skeleton from animal MB67 from slice 01 and sampling site 01. (VM)
|   |   |   ...
|   |   |   results.csv - axon statistics csv file for all VM slices

```

## Usage

0. Download source code .zip and .model files from [releases](https://github.com/lorinczszabolcs/axon_quantification/releases/tag/v0.2.2) and place models inside models folder after unzipping the source code.

1. Open and run `export_tif_from_nd2.py` to export `.tif` files from a folder containing `.nd2` files.

  ![image](https://user-images.githubusercontent.com/13637835/203436560-e44774f8-0df0-4505-9e7f-07da16510380.png)
  - Input directory contains .nd2 files containing hyperstacks of multichannel images. The script saves each series in all hyperstacks in the output folder with the channels being split. **Make sure only those nd2 files are in the input directory that need to be processed and that the output directory is empty, because files might get overwritten.**

2. Open and run `bouton_segmentation_batch.bsh` script to detect and save bouton segmentations.

  ![image](https://user-images.githubusercontent.com/13637835/182021121-6677bea7-98e8-4d57-a9dc-95468d888bd4.png)
  - Input directory has to contain raw isovoxel TIFF files that need to be processed (either from PO or VM, **not both**). **Make sure only those tiff files are in the input directory that need to be processed, because this processing step takes quite a long time**.  
  - Output directory is the directory where the bouton segmentation masks will be saved for further usage, use separate output directories for PO and VM. **Make sure the output directory is empty, otherwise some files might get overwritten**.
  - Weka model is the trained model that is used to segment boutons. Currently there are two models, one for PO (`models/classifier_po.model`) and one for VM (`models/classifier_vm.model`), use them accordingly.
  - When segmentation is done, the output directory should contain segmentation masks of boutons (as many masks as many scans there were in the input directory).

3. Next, open and run `multiply_tiff_mask_batch.py` script to multiply segmentation masks with original tiff files. This way the boutons get eliminated.

  ![image](https://user-images.githubusercontent.com/13637835/182021466-b8070324-6ce3-4125-9108-6ae6dc826b28.png)
  - Tiff directory is the same as the input directory in the previous step. **Make sure to provide the same input directory with the same files as in the previous step**.
  - Mask directory is the same as the output directory in the previous step. **Make sure to provvide the same output directory with the same files that were the results of the previous step**.
  - Output directory is the directory containing the bouton eliminated scans. **Make sure it is empty before processing, otherwise files might get overwritten.**
  - LUT File is LUT.csv in this repository. Can provide a completely different LUT file if required.

4. Finally, open and run `skeleton_batch_final.py` to filter axons and skeletonize them, as well as calculate axon length and densities. The quantified results will be saved in a .csv file, while the max-z projected skeletons merged with the max-z projected original image will be saved in a folder to enable visual evaluation.

  ![image](https://user-images.githubusercontent.com/13637835/182021684-b351bbf4-7e38-4f2a-9b19-320e1dfa2523.png)
  - Input directory is the directory that resulted from the previous step (bouton eliminated scans). **Make sure it is the same folder containing only those images that were bouton eliminated in the previous step**.
  - Original directory is the directory that contains the original isovoxel (non-boutoneliminated) tiff files. **Make sure it contains only those images that corrrespond to the bouton eliminated images in the previous step**.
  - Output directory will contain the .csv file with the axon statistics, the 3D skeletons, as well as the max-z projected merged skeletons and original images. **Make sure it is empty before processing, otherwise some files might get overwritten**.
