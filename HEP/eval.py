from PIL import Image
import numpy as np
import os
import skimage.metrics
import csv
from torchvision import transforms

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def save_psnr_results_csv(psnr_values, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image Name', 'PSNR (dB)'])
        for img_name, psnr_value in psnr_values:
            writer.writerow([img_name, f'{psnr_value:.2f}'])
        # Calculate and write average PSNR values
        average_psnr = np.mean([v for k, v in psnr_values]) if psnr_values else 'N/A'
        writer.writerow(['Average PSNR', f'{average_psnr:.2f}'])

def test(image_path, gt_path, csv_file):
    filelist = os.listdir(image_path)
    psnr_total = 0
    count = 0
    psnr_values = []

    for file in filelist:
        testmat_path = os.path.join(image_path, file)
        gtmat_path = os.path.join(gt_path, file)

        print(f"Loading images from:\n Test: {testmat_path}\n GT: {gtmat_path}")

        if not os.path.exists(testmat_path) or not os.path.exists(gtmat_path):
            print(f"File not found: {file}")
            continue

        testmat = Image.open(testmat_path).convert('RGB')
        gtmat = Image.open(gtmat_path).convert('RGB')
        testmat = np.array(testmat)
        gtmat = np.array(gtmat)

        # Determine window size based on image size
        min_dim = min(testmat.shape[:2])  # min height or width
        win_size = min(7, min_dim)  # Use window size 7 or the size of the smallest dimension, whichever is smaller

        # Calculate PSNR
        psnr = skimage.metrics.peak_signal_noise_ratio(testmat, gtmat)

        # Append PSNR value to the list
        psnr_values.append((file, psnr))

        psnr_total += psnr
        count += 1

    if count > 0:
        average_psnr = psnr_total / count
        print(f"Processed {count} images.")
        print(f'Mean PSNR: {average_psnr}')
        # Save results as CSV
        save_psnr_results_csv(psnr_values, csv_file)
    else:
        print('No images processed.')

if __name__ == "__main__":
    testfolder = './NDM_results/'
    gtfolder = './test_images_gt/high/'
    csv_file = 'psnr_results_1.csv'
    test(testfolder, gtfolder, csv_file)
