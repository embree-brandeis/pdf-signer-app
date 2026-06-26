import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signatures"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # Search for all instances of "Signature:"
        text_instances = page.search_for("Signature:")
        
        if len(text_instances) < 2:
            st.error("Could not find both signature lines.")
        else:
            # text_instances[0] is the Academic Signature line (top of page)
            # text_instances[1] is the Conduct Signature line (bottom of page)
            academic_sig_label = text_instances[0]
            
            # Position the signature image slightly to the right of the label, 
            # and slightly shifted up so it sits on the line
            img_x_start = academic_sig_label.x0 + 80
            img_y_start = academic_sig_label.y0 - 45 
            
            target_area = fitz.Rect(img_x_start, img_y_start, img_x_start + 150, img_y_start + 50)
            
            # Apply the signature image
            page.insert_image(target_area, filename="unnamed.jpg")
            
            # Save
            output_bytes = doc.write()
            doc.close()
            
            st.success("Academic signature applied to correct location!")
            st.download_button("Download Signed PDF", output_bytes, file_name="final_signed_doc.pdf")
