import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# Title of the app
st.title('Image Enhancement App')

# File uploader for the user to upload an image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# Function to apply image enhancement
def enhance_image(image, method):
    if method == "Blur":
        enhanced_image = cv2.GaussianBlur(image, (5, 5), 0)
    elif method == "Sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        enhanced_image = cv2.filter2D(image, -1, kernel)
    elif method == "Edge Detection":
        enhanced_image = cv2.Canny(image, 100, 200)
    return enhanced_image

# If an image is uploaded, perform enhancement
if uploaded_file is not None:
    # Convert the uploaded file to a PIL image
    image = Image.open(uploaded_file)
    # Convert PIL image to OpenCV format (BGR)
    opencv_image = np.array(image)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

    # Show the original image
    st.image(image, caption="Original Image", use_column_width=True)

    # Let user choose enhancement method
    enhancement_method = st.selectbox("Choose Enhancement Method", ["Blur", "Sharpen", "Edge Detection"])

    # Enhance the image based on the selected method
    enhanced_image = enhance_image(opencv_image, enhancement_method)

    # Convert enhanced image to RGB format for displaying in Streamlit
    enhanced_image_rgb = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB)
    enhanced_image_pil = Image.fromarray(enhanced_image_rgb)

    # Show the enhanced image
    st.image(enhanced_image_pil, caption=f"Enhanced Image ({enhancement_method})", use_column_width=True)

    # Allow the user to download the enhanced image
    download_button = st.download_button(
        label="Download Enhanced Image",
        data=enhanced_image_pil.tobytes(),
        file_name="enhanced_image.png",
        mime="image/png"
    )
