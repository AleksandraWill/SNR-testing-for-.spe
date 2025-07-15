import subprocess
import os
import sys
import pims
import numpy as np
import cv2
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_input_subfolder(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        os.makedirs(self.input_subfolder, exist_ok=True)
        return func(self, *args, **kwargs)
    return wrapper

class SPEProcessor:
    def __init__(self, spe_file_path, input_subfolder):
        self.spe_file_path = spe_file_path
        self.input_subfolder = input_subfolder

    @create_input_subfolder
    def process_spe_file(self):
        logging.info(f"Processing {self.spe_file_path}: saving each frame to .tiff format in {self.input_subfolder}")

        # Read the SPE file
        frames = pims.open(self.spe_file_path)
        num_frames = len(frames)
        logging.info(f"Total frames read: {num_frames}")

        for i, frame in enumerate(frames, start=1):
            # Convert to uint16 if necessary
            if frame.dtype != np.uint16:
                frame = (frame / frame.max() * 65535).astype(np.uint16)

            # Save the frame
            input_path = os.path.join(self.input_subfolder, f"frame_{i:04d}.tiff")
            cv2.imwrite(input_path, frame)

        logging.info(f"Finished saving {num_frames} frames to {self.input_subfolder}")

class SPEBatchProcessor:
    def __init__(self, input_root, input_subroot):
        self.input_root = input_root
        self.input_subroot = input_subroot

    def process_all_spe_files(self):
        for root, _, files in os.walk(self.input_root):
            for file in files:
                if file.endswith('.spe') or file.endswith('.SPE'):
                    spe_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, self.input_root)
                    input_path = os.path.join(self.input_subroot, os.path.splitext(file)[0])
                    processor = SPEProcessor(spe_file_path, input_path)
                    processor.process_spe_file()

def extract_snr(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Calculate the Signal-to-Noise Ratio (SNR)
    snr = np.mean(image) / np.std(image) if np.std(image) != 0 else float('inf')  # Avoid division by zero

    return snr

def extract_snr_from_directory(directory_path):
    all_snr = []
    total_snr = 0
    count = 0

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path) and filename.lower().endswith('.tiff'):
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

            if image is None:
                print(f"Warning: {filename} could not be loaded properly.")
                continue

            snr = extract_snr(file_path)
            all_snr.append({'filename': filename, 'snr': snr})
            total_snr += snr
            count += 1

    average_snr = total_snr / count if count != 0 else 0
    min_snr = min(all_snr, key=lambda x: x['snr'])['snr'] if count != 0 else float('inf')
    max_snr = max(all_snr, key=lambda x: x['snr'])['snr'] if count != 0 else float('-inf')

    return all_snr, average_snr, min_snr, max_snr

def process_spe_files():
    # Ask user for input and output directories
    while True:
        input_root = input('Please enter the path with your files in the .spe format: ')
        if os.path.isdir(input_root):
            break
        print("The specified path does not exist. Please try again.")

    while True:
        input_subroot = input('Please select the path where the frames in .tiff format are saved: ')
        if os.path.isdir(input_subroot):
            break
        print("The specified path does not exist. Please try again.")

    batch_processor = SPEBatchProcessor(input_root, input_subroot)
    batch_processor.process_all_spe_files()

def calculate_snr():
    while True:
        directory_path = input("Please provide the path with the frames in .tiff format for SNR calculation: ")

        if not os.path.isdir(directory_path):
            print("The specified path does not exist. Please try again.")
            continue

        snr_list, average_snr, min_snr, max_snr = extract_snr_from_directory(directory_path)

        # Display the SNR values
        for snr_data in snr_list:
            print(f"File: {snr_data['filename']}, SNR: {snr_data['snr']:.2f}")

        # Display the average, min, and max SNR
        print(f"\nAverage Signal-to-Noise Ratio (SNR): {average_snr:.2f}")
        print(f"Minimum Signal-to-Noise Ratio (SNR): {min_snr:.2f}")
        print(f"Maximum Signal-to-Noise Ratio (SNR): {max_snr:.2f}")

        # Save the SNR values to a text file
        snr_file_path = os.path.join(directory_path, "snr_average_min_max.txt")
        with open(snr_file_path, 'w') as snr_file:
            for snr_data in snr_list:
                snr_file.write(f"{snr_data['filename']}: SNR = {snr_data['snr']:.2f}\n")
            snr_file.write(f"\nAverage Signal-to-Noise Ratio (SNR): {average_snr:.2f}\n")
            snr_file.write(f"Minimum Signal-to-Noise Ratio (SNR): {min_snr:.2f}\n")
            snr_file.write(f"Maximum Signal-to-Noise Ratio (SNR): {max_snr:.2f}\n")

        print(f"SNR values and statistics saved to {snr_file_path}")

        # Ask the user if they want to continue
        continue_choice = input("Do you want to calculate SNR for another directory? Type 'y' for yes and 'n' for no: ").strip().lower()
        if continue_choice != 'y':
            break

def main():
    print("Processing .spe files and saving frames in .tiff format...")
    process_spe_files()

    print("Calculating Signal-to-Noise Ratio (SNR)...")
    calculate_snr()

if __name__ == "__main__":
    main()