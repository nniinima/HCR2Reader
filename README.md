# OCR Image Processing Script for HCR2

This script performs Optical Character Recognition (OCR) on PNG images, processes them, and outputs information in a sorted list.

## Prerequisites

You need to have installed:

-   **Python 3.7** or newer. If Python is not installed, download it from the [official website](https://www.python.org/downloads/).
-   **pip** (Python package installer), usually comes with Python installation.
-   **git** for cloning the repository from GitHub.

## Installation

Follow the steps below to install and run the script:

### Step 1: Clone the Repository

Clone the repository to your local machine using git.

`git clone https://github.com/nniinima/HCR2Reader.git` 

### Step 2: Install Required Python Libraries

Navigate to the cloned repository and install the required Python libraries by running the following command:

`pip install -r requirements.txt` 

### Step 3: Install Tesseract OCR

This script also requires **Tesseract OCR** to function. Download and install it from the [official GitHub repository](https://github.com/tesseract-ocr/tesseract/wiki). Ensure that it's added to your system's PATH.

On Windows, you can also define the tesseract path in your script like so:

`pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'` 

## Running the Script

To run the script, navigate to the repository directory and run:

`python HCR2ReaderGUI.py` 

This will open a graphical user interface where you can select your images. The sorting function is a work in progress, but hopefully things will come out in the right order!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Early Proof of Concept

The script does not currenlty work without specific demands. The images have to be of team events and in correct order for the script to do its job amicably. The images must be in PNG format, and taken as a screenshot with a device with 2160 x 1620 resolution. These shortcomings will be patched up, or you can patch them up yourself. This is very much a work in rogress and not a finished system.
