import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Target the "Academic Services" footer at the bottom of the page
        footer_text = page.search_for("Academic Services")
        
        if not footer_text:
            st.error("Could not find the page structure. Please ensure this is a standard Brandeis Dean's Certification.")
        else:
            # 2. Pin the signature a fixed distance ABOVE the footer (approx 200 units)
            # This lands the signature in the middle of the Academic section
            anchor = footer_text[0]
            img_x = 100  # Fixed horizontal position from the left margin
            img_y = anchor.y0 - 200 # Places signature 200 units above the footer
            
            target_area = fitz.Rect(img_x, img_y, img_x + 160, img_y + 50)
            
            # Draw white box to clear any underlying text
            page.draw_rect(target_area, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_image(target_area, filename="unnamed.jpg")
            
            output_bytes = doc.write()
            doc.close()
            
            original_name = uploaded_pdf.name.rsplit('.', 1)[0]
            st.success("Signature placed using footer anchor!")
            st.download_button(
                label=f"Download {original_name}_SIGNED.pdf", 
                data=output_bytes, 
                file_name=f"{original_name}_SIGNED.pdf",
                mime="application/pdf"
            )
