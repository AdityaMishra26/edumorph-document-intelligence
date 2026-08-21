class DocumentStructureBuilder:

    """
    Build a structured representation of a document
    using headings, topics, tables, page text,
    and unified document elements.
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

            elements = self._build_elements(
                page["text"],
                page_headings,
                page_tables
            )

            structure_pages.append({

                "page_number": page_number,

                "text": page["text"],

                "headings": page_headings,

                "topics": page_topics,

                "tables": page_tables,

                "elements": elements

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

    def _build_elements(
        self,
        page_text,
        headings,
        tables
    ):
        """
        Build a unified list of document elements.

        Currently supports:
        - heading
        - paragraph
        - question
        - table

        Image, diagram, and flowchart detection
        will be added in later modules.
        """

        elements = []

        heading_texts = set()

        for heading in headings:

            if isinstance(heading, dict):

                text = heading.get(
                    "text",
                    ""
                ).strip()

                if text:

                    heading_texts.add(text)

                    elements.append({

                        "type": "heading",

                        "content": text,

                        "metadata": {

                            "level": heading.get(
                                "level",
                                None
                            ),

                            "bounding_box": heading.get(
                                "bounding_box",
                                None
                            )

                        }

                    })

        paragraphs = self._split_paragraphs(
            page_text
        )

        for paragraph in paragraphs:

            if paragraph in heading_texts:

                continue

            if self._is_question(paragraph):

                elements.append({

                    "type": "question",

                    "content": paragraph,

                    "metadata": {}

                })

            else:

                elements.append({

                    "type": "paragraph",

                    "content": paragraph,

                    "metadata": {}

                })

        for table in tables:

            elements.append({

                "type": "table",

                "content": table.get(
                    "data",
                    []
                ),

                "metadata": {

                    "table_number": table.get(
                        "table_number",
                        None
                    ),

                    "bounding_box": table.get(
                        "bounding_box",
                        None
                    )

                }

            })

        return elements

    def _split_paragraphs(
        self,
        page_text
    ):
        """
        Split page text into meaningful paragraphs.
        """

        paragraphs = [

            paragraph.strip()

            for paragraph in page_text.split(
                "\n\n"
            )

            if paragraph.strip()

        ]

        return paragraphs

    def _is_question(
        self,
        text
    ):
        """
        Detect whether text appears to be a question.
        """

        text = text.strip()

        if not text:

            return False

        question_prefixes = (

            "Q.",
            "Q:",
            "Question",
            "QUESTION",
            "What ",
            "Why ",
            "How ",
            "When ",
            "Where ",
            "Which ",
            "Who "

        )

        if text.endswith("?"):

            return True

        return text.startswith(
            question_prefixes
        )
