import streamlit as st
import fitz  # PyMuPDF

st.title("Smart PDF Signer")
st.write("Upload a Dean's Certification. The app will verify the Conduct signature exists before signing.")

# File Uploader
uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_pdf is not None:
    if st.button("Apply Signature"):
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0] # Assumes everything is on the first page
        
        # 1. Find all instances of "Signature:"
        text_instances = page.search_for("Signature:")
        
        # Ensure there are at least two signature lines found
        if len(text_instances) < 2:
            st.error("Error: Could not find both signature lines on this document.")
        else:
            top_sig_rect = text_instances[0]
            bottom_sig_rect = text_instances[1]
            
            # 2. Define a "Search Box" around the bottom signature line
            # This creates an invisible box right above the 2nd "Signature:" text
            check_area = fitz.Rect(
                bottom_sig_rect.x0, 
                bottom_sig_rect.y0 - 60, # 60 pixels above the word
                bottom_sig_rect.x0 + 250, # 250 pixels to the right
                bottom_sig_rect.y0 + 20
            )
            
            bottom_sig_present = False
            
            # 3. Check if any images intersect with our Search Box
            for img in page.get_image_info():
                if fitz.Rect(img["bbox"]).intersects(check_area):
                    bottom_sig_present = True
                    break
                    
            # 4. Check if any digital ink/drawings intersect with our Search Box
            if not bottom_sig_present:
                for drawing in page.get_drawings():
                    if drawing["rect"].intersects(check_area):
                        bottom_sig_present = True
                        break
            
            # 5. Logic branching: Return error or apply top signature
            if not bottom_sig_present:
                st.error("Bottom signature missing. Please ensure the Conduct Report is signed first before stamping.")
            else:
                # Apply the top signature
                img_x_start = top_sig_rect.x0
                img_y_start = top_sig_rect.y0 - 50 
                img_x_end = img_x_start + 180   
                img_y_end = img_y_start + 60    
                
                target_area = fitz.Rect(img_x_start, img_y_start, img_x_end, img_y_end)
                page.insert_image(target_area, filename="unnamed.jpg")
                
                # Save and prepare for download
                output_bytes = doc.write()
                doc.close()
                
                # Dynamic Naming
                original_name = uploaded_pdf.name
                if original_name.lower().endswith(".pdf"):
                    base_name = original_name[:-4] 
                else:
                    base_name = original_name
                    
                output_filename = f"{base_name}_STEP03.pdf"
                
                st.success("Conduct signature verified! Top signature applied successfully.")
                st.download_button(
                    label=f"Download {output_filename}",
                    data=output_bytes,
                    file_name=output_filename,
                    mime="application/pdf"
                )
