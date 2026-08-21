from src.pdf_reader.reader import PDFReader
from src.layout.layout_analyzer import LayoutAnalyzer
from src.heading_detection.heading_detector import HeadingDetector
from src.topic_detection.topic_detector import TopicDetector
from src.table_detection.table_detector import TableDetector
from src.document_structure.structure_builder import DocumentStructureBuilder
from src.output.json_writer import JSONWriter


class DocumentAnalyzer:

    """
    Main pipeline for analyzing a PDF document.

    Runs PDF reading, layout analysis, heading detection,
    topic detection, table detection, document structure
    building, and JSON output generation.
    """

    def analyze(self, pdf_path, output_path=None):

        """
        Run the complete document analysis pipeline.
        """

        # Step 1: Read the PDF
        pdf_reader = PDFReader(pdf_path)

        document_info = pdf_reader.get_document_info()

        # Step 2: Analyze the layout
        layout_analyzer = LayoutAnalyzer()

        layout_data = layout_analyzer.analyze_pdf(pdf_path)

        # Step 3: Detect headings
        heading_detector = HeadingDetector()

        heading_data = heading_detector.detect_headings(
            layout_data
        )

        # Step 4: Detect topics
        topic_detector = TopicDetector()

        topic_data = topic_detector.detect_topics(
            document_info["pages"]
        )

        # Step 5: Detect tables
        table_detector = TableDetector()

        table_data = table_detector.detect_tables(
            pdf_path
        )

        # Step 6: Build the final document structure
        structure_builder = DocumentStructureBuilder()

        document_structure = structure_builder.build_structure(
            document_info,
            heading_data,
            topic_data,
            table_data
        )

        # Step 7: Optionally save as JSON
        if output_path:

            json_writer = JSONWriter()

            json_writer.save(
                document_structure,
                output_path
            )

        return document_structure
