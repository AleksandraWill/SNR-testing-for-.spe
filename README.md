# SNR-testing-for-.spe
This Python-based program is designed to test the signal-to-noise ratio by saving each frame from a .spe stack as a .tiff file, analyzing the signal-to-noise ratio of each frame, and saving the analysis results in .txt format.
# Example Run
Processing .spe files and saving frames in .tiff format...
Please enter the path with your files in the .spe format: D:\testing_snr\pos1
Please select the path where the frames in .tiff format are saved: D:\testing_snr\pos1_snr
2025-07-15 14:08:29,516 - INFO - Processing D:\testing_snr\pos1\test_000_.SPE: saving each frame to .tiff format in D:\testing_snr\pos1_snr\test_000_
2025-07-15 14:08:29,538 - INFO - Total frames read: 25
2025-07-15 14:08:29,633 - INFO - Finished saving 25 frames to D:\testing_snr\pos1_snr\test_000_
...
Calculating Signal-to-Noise Ratio (SNR)...
Please provide the path with the frames in .tiff format for SNR calculation: D:\testing_snr\pos1_snr\test_000_
File: frame_0001.tiff, SNR: 2.06
File: frame_0002.tiff, SNR: 2.13
...
File: frame_0025.tiff, SNR: 2.37

Average Signal-to-Noise Ratio (SNR): 2.26
Minimum Signal-to-Noise Ratio (SNR): 2.06
Maximum Signal-to-Noise Ratio (SNR): 2.39
SNR values and statistics saved to D:\testing_snr\pos1_snr\test_000_\snr_average_min_max.txt
Do you want to calculate SNR for another directory? Type 'y' for yes and 'n' for no:
