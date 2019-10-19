# image_processing
I wrote an code that manipulate the RGB values of images

In this code, I used image sequences from [DAVIS Challenge](https://davischallenge.org) which is a dataset originally created for semantic segmentation. You can download the [TrainVal](https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-Unsupervised-trainvalFull-Resolution.zip) set which contains image sets and their semantic annotations.

In the part 1, Code masks the segmented area of the image and changes its RGB value\
In the part 2, By "Histogram Matching" the original images' histogram are fitted to the target images' histogram.\
In the part 3, Also by "Histogram Matching" different segments of images are fitted to different target images by using image mask.
