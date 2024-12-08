import streamlit as st
import time
import cv2
import numpy as np
from PIL import Image
import io

# Function to apply Gaussian Blur
def gaussian_blur(image):
    return cv2.GaussianBlur(image, (15, 15), 0)

# Function to apply Edge Detection
def edge_detection(image):
    return cv2.Canny(image, 100, 200)

# Function to apply Sharpening
def sharpen(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

# Function to adjust contrast
def adjust_contrast(image, factor=1.5):
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

# Function to adjust brightness
def adjust_brightness(image, value=50):
    return cv2.convertScaleAbs(image, alpha=1, beta=value)

# Function to invert colors
def invert_colors(image):
    return cv2.bitwise_not(image)

# Function to denoise image
def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

# Function to display logo at the start
def display_logo():
    logo = Image.open(r'C:\New folder\assets\APP LOGO.jpg')  # Correct path to your logo image
    st.image(logo, caption="Welcome to Image Enhancement App", use_column_width=True)
    time.sleep(3)  # Display for 3 seconds

# Function to play background sound (Autoplay attempt)
def play_background_sound():
    st.markdown("""
        <audio autoplay loop>
            <source src="C:/New folder/assets/BGM.mp3" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """, unsafe_allow_html=True)

# Function to display process flowchart
def display_flowchart():
    flowchart = Image.open(r'C:\New folder\assets\process_flowchart.png')  # Add your flowchart image path
    st.image(flowchart, caption="Image Enhancement Process", use_column_width=True)

# Streamlit app layout
def start_app():
    display_logo()  # Show the logo
    play_background_sound()  # Play background sound automatically

start_app()

# Streamlit title
st.title("Image Enhancement App")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open image using PIL and convert it to OpenCV format
    image = Image.open(uploaded_file)
    original_image = np.array(image)  # Keep the original image for display without modifications

    # Display original uploaded image (without any processing)
    st.image(original_image, caption="Uploaded Image", use_column_width=True)
    
    # Display the flowchart
    display_flowchart()

    # Allow user to select the enhancement technique
    enhancement_choice = st.radio("Select Enhancement Technique", [
        "Gaussian Blur (Using Gaussian filter)",
        "Edge Detection (Canny Edge Detection)",
        "Sharpen (Using sharpening filter)",
        "Contrast Adjustment (Adjust contrast levels)",
        "Brightness Adjustment (Adjust brightness levels)",
        "Invert Colors (Invert the color scheme)",
        "Denoising (Remove noise from the image)"
    ])
    
    # Apply selected enhancement
    if enhancement_choice == "Gaussian Blur (Using Gaussian filter)":
        result = gaussian_blur(original_image)
    elif enhancement_choice == "Edge Detection (Canny Edge Detection)":
        result = edge_detection(original_image)
    elif enhancement_choice == "Sharpen (Using sharpening filter)":
        result = sharpen(original_image)
    elif enhancement_choice == "Contrast Adjustment (Adjust contrast levels)":
        result = adjust_contrast(original_image)
    elif enhancement_choice == "Brightness Adjustment (Adjust brightness levels)":
        # Add brightness adjustment slider
        brightness_value = st.slider("Adjust Brightness", min_value=-100, max_value=100, value=50)
        result = adjust_brightness(original_image, brightness_value)
    elif enhancement_choice == "Invert Colors (Invert the color scheme)":
        result = invert_colors(original_image)
    elif enhancement_choice == "Denoising (Remove noise from the image)":
        result = denoise_image(original_image)
    
    # Display enhanced image
    st.image(result, caption="Enhanced Image", use_column_width=True)
    
    # Allow user to download the enhanced image
    result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    buffered = io.BytesIO()
    result_pil.save(buffered, format="JPEG")
    buffered.seek(0)

    st.download_button(
        label="Download Enhanced Image",
        data=buffered,
        file_name="enhanced_image.jpg",
        mime="image/jpeg"
    )
