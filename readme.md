# Low-Light Image Enhancement (LLE)

## Problem Statement

Low-light conditions often result in images that are underexposed, leading to a loss of detail and poor visibility. This can be problematic in various fields, such as photography, security, and autonomous vehicles, where clear and detailed imagery is essential.

## Solution

To address this challenge, we utilized a method for enhancing low-light images, focusing on improving brightness and detail while maintaining color accuracy. Our approach is inspired by the techniques outlined in the paper **"Unsupervised Low-Light Image Enhancement via Histogram Equalization Prior"**. This method effectively enhances the visibility of low-light images without requiring paired training data, making it suitable for a wide range of real-world applications.

## Methodology

The enhancement process involves two key stages:

1. **Brightness Enhancement**:
   - We utilize a Light Up Module (LUM) that separates the low-light image into illumination and reflectance components.
   - The enhancement is guided by a Histogram Equalization Prior (HEP), which aligns the feature maps of the low-light images with those of well-lit images, effectively improving brightness and contrast.

2. **Noise Reduction**:
   - Following the brightness enhancement, a Noise Disentanglement Module (NDM) is applied to the reflectance component.
   - This module separates noise from the true image content, resulting in cleaner and more detailed output images.

This method, derived from the referenced paper, does not rely on paired datasets for training, making it highly versatile and effective across different types of low-light scenarios.

## Results

Below is an example of an image before and after applying our low-light enhancement method:

![Example of Low-Light Image Enhancement](HEP\assets\output.png)

*Image on the left: Original low-light image; Image on the right: Enhanced image using the described method.*

## Acknowledgments

This work leverages the method described in the paper **"Unsupervised Low-Light Image Enhancement via Histogram Equalization Prior."** We utilized this approach to enhance low-light images in various applications.
