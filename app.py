# from dotenv import load_dotenv

# load_dotenv() # load all the environment variables from .env


# import streamlit as st
# import os
# from PIL import Image
# import google.generativeai as genai

# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# # function to load gemini pro vision


# def get_response(model, input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])

#     return response.text


# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         # read the file into bytes
#         bytes_data = uploaded_file.getvalue()

#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")



# # Initialize streamlit
# st.set_page_config(page_title='MultiLanguage Invoice Extractor')

# st.header("Multilanguage Invoice Extractor")
# input = st.text_input("Input Prompt: ", key='input')
# uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])

# image = ''
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Uploaded image', use_column_width=True)

# submit = st.button("Tell me about the invoice")


# input_prompt = """
# You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structured and accuracy in your responses.

# """
# if submit:
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     image_data = input_image_details(uploaded_file)
#     response = get_response(model, input_prompt, image_data, input)
#     st.subheader('The Resposne is')
#     st.write(response)

    
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai
import pandas as pd
# Load environment variables from .env
load_dotenv()  
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to load multiple image files
def input_image_details(uploaded_files):
    image_parts = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Read the file into bytes
            bytes_data = uploaded_file.getvalue()
            image_parts.append({
                "mime_type": uploaded_file.type,
                "data": bytes_data
            })
        return image_parts
    else:
        return None  # Handle this case in the UI

# Function to get a response from the AI model
def get_response(model, input, image, prompt):
    response = model.generate_content([input, *image, prompt])
    return response.text

# Initialize streamlit
st.set_page_config(page_title='MultiLanguage Invoice Extractor')
silos = pd.read_csv("data/silos.csv")

# Title and input elements
st.header("Multilanguage Invoice Extractor")
# input = st.text_input("Input Prompt: ", key='input')
input = """please extract all I emphasize all data  and line items and format out put to strictly json. dont aggregate simmilar or duplicated rows.. strictly to this format of  12 features don't give
 me anything else. Check for rollups and individual line items.remember this is important Folio account number is sometimes regarded as customer no or custmer p/o number. it is never ever null try and
   find it.Also vat is also never null, if it's not the vat should be 15 percent of price.You can lookup the Client Name from """ + str(silos['COOP'].values) + """.Silo Name is sometimes regarded as branch or tak.you can lookup the Silo Name from""" + str(silos['SILO NAME'].values) + """.I want only the 12 features. this is important.  12 features remember this 
   [   {  "Silo Name": "Klipdale silo", "Folio Account Number":423423,
       Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",    "Document Type": "Belasting Faktuur",     
       "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 22760.62,     "Total Excl": 22760.62,     "Vat": 3414.09,     "Total Incl": 26174.71,     "Item Description": "DAY STORAGE BREDASDORP"   },
             {   "Silo Name": "Klipdale silo",  "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",
                       "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 69193.59,     "Total Excl": 69193.59,     "Vat": 10379.04,     "Total Incl": 79572.63,     "Item Description": "DAY STORAGE NAPIER"   },
                             {  "Silo Name": "Klipdale silo",   "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",
                                   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 89199.79,     "Total Excl": 89199.79,     "Vat": 13379.97,     
                                   "Total Incl": 102579.76,     "Item Description": "DAY STORAGE KLIPDALE"   },   {  "Silo Name": "Klipdale silo", "Folio Account Number":423423,     "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   
                                   "Client":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",  "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 1000,     
                                   "Price": 39161.00,     "Total Excl": 39161.00,     "Vat": 5874.15,     "Total Incl": 45035.15,     "Item Description": "DAY STORAGE PROTEM"   },   {  "Silo Name": "Klipdale silo",  "Folio Account Number":423423,   
                                   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",  "Document Type": "Belasting Faktuur",     
                                   "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 119016.49,     "Total Excl": 119016.49,     "Vat": 17852.47,     "Total Incl": 136868.96,     
                                   "Item Description": "DAY STORAGE CALEDON"   },   {  "Silo Name": "Klipdale silo",   "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",  
                                     "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 42338.32,     "Total Excl": 42338.32,     
                                     "Vat": 6350.75,     "Total Incl": 48689.07,     "Item Description": "DAY STORAGE KRIGE"   },   {  "Silo Name": "Klipdale silo",   "Folio Account Number":423423,   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   
                                     "Client":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",  "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 40.021,     
                                     "Price": 290.00,     "Total Excl": 11605.89,     "Vat": 1740.91,     "Total Incl": 13347.00,     "Item Description": "STOCK CARRY OVER KLIPDALE"   },   
                                     {  "Silo Name": "Klipdale silo", "Folio Account Number":423423,    "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",  
                                       "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 40.100,     "Price": 290.00,     "Total Excl": 11629.00,     "Vat": 1744.35,     
                                       "Total Incl": 13373.35,     "Item Description": "STOCK CARRY OVER RIETPOEL"   },   {"Silo Name": "Klipdale silo", "Folio Account Number":423423,   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   
                                       "Client":"Overberg Agri Bedrywe (Edms) Bpk",      "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     
                                       "Units": 4952.135,     "Price": 255.00,     "Total Excl": 1263334.27,     "Vat": 189419.16,     "Total Incl": 1452753.43,     "Item Description": "LONG TERM STOCK BREDASDORP"   },  
                                         { "Silo Name": "Klipdale silo", "Folio Account Number":423423,   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",     "Invoice number": "MIVP123083083/2",   
                                         "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 716.062,     "Price": 255.00,     "Total Excl": 182555.73,     "Vat": 27389.37,     
                                         "Total Incl": 209945.10,     "Item Description": "LONG TERM STOCK KLIPDALE"   },   { "Silo Name": "Klipdale silo",   "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,  
                                           "Client":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     
                                           "Units": 650.649,     "Price": 255.00,     "Total Excl": 165914.24,     "Vat": 24887.33,     "Total Incl": 190801.57,     "Item Description": "LONG TERM STOCK PROTEM"   },   
                                           { "Silo Name": "Klipdale silo",  "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",   
                                           "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 634.116,     "Price": 255.00,     "Total Excl": 161719.78,     "Vat": 24254.94,     
                                           "Total Incl": 185974.72,     "Item Description": "LONG TERM STOCK CALEDON"   },   { "Silo Name": "Klipdale silo",  "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,  
                                             "Client":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",    
                                               "Units": 4877.681,     "Price": 255.00,     "Total Excl": 1244776.05,     "Vat": 186571.30,     "Total Incl": 1431347.35,     "Item Description": "LONG TERM STOCK RIETPOEL"   } ]"""
# Allow users to upload multiple image files
uploaded_files = st.file_uploader('Choose images of invoices...', type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# Display uploaded images
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Uploaded image: {uploaded_file.name}', use_column_width=True)

submit = st.button("Process Invoice")

# Predefined prompt
input_prompt = """
You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structure, and accuracy in your responses.
"""

# When submit is clicked
if submit:
    if uploaded_files:
        model = genai.GenerativeModel('gemini-1.5-flash')
        image_data = input_image_details(uploaded_files)
        response = get_response(model, input_prompt, image_data, input)
        print(input_prompt)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.error("Please upload at least one image file!")
