import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Get all "Signature:" labels
        all_labels = page.search_for("Signature:")
        
        # 2. Filter for the one in the top half of the page (Academic section)
        # Page height is usually around 792 points. We look for labels where y < 400.
        academic_label = None
        for label in all_labels:
            if label.y0 < 400:
                academic_label = label
                break
        
        if not academic_label:
            st.error("Could not find the Academic signature line.")
        else:
            # 3. Define signature size and placement
            # y0 + 10 places it just below the "Signature:" text
            img_width = 150
            img_height = 50
            img_x = academic_label.x0
            img_y = academic_label.y0 + 10 
            
            target_area = fitz.Rect(img_x, img_y, img_x + img_width, img_y + img_height)
            
            page.insert_image(target_area, filename="unnamed.jpg")
            
            output_bytes = doc.write()
            doc.close()
            
            original_name = uploaded_pdf.name.rsplit('.', 1)[0]
            st.success("Signature correctly placed in the Academic section!")
            st.download_button(
                label="Download Signed PDF", 
                data=output_bytes, 
                file_name=f"{original_name}_SIGNED.pdf",
                mime="application/pdf"
            )
