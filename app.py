import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Find the "Academic Report:" header
        academic_report_text = page.search_for("Academic Report:")
        
        # 2. Find the reference Conduct signature for size/width
        text_instances = page.search_for("Signature:")
        conduct_sig_rect = None
        
        if len(text_instances) >= 2:
            for img in page.get_image_info():
                img_rect = fitz.Rect(img["bbox"])
                if img_rect.y0 > text_instances[1].y0 - 80:
                    conduct_sig_rect = img_rect
                    break

        if not academic_report_text or not conduct_sig_rect:
            st.error("Could not find required sections for alignment.")
        else:
            # 3. Pin to the bottom of the Academic Report table
            anchor = academic_report_text[0]
            
            img_x = conduct_sig_rect.x0
            img_y = anchor.y0 + 350 # Adjust this number to nudge placement
            
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
