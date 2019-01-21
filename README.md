
# pose2pose

This is [\<everybody  dance  now\>](https://arxiv.org/pdf/1808.07371.pdf) python implementation

pose2pose is [pix2pix](https://github.com/affinelayer/pix2pix-tensorflow) based video style(pose) tranfer.

It learns poses from a video, and translates your pose to the trained pose.  

This repository is based on [GordonRen's repository](https://github.com/GordonRen/pose2pose). This one does not use [PyOpenPose](https://github.com/FORTH-ModelBasedTracker/PyOpenPose/issues/10) which is custom python wrapper of [openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose). So it's easier to be built in Windows system.

## Getting Started

#### 1. Build [openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
Build openpose with instruction documents of openpose python module API.
Then you will get openpose libraries include `pyopenpose.lib`.

#### 2. Put all libraries in `libs` folder.

#### 3. Set an environment variable.
Set `OPENPOSE_ROOT` which includes `models` folder.  This is necessary to use pretrained models of openpose.

In Windows system, you can set with the command below.
```
set %OPENPOSE_ROOT%=YOUR_OPENPOSE_DIR 
```

## Usage

#### 1. Generate Training Data
```
python generate_train_data.py --file My_Video.mp4
```

This operation will create `original` and `landmarks`.

#### 2. Train Model

```
# Clone the repo from Christopher Hesse's pix2pix TensorFlow implementation
git clone https://github.com/affinelayer/pix2pix-tensorflow.git

# Move the original and landmarks folder into the pix2pix-tensorflow folder
mv pose2pose/landmarks pose2pose/original pix2pix-tensorflow/photos_pose

# Go into the pix2pix-tensorflow folder
cd pix2pix-tensorflow/

# Reset to april version
git reset --hard d6f8e4ce00a1fd7a96a72ed17366bfcb207882c7

# Resize original images
python tools/process.py \
  --input_dir photos_pose/original \
  --operation resize \
  --output_dir photos_pose/original_resized
  
# Resize landmark images
python tools/process.py \
  --input_dir photos_pose/landmarks \
  --operation resize \
  --output_dir photos_pose/landmarks_resized
  
# Combine both resized original and landmark images
python tools/process.py \
  --input_dir photos_pose/landmarks_resized \
  --b_dir photos_pose/original_resized \
  --operation combine \
  --output_dir photos_pose/combined
  
# Split into train/val set
python tools/split.py \
  --dir photos_pose/combined
  
# Train the model on the data
python pix2pix.py \
  --mode train \
  --output_dir pose2pose-model \
  --max_epochs 1000 \
  --input_dir photos_pose/combined/train \
  --which_direction AtoB
```

Trainning takes quite a lot of time. Recommend to use gpu.

#### 3. Export Model

2019-01-22 : on writting.
