from src.table_detection.table_detector import TableDetector


def main():

    pdf_path = "sample_data/input/sample.pdf"

    table_detector = TableDetector()

    results = table_detector.detect_tables(pdf_path)

    print("\n========== TABLE DETECTION ==========\n")

    total_tables = 0

    for page in results:

        print(f"PAGE: {page['page_number']}")

        print(f"Tables Found: {page['table_count']}\n")

        total_tables += page["table_count"]

        for table in page["tables"]:

            print(f"TABLE {table['table_number']}")

            print(
                "Bounding Box:",
                table["bounding_box"]
            )

            print("\nTable Data:")

            for row in table["data"]:
                print(row)

            print("\n" + "-" * 40 + "\n")

        print("=" * 50 + "\n")

    print(f"TOTAL TABLES FOUND: {total_tables}")


if __name__ == "__main__":
    main()
