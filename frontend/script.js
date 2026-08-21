const uploadArea = document.getElementById("uploadArea");
const pdfFile = document.getElementById("pdfFile");
const selectedFile = document.getElementById("selectedFile");
const selectedFileName = document.getElementById("selectedFileName");
const selectedFileSize = document.getElementById("selectedFileSize");
const removeFileButton = document.getElementById("removeFileButton");
const analyzeButton = document.getElementById("analyzeButton");
const buttonText = document.getElementById("buttonText");
const status = document.getElementById("status");

let selectedPDF = null;


// ----------------------------------------
// OPEN FILE SELECTOR
// ----------------------------------------

uploadArea.addEventListener(
    "click",
    () => {
        pdfFile.click();
    }
);


// ----------------------------------------
// FILE SELECTED
// ----------------------------------------

pdfFile.addEventListener(
    "change",
    (event) => {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        selectFile(file);
    }
);


// ----------------------------------------
// DRAG AND DROP
// ----------------------------------------

uploadArea.addEventListener(
    "dragover",
    (event) => {
        event.preventDefault();

        uploadArea.classList.add("drag-active");
    }
);


uploadArea.addEventListener(
    "dragleave",
    () => {
        uploadArea.classList.remove("drag-active");
    }
);


uploadArea.addEventListener(
    "drop",
    (event) => {
        event.preventDefault();

        uploadArea.classList.remove("drag-active");

        const file = event.dataTransfer.files[0];

        if (!file) {
            return;
        }

        selectFile(file);
    }
);


// ----------------------------------------
// SELECT PDF
// ----------------------------------------

function selectFile(file) {

    if (
        file.type !== "application/pdf" &&
        !file.name.toLowerCase().endsWith(".pdf")
    ) {

        showStatus(
            "Please select a valid PDF file.",
            "error"
        );

        return;
    }

    selectedPDF = file;

    selectedFileName.textContent = file.name;

    selectedFileSize.textContent = formatFileSize(
        file.size
    );

    uploadArea.classList.add("hidden");

    selectedFile.classList.remove("hidden");

    analyzeButton.disabled = false;

    clearStatus();
}


// ----------------------------------------
// REMOVE FILE
// ----------------------------------------

removeFileButton.addEventListener(
    "click",
    () => {

        selectedPDF = null;

        pdfFile.value = "";

        selectedFile.classList.add("hidden");

        uploadArea.classList.remove("hidden");

        analyzeButton.disabled = true;

        clearStatus();
    }
);


// ----------------------------------------
// ANALYZE DOCUMENT
// ----------------------------------------

analyzeButton.addEventListener(
    "click",
    async () => {

        if (!selectedPDF) {

            showStatus(
                "Please select a PDF first.",
                "error"
            );

            return;
        }

        const formData = new FormData();

        formData.append(
            "file",
            selectedPDF
        );

        analyzeButton.disabled = true;

        buttonText.textContent =
            "Analyzing Document...";

        showStatus(
            "Uploading and analyzing your PDF...",
            "loading"
        );

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );


            if (!response.ok) {

                let errorMessage =
                    "Document analysis was unsuccessful.";

                try {

                    const errorData =
                        await response.json();

                    if (errorData.detail) {

                        errorMessage =
                            errorData.detail;
                    }

                } catch (error) {

                    console.error(error);
                }

                throw new Error(
                    errorMessage
                );
            }


            // --------------------------------
            // GET JSON RESPONSE
            // --------------------------------

            const analysisData =
                await response.json();


            // --------------------------------
            // CREATE JSON FILE
            // --------------------------------

            const jsonContent =
                JSON.stringify(
                    analysisData,
                    null,
                    2
                );


            const blob = new Blob(
                [jsonContent],
                {
                    type:
                        "application/json"
                }
            );


            const downloadURL =
                URL.createObjectURL(
                    blob
                );


            const downloadLink =
                document.createElement("a");


            downloadLink.href =
                downloadURL;


            downloadLink.download =
                selectedPDF.name
                    .replace(
                        /\.pdf$/i,
                        ""
                    ) +
                "_analysis.json";


            document.body.appendChild(
                downloadLink
            );


            downloadLink.click();


            document.body.removeChild(
                downloadLink
            );


            URL.revokeObjectURL(
                downloadURL
            );


            showStatus(
                "Analysis complete. Your JSON file has been downloaded.",
                "success"
            );


            buttonText.textContent =
                "Analysis Complete";


            setTimeout(
                () => {

                    buttonText.textContent =
                        "Analyze Document";

                    analyzeButton.disabled =
                        false;

                },
                1500
            );

        } catch (error) {

            console.error(
                "Analysis error:",
                error
            );


            showStatus(
                error.message ||
                "Document analysis was unsuccessful.",
                "error"
            );


            buttonText.textContent =
                "Analyze Document";

            analyzeButton.disabled =
                false;
        }
    }
);


// ----------------------------------------
// FILE SIZE FORMATTER
// ----------------------------------------

function formatFileSize(bytes) {

    if (bytes === 0) {
        return "0 Bytes";
    }

    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];

    const index = Math.floor(
        Math.log(bytes) /
        Math.log(1024)
    );

    return (
        parseFloat(
            (
                bytes /
                Math.pow(
                    1024,
                    index
                )
            ).toFixed(2)
        ) +
        " " +
        units[index]
    );
}


// ----------------------------------------
// STATUS MESSAGE
// ----------------------------------------

function showStatus(
    message,
    type
) {

    status.textContent =
        message;

    status.className =
        "status-message " + type;
}


function clearStatus() {

    status.textContent = "";

    status.className =
        "status-message";
}
