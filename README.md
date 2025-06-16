# Dementia Diagnosis with Multi-Modal Vision Transformers Using MRI and PET

Official Pytorch Implementation of Paper - 💎 DiaMond: Dementia Diagnosis with Multi-Modal Vision Transformers Using MRI and PET - Accepted by [WACV 2025](https://wacv2025.thecvf.com/)

[![Preprint](https://img.shields.io/badge/arXiv-2410.23219-b31b1b)](https://arxiv.org/abs/2410.23219)

<p align="center">
  <img src="img/arch.png" />
</p>

## Installation

1. Create environment: `conda env create -n diamond --file requirements.yaml`
2. Activate environment: `conda activate diamond`

## Data

We used data from [Alzheimer's Disease Neuroimaging Initiative (ADNI)](https://adni.loni.usc.edu/) and [Japanese Alzheimer's Disease Neuroimaging Initiative (J-ADNI)](https://pubmed.ncbi.nlm.nih.gov/29753531/). Since we are not allowed to share our data, you would need to process the data yourself. Data for training, validation, and testing should be stored in separate [HDF5](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) files, using the following hierarchical format:

1. First level: A unique identifier, e.g. image ID.
2. The second level always has the following entries:
    1. A group named `MRI/T1`, containing the T1-weighted 3D MRI data.
    2. A group named `PET/FDG`, containing the 3D FDG PET data.
    3. A string attribute `DX` containing the diagnosis labels: `CN`, `Dementia/AD`, `FTD`, or `MCI`, if available.
    4. A scalar attribute `RID` with the patient ID, if available.

## Usage

The package uses [PyTorch](https://pytorch.org). To train and test DiaMond, execute the `src/train.py` script. 
The configuration file of the command arguments is stored in `config/config.yaml`.
The essential command line arguments are:

  - `--dataset_path`: Path to HDF5 files containing either train, validation, or test data splits.
  - `--img_size`: Size of the input scan.
  - `--test`: *True* for model evaluation.


After specifying the config file, simply start training/evaluation by:
```bash
python src/train.py
```

## Contacts

For any questions, please contact: Yitong Li (yi_tong.li@tum.de)


If you find this repository useful, please consider giving a star 🌟 and citing the paper:

WACV 2025 proceedings:
```bibtex
@INPROCEEDINGS{li2024diamond,
  author={Li, Yitong and Ghahremani, Morteza and Wally, Youssef and Wachinger, Christian},
  booktitle={2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)}, 
  title={DiaMond: Dementia Diagnosis with Multi-Modal Vision Transformers Using MRI and PET}, 
  year={2025},
  volume={},
  number={},
  pages={107-116},
  doi={10.1109/WACV61041.2025.00021}}
```
