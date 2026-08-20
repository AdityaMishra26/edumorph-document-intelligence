from src.layout.layout_analyzer import LayoutAnalyzer


def main():
    pdf_path = "sample_data/input/sample.pdf"

    analyzer = LayoutAnalyzer()

    results = analyzer.analyze_pdf(pdf_path)

    print("\n========== LAYOUT ANALYSIS ==========\n")

    for page in results:
        print(f"PAGE: {page['page_number']}")
        print(f"Page Size: {page['page_width']} x {page['page_height']}")
        print(f"Number of Text Blocks: {len(page['blocks'])}\n")

        for index, block in enumerate(page["blocks"], start=1):
            print(f"BLOCK {index}")

            print("Text:")
            print(block["text"])

            print("\nBounding Box:")
            print(block["bounding_box"])

            print(f"Width: {block['width']}")
            print(f"Height: {block['height']}")

            print("-" * 40)

        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
