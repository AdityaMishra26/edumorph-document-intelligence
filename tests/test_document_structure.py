from src.pdf_reader.reader import PDFReader
from src.layout.layout_analyzer import LayoutAnalyzer
from src.heading_detection.heading_detector import HeadingDetector
from src.topic_detection.topic_detector import TopicDetector
from src.table_detection.table_detector import TableDetector
from src.document_structure.structure_builder import DocumentStructureBuilder


def main():

    pdf_path = "sample_data/input/sample.pdf"

    # Read PDF
    pdf_reader = PDFReader(pdf_path)

    document_info = pdf_reader.get_document_info()

    # Analyze layout
    layout_analyzer = LayoutAnalyzer()

    layout_data = layout_analyzer.analyze_pdf(pdf_path)

    # Detect headings
    heading_detector = HeadingDetector()

    heading_data = heading_detector.detect_headings(
        layout_data
    )

    # Detect topics
    topic_detector = TopicDetector()

    topic_data = topic_detector.detect_topics(
        document_info["pages"]
    )

    # Detect tables
    table_detector = TableDetector()

    table_data = table_detector.detect_tables(
        pdf_path
    )

    # Build document structure
    structure_builder = DocumentStructureBuilder()

    document_structure = structure_builder.build_structure(
        document_info,
        heading_data,
        topic_data,
        table_data
    )

    # Print results
    print("\n========== DOCUMENT STRUCTURE ==========\n")

    print(
        f"File Name: "
        f"{document_structure['file_name']}"
    )

    print(
        f"Page Count: "
        f"{document_structure['page_count']}"
    )

    for page in document_structure["pages"]:

        print(f"\nPAGE: {page['page_number']}")

        print("\nHEADINGS:")

        for heading in page["headings"]:
            print(f"- {heading['text']}")

        print("\nTOPICS:")

        for topic, count in page["topics"]:
            print(f"- {topic}: {count}")

        print("\nTABLES:")

        print(f"Tables Found: {len(page['tables'])}")

        print("\n" + "=" * 50)


if __name__ == "__main__":

    main()
