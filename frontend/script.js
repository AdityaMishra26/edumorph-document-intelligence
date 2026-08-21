const API_URL =
    "http://127.0.0.1:8000/analyze";


const pdfFileInput =
    document.getElementById(
        "pdfFile"
    );

const uploadArea =
    document.getElementById(
        "uploadArea"
    );

const analyzeButton =
    document.getElementById(
        "analyzeButton"
    );

const removeFileButton =
    document.getElementById(
        "removeFileButton"
    );

const selectedFile =
    document.getElementById(
        "selectedFile"
    );

const selectedFileName =
    document.getElementById(
        "selectedFileName"
    );

const selectedFileSize =
    document.getElementById(
        "selectedFileSize"
    );

const buttonText =
    document.getElementById(
        "buttonText"
    );

const statusElement =
    document.getElementById(
        "status"
    );

const resultsElement =
    document.getElementById(
        "results"
    );

const fileNameElement =
    document.getElementById(
        "fileName"
    );

const pageCountElement =
    document.getElementById(
        "pageCount"
    );

const elementCountElement =
    document.getElementById(
        "elementCount"
    );

const pagesContainer =
    document.getElementById(
        "pagesContainer"
    );


uploadArea.addEventListener(
    "click",
    function () {

        pdfFileInput.click();

    }
);


pdfFileInput.addEventListener(
    "change",
    function () {

        if (
            pdfFileInput.files.length > 0
        ) {

            selectFile(
                pdfFileInput.files[0]
            );

        }

    }
);


uploadArea.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        uploadArea.classList.add(
            "dragging"
        );

    }
);


uploadArea.addEventListener(
    "dragleave",
    function () {

        uploadArea.classList.remove(
            "dragging"
        );

    }
);


uploadArea.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        uploadArea.classList.remove(
            "dragging"
        );

        const file =
            event.dataTransfer.files[0];

        if (file) {

            selectFile(
                file
            );

        }

    }
);


removeFileButton.addEventListener(
    "click",
    function () {

        clearSelectedFile();

    }
);


analyzeButton.addEventListener(
    "click",
    analyzeDocument
);


function selectFile(file) {

    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        showStatus(
            "Please select a valid PDF file.",
            "error"
        );

        return;

    }


    const dataTransfer =
        new DataTransfer();

    dataTransfer.items.add(
        file
    );

    pdfFileInput.files =
        dataTransfer.files;


    selectedFileName.textContent =
        file.name;

    selectedFileSize.textContent =
        formatFileSize(
            file.size
        );


    selectedFile.classList.remove(
        "hidden"
    );


    uploadArea.classList.add(
        "hidden"
    );


    analyzeButton.disabled = false;


    showStatus(
        "PDF ready for analysis.",
        "success"
    );

}


function clearSelectedFile() {

    pdfFileInput.value = "";

    selectedFile.classList.add(
        "hidden"
    );

    uploadArea.classList.remove(
        "hidden"
    );

    analyzeButton.disabled = true;

    statusElement.textContent = "";

    statusElement.className =
        "status-message";

}


function formatFileSize(bytes) {

    if (bytes < 1024) {

        return bytes + " bytes";

    }


    const kilobytes =
        bytes / 1024;


    if (kilobytes < 1024) {

        return (
            kilobytes.toFixed(1) +
            " KB"
        );

    }


    const megabytes =
        kilobytes / 1024;


    return (
        megabytes.toFixed(2) +
        " MB"
    );

}


async function analyzeDocument() {

    const file =
        pdfFileInput.files[0];


    if (!file) {

        showStatus(
            "Please select a PDF first.",
            "error"
        );

        return;

    }


    analyzeButton.disabled = true;

    buttonText.textContent =
        "Analyzing...";


    showStatus(
        "EduMorph is analyzing your document...",
        "loading"
    );


    resultsElement.classList.add(
        "hidden"
    );


    try {

        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Document analysis failed."
            );

        }


        if (!data.success) {

            throw new Error(
                "Document analysis was unsuccessful."
            );

        }


        displayResults(
            data.analysis,
            file.name
        );


        showStatus(
            "Analysis completed successfully!",
            "success"
        );


        resultsElement.scrollIntoView(
            {
                behavior: "smooth",
                block: "start"
            }
        );

    } catch (error) {

        console.error(
            error
        );


        showStatus(
            error.message ||
            "Something went wrong.",
            "error"
        );

    } finally {

        analyzeButton.disabled = false;

        buttonText.textContent =
            "Analyze Document";

    }

}


function displayResults(
    analysis,
    originalFileName
) {

    fileNameElement.textContent =
        originalFileName;

    pageCountElement.textContent =
        analysis.page_count;


    pagesContainer.innerHTML = "";


    let totalElements = 0;


    analysis.pages.forEach(
        function (page) {

            const elements =
                page.elements || [];


            totalElements +=
                elements.length;


            const pageCard =
                document.createElement(
                    "div"
                );

            pageCard.className =
                "page-card";


            const pageTitle =
                document.createElement(
                    "h3"
                );

            pageTitle.className =
                "page-title";


            pageTitle.innerHTML =
                `
                <span class="page-number">
                    ${page.page_number}
                </span>
                Page ${page.page_number}
                `;


            pageCard.appendChild(
                pageTitle
            );


            if (
                elements.length === 0
            ) {

                const emptyMessage =
                    document.createElement(
                        "p"
                    );

                emptyMessage.textContent =
                    "No structured elements detected.";

                pageCard.appendChild(
                    emptyMessage
                );

            }


            elements.forEach(
                function (element) {

                    const elementCard =
                        createElementCard(
                            element
                        );

                    pageCard.appendChild(
                        elementCard
                    );

                }
            );


            const topicsCard =
                createTopicsCard(
                    page.topics || []
                );


            pageCard.appendChild(
                topicsCard
            );


            pagesContainer.appendChild(
                pageCard
            );

        }
    );


    elementCountElement.textContent =
        totalElements;


    resultsElement.classList.remove(
        "hidden"
    );

}


function createElementCard(
    element
) {

    const card =
        document.createElement(
            "div"
        );

    card.className =
        "element-card " +
        element.type;


    const type =
        document.createElement(
            "div"
        );

    type.className =
        "element-type";

    type.textContent =
        element.type;


    card.appendChild(
        type
    );


    if (element.text) {

        const text =
            document.createElement(
                "p"
            );

        text.className =
            "element-text";

        text.textContent =
            element.text;

        card.appendChild(
            text
        );

    }


    if (
        element.type === "table"
    ) {

        const info =
            document.createElement(
                "p"
            );

        info.className =
            "element-text";

        info.textContent =
            "Table " +
            (
                element.table_number ||
                ""
            );

        card.appendChild(
            info
        );

    }


    if (
        element.type === "image"
    ) {

        const info =
            document.createElement(
                "p"
            );

        info.className =
            "element-text";

        info.textContent =
            "Detected image " +
            (
                element.image_number ||
                ""
            );

        card.appendChild(
            info
        );

    }


    if (
        element.type === "drawing"
    ) {

        const info =
            document.createElement(
                "p"
            );

        info.className =
            "element-text";

        info.textContent =
            "Detected vector drawing";

        card.appendChild(
            info
        );

    }


    return card;

}


function createTopicsCard(
    topics
) {

    const card =
        document.createElement(
            "div"
        );

    card.className =
        "topics-card";


    const title =
        document.createElement(
            "h4"
        );

    title.textContent =
        "Detected Topics";


    card.appendChild(
        title
    );


    if (topics.length === 0) {

        const empty =
            document.createElement(
                "p"
            );

        empty.textContent =
            "No topics detected.";

        card.appendChild(
            empty
        );

        return card;

    }


    const topicsList =
        document.createElement(
            "div"
        );

    topicsList.className =
        "topics-list";


    topics.forEach(
        function (topic) {

            const topicItem =
                document.createElement(
                    "span"
                );

            topicItem.className =
                "topic-tag";


            const topicText =
                Array.isArray(topic)
                    ? topic[0]
                    : topic.text;


            const topicCount =
                Array.isArray(topic)
                    ? topic[1]
                    : topic.count;


            topicItem.textContent =
                topicText +
                (
                    topicCount
                        ? " · " +
                          topicCount
                        : ""
                );


            topicsList.appendChild(
                topicItem
            );

        }
    );


    card.appendChild(
        topicsList
    );


    return card;

}


function showStatus(
    message,
    type
) {

    statusElement.textContent =
        message;

    statusElement.className =
        "status-message " +
        type;

}
