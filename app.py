import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Find the "Academic Report:" header as our stable anchor
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
            # We look for where the Academic table ends (usually quite high up)
            # and place the signature a set distance below it.
            anchor = academic_report_text[0]
            
            img_x = conduct_sig_rect.x0
            # Nudge this 'y' value to get the exact vertical height you need
            # Lower the number to move it UP, raise to move it DOWN
            img_y = anchor.y0 + 350 
            
            target_area = fitz.Rect(img_x, img_y, img_x + conduct_sig_rect.width, img_y + conduct_sig_rect.height)
            
            page.insert_image(target_area, filename="unnamed.jpg")
            
            output_bytes = doc.write()
            doc.close()
            
            original_name = uploaded_pdf.name.rsplit('.', 1)[0]
            st.download_button("Download Signed PDF", output_bytes, file_name=f"{original_name}_SIGNED.pdf")
            else:
                st.error("Could not detect the dimensions of the bottom signature for alignment.")
