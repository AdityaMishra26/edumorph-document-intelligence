from src.pdf_reader.reader import PDFReader


pdf_path = "sample_data/input/sample.pdf"

reader = PDFReader(pdf_path)

document_info = reader.get_document_info()

print("File Name:", document_info["file_name"])
print("Page Count:", document_info["page_count"])
print()

for page in document_info["pages"]:
    print(f"--- PAGE {page['page_number']} ---")
    print("Width:", page["width"])
    print("Height:", page["height"])
    print("Text Preview:")
    print(page["text"][:500])
    print()
