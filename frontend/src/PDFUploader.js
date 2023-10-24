import React from 'react';
import {Input, Button, IconButton} from "@material-ui/core";
import {makeStyles} from '@material-ui/core/styles';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';
import {Typography} from "@mui/material";


const useStyles = makeStyles((theme) => ({
    input: {
        display: 'none',
    },
    Button: {
        marginRight: theme.spacing(1)
    },
    buttonRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: theme.spacing(1),
    },
    buttonContainer: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
    },
    flexibleButton: {
        flex: 1,
        margin: theme.spacing(0, 1),  // Adjust as needed for spacing between buttons
    },
    enhancedButton: {
        padding: theme.spacing(2, 2),  // Increase vertical padding to increase height
        flex: 1,
        margin: theme.spacing(0, 1),  // Adjust as needed for spacing between buttons
    },
    firstButtonInRow: {
        marginLeft: 8,
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

    const handleDownload = () => {
        const filename = 'a078005_page-5.png';
        window.location.href = `http://localhost:8988/images/${filename}`;
    }


    return (
        <div>
            <div style={{textAlign: 'center'}}>
                <div className={classes.buttonRow}>
                    <form onSubmit={handleUpload} className={classes.buttonContainer}>
                        <label htmlFor="pdfInput" className={classes.flexibleButton} style={{marginLeft: 0}}>
                            <Button className={`${classes.enhancedButton} ${classes.firstButtonInRow}`}
                                    aria-label="upload picture" variant="outlined" component="span" color="primary"
                                    fullWidth>Select PDF</Button>
                        </label>
                        <input type="file" accept="application/pdf" id="pdfInput" className={classes.input}
                               color="primary"/>
                        <Button className={classes.enhancedButton} type="submit" variant="contained"
                                startIcon={<CloudUploadIcon/>} color="primary" fullWidth>Upload</Button>
                    </form>
                </div>
                <div className={classes.buttonRow}>
                    <Button className={classes.enhancedButton} variant="outlined" color="primary"
                            startIcon={<CloudDownloadIcon/>} onClick={handleDownload} fullWidth>Download</Button>
                </div>
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
