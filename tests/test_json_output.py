from src.pdf_reader.reader import PDFReader
from src.layout.layout_analyzer import LayoutAnalyzer
from src.heading_detection.heading_detector import HeadingDetector
from src.topic_detection.topic_detector import TopicDetector
from src.table_detection.table_detector import TableDetector
from src.document_structure.structure_builder import DocumentStructureBuilder
from src.output.json_writer import JSONWriter


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

    # Save as JSON
    json_writer = JSONWriter()
    output_path = json_writer.save(
        document_structure
    )

    print("\n========== JSON OUTPUT ==========\n")
    print(f"JSON file created successfully:")
    print(output_path)


if __name__ == "__main__":

    main()
