# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# Import necessary libraries
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

# Fetch the Google API key from environment variables and configure the Gemini API
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini model and get a response based on the input, image, and prompt
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process the uploaded image and prepare it for the Gemini model
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Prepare the image data for the Gemini model
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="Invoice Assistant")

# Set up the header and input fields for the Streamlit app
st.header("Invoice Assistant")
st.write("Upload an invoice image to extract key details such as total amount, date, and vendor information.")
uploaded_file = st.file_uploader("Upload Invoice Image", type=["jpg", "jpeg", "png"])
image = ""

# Display the uploaded image if a file is uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)
    input = st.text_input("Enter Your Query", key="input")
    
    # Create a button to trigger the invoice detail extraction
    submit = st.button("Extract Invoice Information", use_container_width=True)
    
    # Define the input prompt for the Gemini model
    input_prompt = """
                   You are an expert in understanding invoices.
                   You will receive input images as invoices & you will have to answer questions based on the input image.
                   Your responses should be accurate based on the image uploaded.
                   """
    
    # If the "Get Invoice Details" button is clicked
    if submit:
        # Process the uploaded image
        image_data = input_image_setup(uploaded_file)
        
        # Get the response from the Gemini model
        response = get_gemini_response(input_prompt, image_data, input)
        
        # Display the response in the Streamlit app
        st.subheader("Response")
        st.markdown(response)
