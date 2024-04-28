import streamlit as st
import google.generativeai as genai
import base64
import os 
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()
os.environ["GOOGLE_API_KEY"] = "AIzaSyCUoCdgMITG4uss5LW2DoZpCDZZM8SqWTE"

# Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

# Initialise model
model = genai.GenerativeModel("gemini-pro-vision", generation_config=generation_config)

# Function to generate content based on image and prompt
def generate_content(image_data, mime_type, adjusted_prompt):
    # Base64 encode the image data
    encoded_image_data = base64.b64encode(image_data).decode('utf-8')

    # Creating the parts of the content as expected by the API with the adjusted prompt
    content_parts = [
        {
            "mime_type": mime_type,
            "data": encoded_image_data
        },
        {
            "text": adjusted_prompt
        }
    ]

    # Generate content based on the parts
    response = model.generate_content({"parts": content_parts})

    return response.text if response else "No response, or there was an error in the generation process."

# Main function for Streamlit app
def main():
    
    st.title("🤖 Imageers 🤖")
    st.write("Imageers engage in multitasking with images, undertaking various tasks such as summarization, captioning, and analysis, as well as extracting data from images.")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read image and determine MIME type
        image_data = uploaded_file.read()
        mime_type = "image/png" if uploaded_file.type == "image/png" else "image/jpeg"

        # Display uploaded image
        st.image(image_data, caption="Uploaded Image", use_column_width=True)

        # Additional prompt options
        with st.container():
            st.radio("Choose a prompt:", ("Default",  "Table", "JSON", "Caption", "Analysis","Summary"), key="radio")

        # Define prompts
        default = "Extract all the data from the image."

        table1 = "Extract all the data in table format."
        table2 = """
                    Extract and classify data from the image. Label each section of the output clearly as follows:
                    - Title Data: Provide the main title found in the image.
                    - Header Data: List any headings or subheadings.
                    - Chart Data: Describe any charts, including titles, axes, and key data points.
                    #- Table Data: Provide details from tables, including column names and row entries.extract other table data also.
                    -For table data: Retrieve information as follows - include column headers and the corresponding entries for each row. Also, extend the data extraction to encompass additional tables.
                    - Ensure that each section is clearly identified and separated in the output.
                    -Please ensure that each section of the output is clearly identified and formatted as requested, particularly the table data, which should be organized neatly into columns and rows.
                    #For the supplementary information provided, ensure to extract all relevant details including dates, names, and image numbers, in addition to any other pertinent data. This encompasses retrieving comprehensive information from non-tabular sources as well.
                    """
        table3 = """
                    -Extract and classify data from the image. Label each section of the output clearly as follows:
                    - Title Data: Provide the main title found in the image.
                    - Header Data: List any headings  or subheadings with their values also.
                    - Chart Data: Describe any charts, including titles, axes, and key data points.
                    ##- Table Data: Provide details from tables, including column names and row entries.extract other table data also.
                    -For table data: Retrieve information as follows - include column headers and the corresponding entries for each row. Also, extend the data extraction to encompass additional tables.
                    - Ensure that each section is clearly identified and separated in the output.
                    -Please ensure that each section of the output is clearly identified and formatted as requested, particularly the table data, which should be organized neatly into columns and rows.
                    ##For the supplementary information provided, ensure to extract all relevant details including dates, names, and image numbers, in addition to any other pertinent data. This encompasses retrieving comprehensive information from non-tabular sources as well.
                    """
        json1 = "Extract all the data in json format."
        json2 = """Extract all data from the image in JSON format.
                Include all available data, including dates, and handle duplicates appropriately.
                Preserve the original sequence of data when extracting.
                If the image contains a large amount of tabular data, ensure that all of it is extracted."""
        caption1 = "please generate the caption in short."
        caption2 = "Please create a very short caption."
        analysis = "do analysis of the image."
        summary = "generate the summary of the image."
        #additional_prompt_3 = """Summarize the key points from the image."""
        #additional_prompt_4 = """Provide detailed insights based on the image."""

        # Get selected prompt
        selected_prompt = st.session_state.radio
        # Choose the prompt based on selection
        #selected_prompt = st.selectbox("Choose a default prompt:", ("Default Prompt 1", "Default Prompt 2", "Default Prompt 3"), key="selectbox")
        if selected_prompt == "Default":
            adjusted_prompt = default
        elif selected_prompt == "Table":
            selected_prompt = st.selectbox("Choose a default prompt:", ("T1", "T2", "T3"), key="selectbox")
            if selected_prompt == "T1":
                adjusted_prompt = table1
            elif selected_prompt == "T2":
                adjusted_prompt = table2
            elif selected_prompt == "T3":
                adjusted_prompt = table3
        elif selected_prompt == "JSON":
            selected_prompt = st.selectbox("Choose a default prompt:", ("J1", "J2"), key="selectbox")
            if selected_prompt == "J1":
                adjusted_prompt = json1
            elif selected_prompt == "J2":
                adjusted_prompt = json2
        elif selected_prompt == "Caption":
            selected_prompt = st.selectbox("Choose a default prompt:", ("C1", "C2"), key="selectbox")
            if selected_prompt == "C1":
                adjusted_prompt = caption1
            elif selected_prompt == "C2":
                adjusted_prompt = caption2
        elif selected_prompt == "Analysis":
            adjusted_prompt = analysis
        elif selected_prompt == "Summary":
            adjusted_prompt = summary
	    
        # Submit button to generate content
        if st.button("Submit", key="button"):
        # Generate content based on the uploaded image and the adjusted prompt
            output = generate_content(image_data, mime_type, adjusted_prompt)

        # Display generated content
            st.subheader("Generated Content:")
            st.text_area("Content", value=output, height=400)

if __name__ == "__main__":
    main()
