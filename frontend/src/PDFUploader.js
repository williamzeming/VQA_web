import React from 'react';
import {Input, Button, IconButton} from "@material-ui/core";
import {makeStyles} from '@material-ui/core/styles';
import AttachFileIcon from '@material-ui/icons/AttachFile';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';
import {Typography} from "@mui/material";

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
            display: 'none',
        },
    button: {
        marginRight: theme.spacing(2),
    },
}));


function PDFUploader() {
    const [s_open, sets_Open] = React.useState(false);
    const [e_open, sete_Open] = React.useState(false);
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
            if ("error" in data) {
                sete_Open(true)
            } else {
                sets_Open(true)
            }
        } catch (error) {
            console.error("Upload error", error);

        }
    };


    return (
        <div>
            <div style={{textAlign:'center'}}>
                <h2>Upload your PDF</h2>
                <form onSubmit={handleUpload}>
                    <label htmlFor="pdfInput">
                        <Button aria-label="upload picture" variant="outlined" component="span" color="primary" className={classes.button}>Choose a PDF</Button>
                    </label>
                    <input type="file" accept="application/pdf" id="pdfInput" className={classes.input}
                           color="primary"/>
                    <Button type="submit" variant="contained" startIcon={<CloudUploadIcon />} color="primary">Upload file</Button>
                </form>
            </div>
            <div>
                <Box sx={{width: '100%'}}
                     justifyContent="center"
                     alignItems="center"
                     flexDirection="column">
                    <Collapse in={s_open}>
                        <Alert severity="success"
                               action={
                                   <IconButton
                                       aria-label="close"
                                       color="inherit"
                                       size="medium"
                                       onClick={() => {
                                           sets_Open(false);
                                       }}
                                   >
                                       <CloseIcon fontSize="inherit"/>
                                   </IconButton>
                               }
                               sx={{mb: 2}}
                        >
                            <Typography variant="h6">
                                File uploaded successfully
                            </Typography>
                        </Alert>
                    </Collapse>
                    <Collapse in={e_open}>
                        <Alert severity="error"
                               action={
                                   <IconButton
                                       aria-label="close"
                                       color="inherit"
                                       size="medium"
                                       onClick={() => {
                                           sete_Open(false);
                                       }}
                                   >
                                       <CloseIcon fontSize="inherit"/>
                                   </IconButton>
                               }
                               sx={{mb: 2}}
                        >
                            <Typography variant="h6">
                                File uploaded error
                            </Typography>
                        </Alert>
                    </Collapse>
                </Box>
            </div>
        </div>

    );
}

export default PDFUploader;
