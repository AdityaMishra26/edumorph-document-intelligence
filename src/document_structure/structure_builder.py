class DocumentStructureBuilder:

    """
    Build a structured representation of a document
    using headings, topics, tables, and page text.
    """

    def build_structure(
        self,
        document_info,
        heading_data,
        topic_data,
        table_data
    ):

        """
        Combine results from different modules into
        one document structure.
        """

        pages = document_info["pages"]

        structure_pages = []

        for page in pages:

            page_number = page["page_number"]

            page_headings = self._get_page_data(
                heading_data,
                page_number,
                "headings"
            )

            page_topics = self._get_page_data(
                topic_data,
                page_number,
                "keywords"
            )

            page_tables = self._get_page_data(
                table_data,
                page_number,
                "tables"
            )

            structure_pages.append({
                "page_number": page_number,
                "text": page["text"],
                "headings": page_headings,
                "topics": page_topics,
                "tables": page_tables
            })

        return {
            "file_name": document_info["file_name"],
            "page_count": document_info["page_count"],
            "pages": structure_pages
        }

    def _get_page_data(
        self,
        data_list,
        page_number,
        key
    ):

        """
        Get specific data for a page.
        """

        for item in data_list:

            if item["page_number"] == page_number:

                return item.get(key, [])

        return []
