import streamlit as st
import fitz  # PyMuPDF

st.title("Dean's Certification Signature Tool")

uploaded_pdf = st.file_uploader("Upload your Dean's Certification PDF", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        # Read the file
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] 
        
        # 1. Search for all instances of "Signature:"
        text_instances = page.search_for("Signature:")
        
        if len(text_instances) < 2:
            st.error("Could not find both signature lines.")
        else:
            academic_sig_label = text_instances[0]
            conduct_sig_label = text_instances[1]
            
            # 2. Find the reference size from the Conduct signature image
            conduct_sig_rect = None
            for img in page.get_image_info():
                img_rect = fitz.Rect(img["bbox"])
                # Locate the signature image near the bottom label
                if img_rect.y0 > conduct_sig_label.y0 - 80:
                    conduct_sig_rect = img_rect
                    break
            
            if conduct_sig_rect:
                # 3. Position the academic signature
                # Align left with the Conduct signature
                img_x = conduct_sig_rect.x0
                # Nudge down from the "Signature:" label to sit in white space
                img_y = academic_sig_label.y0 + 15 
                
                # Create the target area with the exact dimensions of the reference
                target_area = fitz.Rect(img_x, img_y, img_x + conduct_sig_rect.width, img_y + conduct_sig_rect.height)
                
                # Apply the signature image
                page.insert_image(target_area, filename="unnamed.jpg")
                
                # Save
                output_bytes = doc.write()
                doc.close()
                
                # 4. Generate dynamic filename: [OriginalName]_SIGNED.pdf
                original_name = uploaded_pdf.name
                base_name = original_name.rsplit('.', 1)[0]  # Remove file extension
                output_filename = f"{base_name}_SIGNED.pdf"
                
                st.success("Signature applied and aligned perfectly!")
                st.download_button(
                    label=f"Download {output_filename}",
                    data=output_bytes,
                    file_name=output_filename,
                    mime="application/pdf"
                )
            else:
                st.error("Could not detect the dimensions of the bottom signature for alignment.")
