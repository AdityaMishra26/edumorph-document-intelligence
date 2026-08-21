from src.pipeline.document_analyzer import DocumentAnalyzer


def main():

    pdf_path = "sample_data/input/sample.pdf"

    output_path = (
        "sample_data/output/"
        "full_document_analysis.json"
    )

    analyzer = DocumentAnalyzer()

    result = analyzer.analyze(
        pdf_path,
        output_path
    )

    print("\n========== FULL DOCUMENT ANALYSIS ==========\n")

    print(f"File Name: {result['file_name']}")

    print(f"Page Count: {result['page_count']}")

    for page in result["pages"]:

        print(f"\nPAGE: {page['page_number']}")

        print(
            f"Headings Found: "
            f"{len(page['headings'])}"
        )

        print(
            f"Topics Found: "
            f"{len(page['topics'])}"
        )

        print(
            f"Tables Found: "
            f"{len(page['tables'])}"
        )

        print("-" * 40)

    print("\nJSON file created successfully:")

    print(output_path)


if __name__ == "__main__":

    main()
