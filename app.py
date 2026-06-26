import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Locate the specific name to anchor to
        lori_text = page.search_for("Lori")
        
        if not lori_text:
            st.error("Could not find the signature name area.")
        else:
            # 2. Pin above the name
            target = lori_text[0]
            
            # Place signature 50 pixels to the left of the name, 
            # and 40 pixels ABOVE the name to leave room for the printed title.
            img_x = target.x0 - 50 
            img_y = target.y0 - 40 
            
            target_area = fitz.Rect(img_x, img_y, img_x + 160, img_y + 40)
            
            # This 'whiteout' trick prevents the signature from overlapping text
            page.draw_rect(target_area, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_image(target_area, filename="unnamed.jpg")
            
            output_bytes = doc.write()
            doc.close()
            
            original_name = uploaded_pdf.name.rsplit('.', 1)[0]
            st.success("Signature placed above the name!")
            st.download_button(
                label=f"Download {original_name}_SIGNED.pdf", 
                data=output_bytes, 
                file_name=f"{original_name}_SIGNED.pdf",
                mime="application/pdf"
            )
