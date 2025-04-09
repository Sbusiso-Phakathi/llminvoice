# import os
# from dotenv import load_dotenv
# import streamlit as st
# from PIL import Image
# import google.generativeai as genai
# import pandas as pd
# import json
# import re


# # Load environment variables from .env
# load_dotenv()  
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # Function to load multiple image files
# def input_image_details(uploaded_files):
#     image_parts = []
#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             # Read the file into bytes
#             bytes_data = uploaded_file.getvalue()
#             image_parts.append({
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             })
#         return image_parts
#     else:
#         return None  # Handle this case in the UI

# # Function to get a response from the AI model
# def get_response(model, input, image, prompt):
#     response = model.generate_content([input, *image, prompt])
#     return response.text

# # Initialize streamlit
# st.set_page_config(page_title=' Invoice Extractor')
# silos = pd.read_csv("data/silos.csv")
# folios = pd.read_csv("data/folios.csv")

# # Title and input elements
# st.header("Multilanguage Invoice Extractor")
# # input = st.text_input("Input Prompt: ", key='input')

# uploaded_files = st.file_uploader('Choose images of invoices...', type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# # Display uploaded images
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         image = Image.open(uploaded_file)
#         st.image(image, caption=f'Uploaded image: {uploaded_file.name}', use_column_width=True)

# submit = st.button("Process Invoice")

# # Predefined prompt
# input_prompt = """
# You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structure, and accuracy in your responses.
# """

 
# if submit:
#     if uploaded_files:
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         image_data = input_image_details(uploaded_files)
#         response = get_response(model, input_prompt, image_data, input)

#         st.subheader('The Response is')
#         st.write(response)  # Show raw response in case parsing fails

#         try:
#             # Extract JSON-like content from the response using regex
#             json_match = re.search(r'\[.*\]', response, re.DOTALL)

#             if json_match:
#                 json_data = json_match.group(0)
#                 parsed_json = json.loads(json_data)
#                 df = pd.DataFrame(parsed_json)

#                 st.subheader("Extracted Invoice Data")
#                 st.dataframe(df)
#             else:
#                 st.warning("No valid JSON array found in the response.")
#         except Exception as e:
#             st.error(f"Failed to parse JSON from response: {e}")


#     else:
#         st.error("Please upload at least one image file!")



# import os
# from dotenv import load_dotenv
# import streamlit as st
# from PIL import Image, UnidentifiedImageError
# import google.generativeai as genai
# import pandas as pd
# import json
# import re

# # Load environment variables from .env
# load_dotenv()
# api_key = os.getenv('GOOGLE_API_KEY')

# if not api_key:
#     st.error("GOOGLE_API_KEY is not set in the environment.")
#     st.stop()

# try:
#     genai.configure(api_key=api_key)
# except Exception as e:
#     st.error(f"Failed to configure Gemini API: {e}")
#     st.stop()

# # Load supporting data
# try:
#     silos = pd.read_csv("data/silos.csv")
#     folios = pd.read_csv("data/folios.csv")
# except FileNotFoundError as e:
#     st.error(f"Data file not found: {e}")
#     st.stop()
# except Exception as e:
#     st.error(f"Error loading CSV files: {e}")
#     st.stop()

# # Function to load image parts
# def input_image_details(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         try:
#             bytes_data = uploaded_file.getvalue()
#             image_parts.append({
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             })
#         except Exception as e:
#             st.warning(f"Failed to process image {uploaded_file.name}: {e}")
#     return image_parts if image_parts else None

# # Function to get response from Gemini
# def get_response(model, input_text, image_parts, prompt):
#     try:
#         response = model.generate_content([input_text, *image_parts, prompt])
#         return response.text
#     except Exception as e:
#         st.error(f"Error generating content from Gemini: {e}")
#         return None

# # Streamlit UI Setup
# st.set_page_config(page_title='Invoice Extractor')
# st.header("Multilanguage Invoice Extractor")

# uploaded_files = st.file_uploader(
#     'Choose images of invoices...', 
#     type=['jpg', 'jpeg', 'png'], 
#     accept_multiple_files=True
# )

# # Display uploaded images
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         try:
#             image = Image.open(uploaded_file)
#             st.image(image, caption=f'Uploaded: {uploaded_file.name}', use_column_width=True)
#         except UnidentifiedImageError:
#             st.warning(f"Could not open image: {uploaded_file.name}")

# submit = st.button("Process Invoice")

# # Construct full prompt with data
# input_prompt = """
# You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structure, and accuracy in your responses.
# """
# # Append data-driven instructions
# # input_prompt += f"\nFolio Account Numbers: {folios['Folio'].values}"
# # input_prompt += f"\nSupplier Names: {folios['NEXGRO COMPANY'].values}"
# # input_prompt += f"\nClient Company Names: {silos['COOP'].values}"
# # input_prompt += f"\nSilo Names: {silos['SILO NAME'].values}"

# input = """please extract all I emphasize all data  and line items and format out put to strictly json. dont aggregate simmilar or duplicated rows.. strictly to this format of  12 features don't give
#  me anything else. Check for rollups and individual line items.remember this is important Folio account number is sometimes regarded as customer no or custmer p/o number. it is never ever null try and
#    find it.Also vat is also never null, if it's not the vat should be 15 percent of price.You can lookup the folio account number  from """ + str(folios['Folio'].values) + """ + You can lookup the Supplier Name from """ + str(folios['NEXGRO COMPANY'].values) + """ + You can also lookup the Client Company Name from """ + str(silos['COOP'].values) + """.Silo Name is sometimes regarded as branch or tak.you can lookup the Silo Name from""" + str(silos['SILO NAME'].values) + """.I want only the 12 features. this is important.  12 features remember this 
#    [   {  "Silo Name": "Klipdale silo", "Folio Account Number":423423,
#        Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",    "Document Type": "Belasting Faktuur",     
#        "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 22760.62,     "Total Excl": 22760.62,     "Vat": 3414.09,     "Total Incl": 26174.71,  "Total Invoice": 186174.71,   "Item Description": "DAY STORAGE BREDASDORP"   },
#              {   "Silo Name": "Klipdale silo",  "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",
#                        "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 69193.59,     "Total Excl": 69193.59,     "Vat": 10379.04,     "Total Incl": 79572.63, "Total Invoice": 186174.71,    "Item Description": "DAY STORAGE NAPIER"   },
#                              {  "Silo Name": "Klipdale silo",   "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",
#                                    "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 89199.79,     "Total Excl": 89199.79,     "Vat": 13379.97,     
#                                    "Total Incl": 102579.76, "Total Invoice": 186174.71,     "Item Description": "DAY STORAGE KLIPDALE"   },   {  "Silo Name": "Klipdale silo", "Folio Account Number":423423,     "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   
#                                    "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",  "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 1000,     
#                                    "Price": 39161.00,     "Total Excl": 39161.00,     "Vat": 5874.15,     "Total Incl": 45035.15, "Total Invoice": 186174.71,    "Item Description": "DAY STORAGE PROTEM"   },   {  "Silo Name": "Klipdale silo",  "Folio Account Number":423423,   
#                                    "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",  "Document Type": "Belasting Faktuur",     
#                                    "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 119016.49,     "Total Excl": 119016.49,     "Vat": 17852.47,     "Total Incl": 136868.96, "Total Invoice": 186174.71,    
#                                    "Item Description": "DAY STORAGE CALEDON"   },   {  "Silo Name": "Klipdale silo",   "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",  
#                                      "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 1000,     "Price": 42338.32,     "Total Excl": 42338.32,     
#                                      "Vat": 6350.75,     "Total Incl": 48689.07, "Total Invoice": 186174.71,    "Item Description": "DAY STORAGE KRIGE"   },   {  "Silo Name": "Klipdale silo",   "Folio Account Number":423423,   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   
#                                      "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",   "Invoice number": "MIVP123083083/2",  "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 40.021,     
#                                      "Price": 290.00,     "Total Excl": 11605.89,     "Vat": 1740.91,     "Total Incl": 13347.00, "Total Invoice": 186174.71,    "Item Description": "STOCK CARRY OVER KLIPDALE"   },   
#                                      {  "Silo Name": "Klipdale silo", "Folio Account Number":423423,    "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",  
#                                        "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 40.100,     "Price": 290.00,     "Total Excl": 11629.00,     "Vat": 1744.35,     
#                                        "Total Incl": 13373.35, "Total Invoice": 186174.71,    "Item Description": "STOCK CARRY OVER RIETPOEL"   },   {"Silo Name": "Klipdale silo", "Folio Account Number":423423,   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   
#                                        "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",      "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     
#                                        "Units": 4952.135,     "Price": 255.00,     "Total Excl": 1263334.27,     "Vat": 189419.16,     "Total Incl": 1452753.43, "Total Invoice": 186174.71,    "Item Description": "LONG TERM STOCK BREDASDORP"   },  
#                                          { "Silo Name": "Klipdale silo", "Folio Account Number":423423,   "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",     "Invoice number": "MIVP123083083/2",   
#                                          "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 716.062,     "Price": 255.00,     "Total Excl": 182555.73,     "Vat": 27389.37,     
#                                          "Total Incl": 209945.10, "Total Invoice": 186174.71,    "Item Description": "LONG TERM STOCK KLIPDALE"   },   { "Silo Name": "Klipdale silo",   "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,  
#                                            "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     
#                                            "Units": 650.649,     "Price": 255.00,     "Total Excl": 165914.24,     "Vat": 24887.33,     "Total Incl": 190801.57, "Total Invoice": 186174.71,    "Item Description": "LONG TERM STOCK PROTEM"   },   
#                                            { "Silo Name": "Klipdale silo",  "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,   "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",   
#                                            "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",     "Units": 634.116,     "Price": 255.00,     "Total Excl": 161719.78,     "Vat": 24254.94,     
#                                            "Total Incl": 185974.72,  "Total Invoice": 186174.71,   "Item Description": "LONG TERM STOCK CALEDON"   },   { "Silo Name": "Klipdale silo",  "Folio Account Number":423423,  "Supplier": "AFRICAN GRAIN INVESTMENTS (PTY)" ,  
#                                              "Client Company":"Overberg Agri Bedrywe (Edms) Bpk",    "Invoice number": "MIVP123083083/2",   "Document Type": "Belasting Faktuur",     "Invoice Date": "2024-10-30",    
#                                                "Units": 4877.681,     "Price": 255.00,     "Total Excl": 1244776.05,     "Vat": 186571.30,     "Total Incl": 1431347.35,   "Total Invoice": 186174.71,  "Item Description": "LONG TERM STOCK RIETPOEL"   } ]"""




# if submit:
#     if not uploaded_files:
#         st.error("Please upload at least one image file.")
#     else:
#         image_data = input_image_details(uploaded_files)

#         if not image_data:
#             st.error("Failed to load image data.")
#         else:
#             model = genai.GenerativeModel('gemini-1.5-flash')
#             response = get_response(model, input_prompt, image_data, input)

#             if response:
#                 st.subheader('The Response is')
#                 st.write(response)  # Helpful for debugging

#                 try:
#                     json_match = re.search(r'\[.*?\]', response, re.DOTALL)
#                     if json_match:
#                         json_data = json_match.group(0)
#                         parsed_json = json.loads(json_data)
#                         df = pd.DataFrame(parsed_json)
#                         st.subheader("Extracted Invoice Data")
#                         csv_file = "data/nexgrodata.csv"
#                         df.to_csv(csv_file, mode='a', index=False, header=not pd.io.common.file_exists(csv_file))
#                         st.dataframe(df)
#                     else:
#                         st.warning("No JSON array found in the response.")
#                 except json.JSONDecodeError as e:
#                     st.error(f"JSON decoding error: {e}")
#                 except Exception as e:
#                     st.error(f"Unexpected error parsing response: {e}")


# import os
# from dotenv import load_dotenv
# import streamlit as st
# from PIL import Image, UnidentifiedImageError
# import google.generativeai as genai
# import pandas as pd
# import json
# import re
# import time

# # Load API key
# load_dotenv()
# api_key = os.getenv('GOOGLE_API_KEY')
# if not api_key:
#     st.error("GOOGLE_API_KEY not found in environment.")
#     st.stop()

# try:
#     genai.configure(api_key=api_key)
# except Exception as e:
#     st.error(f"Gemini configuration error: {e}")
#     st.stop()

# # Load support CSVs
# try:
#     silos = pd.read_csv("data/silos.csv")
#     folios = pd.read_csv("data/folios.csv")
#     grade_cost = pd.read_csv("data/cost-grades.csv")

# except Exception as e:
#     st.error(f"Error loading CSVs: {e}")
#     st.stop()

# # Helper functions
# def input_image_details(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         try:
#             bytes_data = uploaded_file.getvalue()
#             image_parts.append({
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             })
#         except Exception as e:
#             st.warning(f"Could not read image {uploaded_file.name}: {e}")
#     return image_parts

# def get_response(model, input_text, image_parts, prompt):
#     try:
#         response = model.generate_content([input_text, *image_parts, prompt])
#         return response.text
#     except Exception as e:
#         st.error(f"Gemini generation failed: {e}")
#         return None

# # Prompt setup
# input_prompt = """
# You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structure, and accuracy in your responses.
# """

# input = f"""please extract all I emphasize all data  and line items and format output strictly as JSON. Don't aggregate similar or duplicated rows. Stick to this exact format of 12 features. Do not return anything else.make credit notes amount to be negative.

# Check for rollups and individual line items. This is important: 'Folio Account Number' is sometimes called 'Customer No' or 'Customer P/O Number'. It should never be null — try and find it. VAT should also never be null — if not found, assume it's 15% of the price.

# You can look up the folio account numbers STRICTLY from: {folios['Folio'].values}
# You can look up the grades STRICTLY from: {grade_cost['GRADE'].values}
# You can look up the commodities STRICTLY from: {grade_cost['DESCRIPTION'].values}
# You can look up the cost type STRICTLY from: {grade_cost['COST FOR'].values}
# You can look up the supplier names STRICTLY from: {folios['NEXGRO COMPANY'].values}
# You can look up the client company names from: {silos['COOP'].values}
# 'Silo Name' might be called 'branch' or 'tak'. You can look it up from: {silos['SILO NAME'].values}

# Only give back the following 12 features in this format:
# [
#     {{
#         "Silo Name": "Example",
#         "Folio Account Number": 123456,
#         "Supplier": "Supplier Name",
#         "Client Company": "Client Name",
#         "Invoice number": "INV123456",
#         "Document Type": "Invoice",
#         "Invoice Date": "YYYY-MM-DD",
#         "Grade": "SB1",
#         "Commodity": "SOYA",
#         "Cost Type": "DAY STORAGE"
#         "Units": 1000,
#         "Price": 12345.67,
#         "Total Excl": 12345.67,
#         "Vat": 1851.85,
#         "Total Incl": 14197.52,
#         "Total Invoice": 14197.52,
#         "Item Description": "Line item description"
#     }}
# ]
# """

# # Streamlit UI
# st.set_page_config(page_title='Invoice Extractor', layout="wide")
# st.header("🚀 Multilanguage Invoice Extractor (Auto-Processing)")

# uploaded_files = st.file_uploader(
#     'Upload invoice images (jpg, jpeg, png)...',
#     type=['jpg', 'jpeg', 'png'],
#     accept_multiple_files=True
# )

# # Auto-processing on upload
# if uploaded_files:
#     batch_size = 1

#     st.info(f"⏳ Starting auto-processing of {len(uploaded_files)} images in batches of {batch_size}...")

#     model = genai.GenerativeModel('gemini-1.5-flash')
#     total_batches = (len(uploaded_files) + batch_size - 1) // batch_size

#     for batch_index in range(total_batches):
#         st.markdown(f"### 🔍 Processing Batch {batch_index + 1} of {total_batches}")

#         current_batch = uploaded_files[batch_index * batch_size:(batch_index + 1) * batch_size]

#         # Show images
#         for file in current_batch:
#             try:
#                 image = Image.open(file)
#                 st.image(image, caption=file.name, width=250)
#             except UnidentifiedImageError:
#                 st.warning(f"⚠️ Could not open image: {file.name}")

#         # Get results
#         image_data = input_image_details(current_batch)
#         if not image_data:
#             st.warning("🚫 No valid image data found in this batch.")
#             continue

#         response = get_response(model, input_prompt, image_data, input)

#         if response:
#             try:
#                 json_match = re.search(r'\[.*?\]', response, re.DOTALL)
#                 if json_match:
#                     json_data = json_match.group(0)
#                     parsed_json = json.loads(json_data)
#                     df = pd.DataFrame(parsed_json)
#                     st.success(f"✅ Extracted {len(df)} records from batch {batch_index + 1}")
#                     st.dataframe(df)

#                     csv_file = "data/nexgrodata.csv"
#                     df.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file))
#                 else:
#                     st.warning("⚠️ No JSON data found in Gemini response.")
#             except Exception as e:
#                 st.error(f"JSON parsing failed: {e}")

#         time.sleep(1)  # brief pause

#     # Download button after processing
#     csv_path = "data/nexgrodata.csv"
#     if os.path.exists(csv_path):
#         with open(csv_path, "rb") as f:
#             st.download_button(
#                 label="📥 Download Combined CSV",
#                 data=f,
#                 file_name="nexgrodata.csv",
#                 mime="text/csv"
#             )


import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image, UnidentifiedImageError
import fitz  # PyMuPDF
import google.generativeai as genai
import pandas as pd
import json
import re
import time
import io

# Load API key
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error("GOOGLE_API_KEY not found in environment.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Gemini configuration error: {e}")
    st.stop()

# Load support CSVs
try:
    silos = pd.read_csv("data/silos.csv")
    folios = pd.read_csv("data/folios.csv")
    grade_cost = pd.read_csv("data/cost-grades.csv")
except Exception as e:
    st.error(f"Error loading CSVs: {e}")
    st.stop()

# Prompt setup
input_prompt = """
You are a skilled professional specializing in the interpretation of invoices across various languages. Users will upload images of invoices, and you will provide accurate responses to any questions related specifically to invoices. Your task is to offer precise and insightful assistance in invoice interpretation, ensuring clarity, structure, and accuracy in your responses.
"""

input = f"""please extract all I emphasize all data  and line items and format output strictly as JSON. Don't aggregate similar or duplicated rows. Stick to this exact format of 12 features. Do not return anything else.make all document type  that are credit note amounts(vat,total inc, total excl, price, total invoice and units) to be negative I emphasize the amount must be negative for credit note.

Check for rollups and individual line items. This is important: 'Folio Account Number' is sometimes called 'Customer No' or 'Customer P/O Number'. It should never be null — try and find it. VAT should also never be null — if not found, assume it's 15% of the price.

You can look up the folio account numbers STRICTLY from: {folios['Folio'].values}
You can look up the grades STRICTLY from: {grade_cost['GRADE'].values}
You can look up the commodities STRICTLY from: {grade_cost['DESCRIPTION'].values}
You can look up the cost type STRICTLY from: {grade_cost['COST FOR'].values}
You can look up the supplier names STRICTLY from: {folios['NEXGRO COMPANY'].values}
You can look up the client company names from: {silos['COOP'].values}
'Silo Name' might be called 'branch' or 'tak'. You can look it up from: {silos['SILO NAME'].values}

Only give back the following 12 features in this format:
[
    {{
        "Silo Name": "Example",
        "Folio Account Number": 123456,
        "Supplier": "Supplier Name",
        "Client Company": "Client Name",
        "Invoice number": "INV123456",
        "Document Type": "Invoice",
        "Invoice Date": "YYYY-MM-DD",
        "Grade": "SB1",
        "Commodity": "SOYA",
        "Cost Type": "DAY STORAGE",
        "Units": 1000,
        "Price": 12345.67,
        "Total Excl": 12345.67,
        "Vat": 1851.85,
        "Total Incl": 14197.52,
        "Total Invoice": 14197.52,
        "Item Description": "Line item description"
    }}
]
"""

# Helper: Convert PDF to list of PIL images
def convert_pdf_to_images_pymupdf(pdf_file):
    images = []
    pdf_file.seek(0)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
    return images

# Helper: Convert images to parts for Gemini
def input_image_details(pil_images):
    image_parts = []
    for img in pil_images:
        with io.BytesIO() as img_bytes:
            img.convert("RGB").save(img_bytes, format="JPEG")
            image_parts.append({
                "mime_type": "image/jpeg",
                "data": img_bytes.getvalue()
            })
    return image_parts

# Helper: Get Gemini response
def get_response(model, input_text, image_parts, prompt):
    try:
        response = model.generate_content([input_text, *image_parts, prompt])
        return response.text
    except Exception as e:
        st.error(f"Gemini generation failed: {e}")
        return None

# UI Setup
st.set_page_config(page_title='Invoice Extractor', layout="wide")
st.header("📄 PDF Invoice Extractor")

uploaded_pdfs = st.file_uploader(
    'Upload invoice PDFs...',
    type=['pdf'],
    accept_multiple_files=True
)

# Auto-processing PDFs
if uploaded_pdfs:
    st.info(f"⏳ Starting auto-processing of {len(uploaded_pdfs)} PDF files...")

    model = genai.GenerativeModel('gemini-1.5-flash')

    for index, pdf_file in enumerate(uploaded_pdfs):
        st.markdown(f"### 🔍 Processing: {pdf_file.name}")
        try:
            images = convert_pdf_to_images_pymupdf(pdf_file)
        except Exception as e:
            st.error(f"Failed to convert {pdf_file.name}: {e}")
            continue

        # Show images
        for i, image in enumerate(images):
            st.image(image, caption=f"{pdf_file.name} - Page {i + 1}", width=250)

        # Convert to Gemini format
        image_data = input_image_details(images)

        # Get model response
        response = get_response(model, input_prompt, image_data, input)

        if response:
            try:
                json_match = re.search(r'\[.*?\]', response, re.DOTALL)
                if json_match:
                    json_data = json_match.group(0)
                    parsed_json = json.loads(json_data)
                    df = pd.DataFrame(parsed_json)
                    st.success(f"✅ Extracted {len(df)} rows from {pdf_file.name}")
                    st.dataframe(df)

                    csv_file = "data/nexgrodata.csv"
                    df.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file))
                else:
                    st.warning("⚠️ No JSON data found in response.")
            except Exception as e:
                st.error(f"JSON parsing failed: {e}")

        time.sleep(1)

    # Show download button
    csv_path = "data/nexgrodata.csv"
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as f:
            st.download_button(
                label="📥 Download Combined CSV",
                data=f,
                file_name="nexgrodata.csv",
                mime="text/csv"
            )
