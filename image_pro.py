## Nurdogan Karaman ##
## 09.10.2019       ##

import moviepy.editor as mpy
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join

#FILTERING IMAGE
def filter():
    img_list = []
    for i in range (len(all_images)-1):
        print(i)
        # READING IMAGE
        image = cv2.imread(path_of_images + all_images[i])
        seg = cv2.imread(path_of_segments + all_images[i].split('.')[0] + '.png',cv2.IMREAD_GRAYSCALE)
        seg = (seg == 38)
        seg = np.dstack([seg])

        black_img = np.zeros((len(image), len(image[0]), 3), np.uint8)

        # SEPERATING OBJECT AND ENVIRONMENT
        image_of_the_guy = np.where(seg[:,:], image[:,:], black_img[:,:])
        image_without_the_guy = np.where(seg[:,:], black_img[:,:], image[:,:])

        # CHANGING RGB VALUES
        image_of_the_guy[:,:,1] = image_of_the_guy[:,:,1] * .2
        image = (image_without_the_guy + image_of_the_guy)

        # REVERTING RGB TO BGR COLOR SCHEME
        reverted = image[:,:,::-1]
        img_list.append(reverted)

    return img_list

#MATCHING HISTOGRAMS
def hist_match(org_img, tgt_img, mask):
    #OBTAINING DIMENSIONS OF IMAGES
    re_img = org_img.copy()

    #MATCHING HISTOGRAMS FOR 3 COLORS SEPARETLY
    color = ('r','g','b')
    for i,col in enumerate(color):
        #CALCULATING HISTOGRAMS
        org_hist = cv2.calcHist([org_img],[i],mask,[256],[0,256]) #IF IMAGE IS SEGMENTED, USES MASK
        tgt_hist = cv2.calcHist([tgt_img],[i],None,[256],[0,256])

        #CONVERTING HISTOGROMS TO CUMULATIVE FORM
        org_img_cdf = org_hist.cumsum() / org_hist.sum()
        tgt_img_cdf = tgt_hist.cumsum() / tgt_hist.sum()

        g = 256
        LUT = np.zeros((g))

        #CREATING LUT
        for k in np.arange(g):
            j = g - 1
            while True:
                LUT[k] = j
                j = j - 1
                if j < 0 or org_img_cdf[k] > tgt_img_cdf[j]:
                    break

        #MATCHING ACC TO LUT
        for m in np.arange(len(org_img)):
            for n in np.arange(len(org_img[0])):
                k = re_img[m, n, i]
                b = LUT[k]
                re_img[m, n, i] = b

    masked_img = cv2.bitwise_and(re_img, re_img, mask=mask)
    return masked_img

# APPLYING HISTOGRAM OF TARGET IMAGE
def apply_effect():
    tgt_img = cv2.imread(path_of_targets + "tom.jpg")
    img_list = []

    for i in range(len(all_images)):
        print(i)
        # READING IMAGE
        org_img = cv2.imread(path_of_images + all_images[i])
        # MATCHING HISTOGRAM
        re_img = hist_match(org_img, tgt_img, None)
        reverted = re_img[:, :, ::-1]
        img_list.append(reverted)

    return img_list

# FILTERING IMAGE
def segmented_match():
    img_list = []

    for i in range(len(all_images)):
        print(i)
        # READING IMAGE AND SEGMENT
        org_img = cv2.imread(path_of_images + all_images[i])
        seg = cv2.imread(path_of_segments + all_images[i].split('.')[0] + '.png', cv2.IMREAD_GRAYSCALE)
        black_image = np.zeros((len(org_img), len(org_img[0]), 3), np.uint8)
        re_img = black_image

        # DETERMINING SEGMENTS COUNT
        if i == 0:
            segments = np.unique(seg)
            segments = np.sort(segments)

        j = 0
        for x in segments:
            # READING TARGET IMAGE
            tgt_img = cv2.imread(path_of_targets + target_images[j])

            # CREATING MASK ACC TO GRAYSCALE VALUE
            mask = np.where(seg[:, :] == x, 255, seg[:, :]*0)

            # MATCHING HISTOGRAM
            re_img += hist_match(org_img, tgt_img, mask)
            j += 1

        # cv2.namedWindow('s', cv2.WINDOW_NORMAL)
        # cv2.imshow('s', re_img)
        # cv2.waitKey(0)

        # REVERTING RGB TO BGR COLOR SCHEME
        reverted = re_img[:, :, ::-1]
        img_list.append(reverted)

    return img_list

# CREATING VIDEO CLIP
def video_maker(img_list):
    clip = mpy.ImageSequenceClip(img_list, fps = 25)
    clip.write_videofile(path_of_outputs + 'video.mp4', codec ='mpeg4')

# LISTING NAMES OF IMAGES FROM FOLDER
path_of_targets = "C:/Users/nurdi/Desktop/targets/"
path_of_images = "C:/Users/nurdi/Desktop/DAVIS-JPEGImages/JPEGImages/shooting/"
path_of_segments = "C:/Users/nurdi/Desktop/DAVIS-JPEGImages/Annotations/shooting/"
path_of_outputs = "C:/Users/nurdi/Desktop/outputs/"

all_images = [f for f in listdir(path_of_images) if isfile(join(path_of_images, f))]
target_images = [g for g in listdir(path_of_targets) if isfile(join(path_of_targets, g))]

# PART 1
# image_list = filter()
# video_maker(image_list)

# PART 2
# image_list = apply_effect()
# video_maker(image_list)

# PART 3
# image_list = segmented_match()
# video_maker(image_list)