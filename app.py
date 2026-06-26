import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

# File Uploader
uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signatures"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Find the "Signature:" lines
        text_instances = page.search_for("Signature:")
        
        if len(text_instances) < 2:
            st.error("Could not find both signature lines.")
        else:
            # bottom_sig_rect is the Conduct signature
            bottom_sig_rect = text_instances[1]
            # top_sig_rect is the Academic signature
            top_sig_rect = text_instances[0]
            
            # 2. Define target for the top signature
            # We align the top signature Y-coordinate to match the bottom one
            # Adjust the '180' and '50' values if you need to nudge the placement
            img_x_start = top_sig_rect.x0 + 100 
            img_y_start = bottom_sig_rect.y0 - 20 # Perfectly aligned with bottom signature's Y
            
            target_area = fitz.Rect(img_x_start, img_y_start, img_x_start + 150, img_y_start + 50)
            
            # 3. Apply the image
            page.insert_image(target_area, filename="unnamed.jpg")
            
            # 4. Save
            output_bytes = doc.write()
            doc.close()
            
            st.success("Signature aligned successfully!")
            st.download_button("Download Signed PDF", output_bytes, file_name="signed_doc.pdf")
