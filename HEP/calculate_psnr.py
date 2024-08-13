import os
import cv2
import numpy as np
import csv
from skimage.metrics import peak_signal_noise_ratio as psnr

# Paths to directories
gt_dir = 'test_images_gt/high'
lum_results_dir = 'LUM_results'
ndm_results_dir = 'NDM_results'

# File to save PSNR results
csv_file = 'psnr_results.csv'

def calculate_psnr(img1, img2):
    return psnr(img1, img2, data_range=img1.max() - img1.min())

def process_images(gt_dir, result_dir):
    psnr_values = []
    gt_images = sorted([f for f in os.listdir(gt_dir) if f.endswith('.png')])
    result_images = sorted([f for f in os.listdir(result_dir) if f.endswith('.png')])

    if len(gt_images) != len(result_images):
        raise ValueError('Number of ground truth and result images do not match.')

    for gt_img_name, result_img_name in zip(gt_images, result_images):
        gt_img_path = os.path.join(gt_dir, gt_img_name)
        result_img_path = os.path.join(result_dir, result_img_name)

        gt_image = cv2.imread(gt_img_path, cv2.IMREAD_COLOR)
        result_image = cv2.imread(result_img_path, cv2.IMREAD_COLOR)

        if gt_image is None or result_image is None:
            raise ValueError(f'Error loading images: {gt_img_path} or {result_img_path}')

        gt_image = cv2.cvtColor(gt_image, cv2.COLOR_BGR2RGB)
        result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

        psnr_value = calculate_psnr(gt_image, result_image)
        psnr_values.append((gt_img_name, psnr_value))

    return psnr_values

def save_psnr_results_csv(lum_psnr_values, ndm_psnr_values, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image Name', 'LUM PSNR (dB)', 'NDM PSNR (dB)'])

        lum_dict = dict(lum_psnr_values)
        ndm_dict = dict(ndm_psnr_values)

        all_images = set(lum_dict.keys()).union(set(ndm_dict.keys()))

        lum_psnr_values = [v for k, v in lum_psnr_values]
        ndm_psnr_values = [v for k, v in ndm_psnr_values]

        for img_name in all_images:
            lum_psnr = lum_dict.get(img_name, 'N/A')
            ndm_psnr = ndm_dict.get(img_name, 'N/A')
            writer.writerow([img_name, f'{lum_psnr:.2f}' if lum_psnr != 'N/A' else lum_psnr,
                             f'{ndm_psnr:.2f}' if ndm_psnr != 'N/A' else ndm_psnr])

        # Calculate and write average PSNR values
        average_lum_psnr = np.mean(lum_psnr_values) if lum_psnr_values else 'N/A'
        average_ndm_psnr = np.mean(ndm_psnr_values) if ndm_psnr_values else 'N/A'
        writer.writerow(['Average PSNR', f'{average_lum_psnr:.2f}', f'{average_ndm_psnr:.2f}'])

# Calculate PSNR values for LUM results
lum_psnr_values = process_images(gt_dir, lum_results_dir)

# Calculate PSNR values for NDM results
ndm_psnr_values = process_images(gt_dir, ndm_results_dir)

# Save results as CSV
save_psnr_results_csv(lum_psnr_values, ndm_psnr_values, csv_file)

print(f'PSNR results saved to {csv_file}')
