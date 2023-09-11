import React from 'react';
import {Input, Button, IconButton} from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import AttachFileIcon from '@material-ui/icons/AttachFile';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: 'none',
  },
}));


function PDFUploader() {
    const classes = useStyles()
    const handleUpload = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("pdfInput");
    const file = fileInput.files[0];
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8988/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        console.log(data);

    } catch (error) {
        console.error("Upload error", error);
    }
};


    return (
        <div>
    <h2>Upload your PDF</h2>
    <div>
        {/*<Input type="text" style={{ marginRight: '10px',width:'500px' }}></Input>*/}

        <form onSubmit={handleUpload}>
            <label htmlFor="pdfInput">
                <IconButton color="secondary" aria-label="upload picture" component="span">
                    <AttachFileIcon />
                </IconButton>
            </label>
            <Input type="file" accept="application/pdf" id="pdfInput" className={classes.input} color="primary"/>
            <Button type="submit" variant="contained" color="primary">upload</Button>
        </form>
    </div>
</div>

    );
}

export default PDFUploader;
