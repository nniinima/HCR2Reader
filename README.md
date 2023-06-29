# Hill Climb Racing 2 Data Extraction Tool

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Start the Application](#start-the-application)
  - [GUI Overview](#gui-overview)
  - [Select Images](#select-images)
  - [Save Data](#save-data)
  - [Exiting the Application](#exiting-the-application)

## Introduction

The Hill Climb Racing 2 Data Extraction Tool is an OCR (Optical Character Recognition) application designed to extract data from screenshots captured in the popular mobile game Hill Climb Racing 2. It provides a convenient way to automatically process Team Event screenshots and extract relevant information.

By automating the data extraction process, this tool eliminates the need for manual data entry and allows teams to quickly analyze and organize their gameplay data. It is particularly useful for teams who want to track their progress, compare scores, or maintain records of their achievements.

## 1. Installation
The application requires Python version 3.8 or higher. Ensure you have Python installed on your system before proceeding with the installation.

# 1.1 Clone the Repository
Clone the repository that contains the application:

Open your terminal or command prompt.

Navigate to the directory where you want to clone the repository.

Run the following command:

<pre>
git clone https://github.com/nniinima/HCR2Reader.git
</pre>

# 1.2 Install the Required Libraries
Navigate to the cloned directory and install the required libraries using the provided requirements.txt file:

Open your terminal or command prompt.

Change to the directory where the repository was cloned.

Run the following command to install the required libraries:

<pre>
pip install -r requirements.txt
</pre>

The necessary libraries, including numpy, pandas, matplotlib, opencv-python, pytesseract, Pillow, scikit-image, tk, lxml, and Jinja2, will be installed.

# 1.3 Install Tesseract OCR
To use the OCR functionality of the application, you need to install Tesseract OCR:

Download the appropriate installer for your operating system from the Tesseract OCR GitHub repository.
Run the installer and follow the on-screen instructions to complete the installation.
Make sure to note the installation path of Tesseract OCR as you may need it in the next steps.

## 2. Usage
# 2.1 Start the Application
To start the application, open your terminal or command prompt and navigate to the cloned directory.

Run the following command:

<pre>
python HRC2ReaderGUI.py
</pre>

The application will start, and the GUI window will be displayed.

# 2.2 GUI Overview
The GUI of the application has the following sections:

Select Images: Click the "Select Images" button to choose the screenshots you want to process. 
The application accepts images with either a 20:9 or 4:3 aspect ratio.
Save Data: After the images are processed, you can save the extracted data. 
Click the "Save Data" button to choose the desired output format (csv, json, xml, or html) and save the data accordingly.
Progress Bar: The progress bar indicates the progress of image processing.
Progress Text: The progress text displays information about the currently processed image.

# 2.3 Select Images
To select images for processing:

Click the "Select Images" button.
In the file dialog, navigate to the folder containing the screenshots you want to process.
Select one or multiple image files.
Click "Open" to start processing the selected images.
The processing will begin automatically as soon as the images are selected. The progress bar and text will update accordingly.

# 2.4 Save Data
Once the images are processed, you have the option to save the extracted data in different formats (csv, json, xml, or html):

Click the "Save Data" button.
In the file dialog, choose the desired output format and specify the file name and location.
Click "Save" to save the data in the selected format.

# 2.5 Exiting the Application
To exit the application, simply close the GUI window.

Please note that the accuracy and effectiveness of the data extraction depend on the quality of the screenshots, the correctness of the image processing parameters, and the proper installation of Tesseract OCR.
