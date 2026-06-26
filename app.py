import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Specifically target the FIRST "Signature:" label
        text_instances = page.search_for("Signature:")
        
        if not text_instances:
            st.error("Could not find the signature line.")
        else:
            academic_sig_label = text_instances[0]
            
            # 2. Define a fixed size for your signature (150 width, 50 height)
            # This ensures it never changes size regardless of what is below it.
            img_width = 150
            img_height = 50
            
            # 3. Pin the image exactly below the FIRST "Signature:" label
            # Change this '60' to nudge the signature UP or DOWN.
            # (60 is roughly one line of text)
            img_x = academic_sig_label.x0
            img_y = academic_sig_label.y0 + 20 
            
            target_area = fitz.Rect(img_x, img_y, img_x + img_width, img_y + img_height)
            
            page.insert_image(target_area, filename="unnamed.jpg")
            
            output_bytes = doc.write()
            doc.close()
            
            original_name = uploaded_pdf.name.rsplit('.', 1)[0]
            st.success("Signature applied to the Academic section!")
            st.download_button(
                label="Download Signed PDF", 
                data=output_bytes, 
                file_name=f"{original_name}_SIGNED.pdf",
                mime="application/pdf"
            )
