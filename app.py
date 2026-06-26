import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Search for all instances of "Signature:"
        text_instances = page.search_for("Signature:")
        
        if len(text_instances) < 2:
            st.error("Could not find both signature lines.")
        else:
            # We target the first "Signature:" label (Academic)
            label_rect = text_instances[0]
            
            # 2. Pin the image relative to the label
            # This places the image directly to the right of the label, 
            # and aligns the top of the image with the top of the label text.
            img_x = label_rect.x1 + 10  # 10 pixels to the right of the word "Signature:"
            img_y = label_rect.y0 - 10  # Start slightly above the label line
            
            # Keep the image size constant (e.g., 120 wide by 40 tall)
            target_area = fitz.Rect(img_x, img_y, img_x + 120, img_y + 40)
            
            # 3. Apply the image
            page.insert_image(target_area, filename="unnamed.jpg")
            
            # 4. Finalize
            output_bytes = doc.write()
            doc.close()
            
            st.success("Signature pinned successfully!")
            st.download_button("Download Signed PDF", output_bytes, file_name="final_signed_doc.pdf")
