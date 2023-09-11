import React, {useState} from 'react';
import Button from "@material-ui/core/Button";
import {Document, Page} from "react-pdf";

const hidden_input = {
    display: 'none',
};

function PDFViewer() {
    const [pdfFile, setPdfFile] = useState(null);

    const uploadEvent = (event) => {
        const file = event.target.files[0];
        if (file && file.type === "application/pdf") {
            setPdfFile(file);
        } else {
            setPdfFile(null);
        }
    };

    return (
        <div>
            <div>
                <input
                    style={hidden_input}
                    accept="application/pdf"
                    id="contained-button-file"
                    multiple
                    type="file"
                    onChange={uploadEvent}
                />
                <label htmlFor="contained-button-file">
                    <Button variant="contained" color="primary" component="span">
                        Upload
                    </Button>
                </label>
            </div>
            {pdfFile && (
                <div>
                    <Document file={pdfFile}>
                        <Page pageNumber={1}/>
                    </Document>
                </div>
            )}
        </div>
    );
}

export default PDFViewer;
