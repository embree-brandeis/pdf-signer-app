import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Find all instances of "Signature:"
        text_instances = page.search_for("Signature:")
        
        if len(text_instances) < 2:
            st.error("Could not find both signature lines.")
        else:
            # academic_sig_label is the top one (near the Academic Report)
            academic_sig_label = text_instances[0]
            
            # 2. Get the reference image from the bottom for size/alignment
            conduct_sig_rect = None
            for img in page.get_image_info():
                img_rect = fitz.Rect(img["bbox"])
                if img_rect.y0 > text_instances[1].y0 - 80:
                    conduct_sig_rect = img_rect
                    break
            
            if conduct_sig_rect:
                # 3. Pin to the top "Signature:" label
                img_x = conduct_sig_rect.x0
                # Use the y0 coordinate of the label itself + a small nudge
                # Try '5' to start. If it's too high, increase to '10' or '15'.
                img_y = academic_sig_label.y0 - 5 
                
                target_area = fitz.Rect(img_x, img_y, img_x + conduct_sig_rect.width, img_y + conduct_sig_rect.height)
                page.insert_image(target_area, filename="unnamed.jpg")
                
                output_bytes = doc.write()
                doc.close()
                
                original_name = uploaded_pdf.name.rsplit('.', 1)[0]
                st.success("Signature applied!")
                st.download_button(
                    label="Download Signed PDF", 
                    data=output_bytes, 
                    file_name=f"{original_name}_SIGNED.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Could not detect the size of the bottom signature.")
