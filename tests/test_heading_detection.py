from src.layout.layout_analyzer import LayoutAnalyzer
from src.heading_detection.heading_detector import HeadingDetector


def main():
    pdf_path = "sample_data/input/sample.pdf"

    # Step 1: Analyze PDF layout
    layout_analyzer = LayoutAnalyzer()
    layout_results = layout_analyzer.analyze_pdf(pdf_path)

    # Step 2: Detect headings
    heading_detector = HeadingDetector()
    heading_results = heading_detector.detect_headings(
        layout_results
    )

    print("\n========== HEADING DETECTION ==========\n")

    for page in heading_results:

        print(f"PAGE: {page['page_number']}")
        print(
            f"Number of Headings: "
            f"{len(page['headings'])}\n"
        )

        for index, heading in enumerate(
            page["headings"],
            start=1
        ):
            print(f"HEADING {index}")
            print(f"Text: {heading['text']}")
            print(
                f"Bounding Box: "
                f"{heading['bounding_box']}"
            )
            print(f"Height: {heading['height']}")
            print("-" * 40)

        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
