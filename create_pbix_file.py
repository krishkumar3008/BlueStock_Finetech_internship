import zipfile
import os

def create_pbix():
    pbix_filename = "bluestock_mf_dashboard.pbix"
    print(f"Creating ZIP archive as {pbix_filename} containing Power BI Project files...")
    
    with zipfile.ZipFile(pbix_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add pbip file
        zipf.write("bluestock_mf_dashboard.pbip")
        
        # Add Report folder
        for root, dirs, files in os.walk("bluestock_mf_dashboard.Report"):
            for file in files:
                filepath = os.path.join(root, file)
                zipf.write(filepath)
                
        # Add SemanticModel folder
        for root, dirs, files in os.walk("bluestock_mf_dashboard.SemanticModel"):
            for file in files:
                filepath = os.path.join(root, file)
                zipf.write(filepath)
                
    print(f"File {pbix_filename} created successfully containing all project files.")

if __name__ == '__main__':
    create_pbix()
