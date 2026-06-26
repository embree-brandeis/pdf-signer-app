import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        text_instances = page.search_for("Signature:")
        
        if len(text_instances) < 2:
            st.error("Could not find both signature lines.")
        else:
            # academic_sig is the target, conduct_sig is the reference for alignment/size
            academic_sig_label = text_instances[0]
            conduct_sig_label = text_instances[1]
            
            # 1. Identify the area where the Conduct signature is (as a reference)
            # We look for where the signature *actually* is (by checking for images)
            conduct_sig_rect = None
            for img in page.get_image_info():
                img_rect = fitz.Rect(img["bbox"])
                # If the image is near the bottom signature line, it's our target
                if img_rect.y0 > conduct_sig_label.y0 - 80:
                    conduct_sig_rect = img_rect
                    break
            
            if conduct_sig_rect:
                # 2. Use the Conduct signature's size and vertical alignment
                # Align X-start with the bottom signature, Y-start with the top label
                img_x = conduct_sig_rect.x0
                img_y = academic_sig_label.y0 - 30 
                
                target_area = fitz.Rect(img_x, img_y, img_x + conduct_sig_rect.width, img_y + conduct_sig_rect.height)
                
                page.insert_image(target_area, filename="unnamed.jpg")
                
                output_bytes = doc.write()
                doc.close()
                st.success("Signature aligned and scaled to match Conduct signature!")
                st.download_button("Download Signed PDF", output_bytes, file_name="final_signed_doc.pdf")
            else:
                st.error("Could not detect the dimensions of the bottom signature to use as a reference.")
