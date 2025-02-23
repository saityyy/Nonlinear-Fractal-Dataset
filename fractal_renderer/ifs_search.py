# -*- coding: utf-8 -*-
"""
Created on Sat Dec 09 23:56:16 2017
@author: Kazushige Okayasu, Hirokatsu Kataoka
"""

import os
import cv2
import time
import numpy as np
from ifs_simple import ifs_function
import argparse

parser = argparse.ArgumentParser(description='PyTorch fractal random search')
parser.add_argument('--rate', default=0.2, type=float, help='filling rate: (fractal pixels) / (all pixels in the image)')
parser.add_argument('--category', default=1000, type=int, help='# of category')
parser.add_argument('--numof_point', default=100000, type=int, help='# of point')
parser.add_argument('--save_dir', default='.', type=str, help='save directory')
parser.add_argument("--function_type", default="linear", type=str, help="use 'linear' or 'nonlinear' function")
args = parser.parse_args()


def cal_pix(gray):
    height, width = gray.shape
    num_pixels = np.count_nonzero(gray) / float(height * width)
    return num_pixels

# Random value generation


def generator(param, function_type):
    generators = ifs_function(function_type, prev_x=0.0, prev_y=0.0)
    for param in params:
        generators.set_param(float(param[0]), float(param[1]), float(param[2]), float(param[3]), float(param[4]), float(param[5]), float(param[6]))
    generators.calculate(args.numof_point)  # class
    img = generators.draw_point(512, 512, 6, 6, 'gray', 0)  # image (x,y pad x,y)
    return img, generators.function_V.__name__  # return by (cv2 , str)


if __name__ == "__main__":
    threshold = args.rate
    np.random.seed(1)
    class_num = 0
    data_root_dir = os.path.join(args.save_dir, "rate{}_category{}_{}".format(args.rate, args.category, args.function_type))
    if os.path.exists(data_root_dir) == False:
        os.makedirs(data_root_dir)
    img_dir = os.path.join(data_root_dir, "image")
    if os.path.exists(img_dir) == False:
        os.makedirs(img_dir)

    cat_dir = os.path.join(data_root_dir, "csv")
    if os.path.exists(cat_dir) == False:
        os.makedirs(cat_dir)

    while(class_num < args.category):  # class
        a, b, c, d, e, f, prob = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        param_size = np.random.randint(2, 8)
        params = np.zeros((param_size, 7), dtype=float)
        sum_proba = 0.0
        # Initially, this is False, parameters are saved when inverse matrix exists
        for i in range(param_size):
            a, b, c, d, e, f = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            param_rand = np.random.uniform(-1.0, 1.0, 6)
            a, b, c, d, e, f = param_rand[0:6]
            prob = abs(a*d-b*c)
            sum_proba += prob
            params[i, 0:7] = a, b, c, d, e, f, prob
        for i in range(param_size):
            params[i, 6] /= sum_proba

        fracral_img, nonlinear_function_name = generator(params, args.function_type)
        pixels = cal_pix(fracral_img[:, :, 0].copy())

        if pixels >= threshold:
            class_str = '%05d' % class_num
            fractal_name = class_str+"_"+nonlinear_function_name
            print('save: '+fractal_name)

            cv2.imwrite(os.path.join(img_dir, fractal_name + '.png'), fracral_img)
            np.savetxt(os.path.join(cat_dir, fractal_name + '.csv'), params, delimiter=',')
            class_num += 1
        else:
            pass
