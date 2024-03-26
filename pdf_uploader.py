import pandas as pd
import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as components
from PIL import Image
import io
import base64
import pytesseract
from pdf2image import convert_from_path
import cv2
import os
import tempfile
import re
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/Cellar/tesseract/5.3.4_1/bin/tesseract"


def upload_pdf_file():
    st.sidebar.markdown(f"## Welcome to the image matching tool")
    st.sidebar.info(f"Please provide file that you want to extract the text")

    uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=False)
    placeholder = st.sidebar.container()   
    option = placeholder.selectbox(f'## Select languages:',('English','Khmer'))
    if uploaded_files is not None:
        with st.expander("**Uploaded PDF**"):

            file_contents = uploaded_files.getvalue()

            base64_pdf = base64.b64encode(file_contents).decode('utf-8')
            pdf_display =  f"""<embed
            class="pdfobject"
            type="application/pdf"
            title="Embedded PDF"
            src="data:application/pdf;base64,{base64_pdf}"
            style="overflow: auto; width: 100%; height: 800px;">"""

            st.write(pdf_display, unsafe_allow_html=True)
        if option == "English":
            if st.sidebar.button("Extract"):
                show_boxes = st.sidebar.checkbox("Show Bounding Boxes", value=True)
                images = pdf_img(uploaded_files)
                # Extract text from images
                extracted_text = ""
                for image_path in images:
                    text = extract_text_from_image_english(image_path)
                    extracted_text += "\n".join(text)

                # Display the result in an expander
                with st.expander("Extracted Text"):
                    st.write(extracted_text)
                with open("extracted_text.txt", "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                with st.expander("Text with bounding boxes"):
                    pdf_box =bounding_boxes(images, show_boxes)
                    print(pdf_box)

                # Provide a download button for the text file
                st.download_button(
                    label="Download Extracted Text",
                    data=open("extracted_text.txt", "rb").read(),
                    file_name="extracted_text.txt",
                    mime="text/plain",
                )
        if option == "Khmer":
            if st.sidebar.button("Extract"):
                show_boxes = st.sidebar.checkbox("Show Bounding Boxes", value=True)
                images = pdf_img(uploaded_files)
                # Extract text from images
                extracted_text = ""
                for image_path in images:
                    text = extract_text_from_image_khmer(image_path)
                    extracted_text += "\n".join(text)

                # Display the result in an expander
                with st.expander("Extracted Text"):
                    st.write(extracted_text)
                with open("extracted_text.txt", "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                with st.expander("Text with bounding boxes"):
                    pdf_box =bounding_boxes(images, show_boxes)
                    print(pdf_box)

                # Provide a download button for the text file
                st.download_button(
                    label="Download Extracted Text",
                    data=open("extracted_text.txt", "rb").read(),
                    file_name="extracted_text.txt",
                    mime="text/plain",
                )

    else: 
        st.warning('No file uploaded!!!')    

def pdf_img(uploaded_files):
    # Create a temporary directory to store the images
    temp_dir = tempfile.mkdtemp()
    
    # Save the uploaded file to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_files.read())
    temp_file.close()
    
    # Get the file path of the temporary file
    pdf_file_path = temp_file.name
    
    # Convert PDF to images
    pages = convert_from_path(pdf_file_path, dpi=350)
    images = []
    for i, page in enumerate(pages, start=1):
        image_path = os.path.join(temp_dir, f'page{i}.jpg')
        page.save(image_path, 'JPEG')
        images.append(image_path)
    
    print("Successfully converted PDF to images")
    
    # Delete the temporary file
    os.unlink(pdf_file_path)
    
    return images

def bounding_boxes(img_list, show_boxes):
    boxes = {}
    for curr_img in img_list:
        img = cv2.imread(curr_img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, ksize=(9, 9), sigmaX=0)
        # _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilate = cv2.dilate(thresh, kernel, iterations=4)
        contours, _ = cv2.findContours(dilate, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        temp = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # print(x, y, w, h)
            if cv2.contourArea(contour) < 10000:
                continue
            temp.append([x, y, w, h])
            if show_boxes:
                cv2.rectangle(img, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
        if show_boxes:
            img = cv2.resize(img, (500, 700), interpolation=cv2.INTER_AREA)
            st.image(image=img, caption=curr_img)
            # cv2.imshow(curr_img, img)
            # cv2.waitKey(0)
        boxes[curr_img] = temp
    print('Contours saved Successfully!')
    return boxes

def extract_text_from_image_english(image):
    custom_config = r'-l eng --oem 3 --psm 4 '
    text = pytesseract.image_to_string(image,config=custom_config)
    bulleted_text = []
    lines = text.split("\n")
    for line in lines:
        # Check for bullet point symbol or line break
        if "•" in line or "\n" in line:
            bulleted_text.append("• " + line)
        else:
            bulleted_text.append(line)
    
    return bulleted_text

def extract_text_from_image_khmer(image):
    custom_config = r'-l khm+eng --oem 3 --psm 4 '
    text = pytesseract.image_to_string(image,config=custom_config).split("\n")
    return text
