import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Target the FIRST "Signature:" label
        text_instances = page.search_for("Signature:")
        
        if not text_instances:
            st.error("Could not find the signature line.")
        else:
            academic_sig_label = text_instances[0]
            
            # 2. Refined Placement
            # We set a fixed size, but we move the Y-coordinate down 
            # by 30 pixels to clear the "Signature:" text and 
            # align it above the printed name.
            img_width = 160
            img_height = 50
            img_x = academic_sig_label.x0 + 80
            img_y = academic_sig_label.y0 + 30 
            
            target_area = fitz.Rect(img_x, img_y, img_x + img_width, img_y + img_height)
            
            page.insert_image(target_area, filename="unnamed.jpg")
            
            output_bytes = doc.write()
            doc.close()
            
            # 3. Dynamic naming
            original_name = uploaded_pdf.name.rsplit('.', 1)[0]
            st.success("Signature placed with breathing room!")
            st.download_button(
                label=f"Download {original_name}_SIGNED.pdf", 
                data=output_bytes, 
                file_name=f"{original_name}_SIGNED.pdf",
                mime="application/pdf"
            )
