

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.pipeline_options import PdfPipelineOptions
# import warnings
# warnings.filterwarnings("ignore")

from pathlib import Path
from docling.document_converter import DocumentConverter

# 1. Initialize converter
converter = DocumentConverter() 

# 2. Use Path for all file operations (cleaner than os.makedirs)
file_path = Path("result_pdf/Dixon_Q1_result.pdf")
output_dir = Path("dockling")




# pipeline_options = PdfPipelineOptions()
# pipeline_options.page_range = (1, 1) # <-- Only process page 1 to test

converter = DocumentConverter(
    # format_options={
    #     InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    # }
)

# 3. Check if the source PDF actually exists before running
if not file_path.exists():
    raise FileNotFoundError(f"Error: The source file '{file_path}' was not found.")

print(f"Loading file: {file_path.name}")

try:
    # 4. Safely create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 5. Convert the document
    print("Converting document... (this may take a moment)")
    converted_file = converter.convert(file_path,page_range=(1, 1))
    
    # 6. Export to markdown
    file_content = converted_file.document.export_to_markdown()
    
    # 7. Write the file using Path syntax
    output_file = output_dir / f"{file_path.stem}.md"
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(file_content)
        
    print(f"Success! Saved markdown to: {output_file}")

except Exception as e:
    print(f"An error occurred during conversion: {e}")
