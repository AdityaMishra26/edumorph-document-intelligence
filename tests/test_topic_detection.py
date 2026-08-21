from src.pdf_reader.reader import PDFReader
from src.topic_detection.topic_detector import TopicDetector


def main():

    pdf_path = "sample_data/input/sample.pdf"

    # Read PDF text
    pdf_reader = PDFReader(pdf_path)

    document_info = pdf_reader.get_document_info()

    pages_data = document_info["pages"]

    # Detect topics
    topic_detector = TopicDetector()

    results = topic_detector.detect_topics(
        pages_data,
        top_n=10
    )

    print("\n========== TOPIC DETECTION ==========\n")

    for page in results:

        print(f"PAGE: {page['page_number']}\n")

        print("TOP KEYWORDS:\n")

        for keyword, count in page["keywords"]:
            print(f"{keyword}: {count}")

        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
