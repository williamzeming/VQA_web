import axios from 'axios';
import React, {useEffect, useState} from 'react';
import Button from "@material-ui/core/Button";
import Grid from '@material-ui/core/Grid';
import PDFUploader from "./PDFUploader";
import ChatBox from "./ChatBox";
import Container from '@mui/material/Container';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import PictureAsPdfSharpIcon from '@mui/icons-material/PictureAsPdfSharp';
import {Divider, ListSubheader, Paper} from "@mui/material";
import {FixedSizeList} from 'react-window';
import './App.css';


function App() {

    const uploadButton = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'flex-start'
    };

    const [files, setFiles] = useState([]);
    const [pdfUrl, setPdfUrl] = useState("");

    const handleClick = async (filename) => {
        try {
            const response = await axios.post('http://127.0.0.1:8988/get_filepath', {
                filename: filename
            });
            setPdfUrl(`http://127.0.0.1:8988/pdfs/${encodeURIComponent(response.data.filepath)}`);
        } catch (error) {
            console.error("An error occurred while fetching the file path: ", error);
        }
    };

    useEffect(() => {
        const fetchFiles = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8988/get_filelist');
                setFiles(response.data);
            } catch (error) {
                console.error("An error occurred while fetching the data: ", error);
            }
        };
        fetchFiles();
    }, []);

    const renderRow = (props) => {
        const {index, style} = props;

        return (
            <div>
                <ListItem button style={style} key={index} onClick={() => handleClick(files[index])}>
                    <ListItemAvatar>
                        <Avatar>
                            <PictureAsPdfSharpIcon/>
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary={files[index]}/>
                </ListItem>
            </div>
        );
    };

    return (
        <div style={{backgroundColor: 'aliceblue'}}>
            {/*<Container maxWidth='xl' style={{backgroundColor: 'aliceblue'}}>*/}
                <h1 align='center'>VQA is Query Application!</h1>
                <Grid container spacing={2}>
                    <Grid item xs={3} md={3}  lg={2} xl={1}>
                        <Paper elevation={2} style={{backgroundColor: 'white'}} sx={{
                            borderColor: 'black',
                            borderWidth: 2,
                            borderStyle: 'solid'
                        }}>
                            <ListSubheader>Uploaded Files</ListSubheader>
                            <FixedSizeList height={750} itemSize={50} itemCount={files.length}>
                                {renderRow}
                            </FixedSizeList>
                        </Paper>
                    </Grid>
                    <Grid item xs={4} md={5} lg={5} xl={5}>
                        <div align='center'>
                            <div className="App">
                                {pdfUrl ? (
                                    <iframe
                                        src={pdfUrl}
                                        width="100%"
                                        height="800"
                                        type="application/pdf"
                                        className="PdfFrame"
                                    >
                                    </iframe>
                                ) : (
                                    <p>Loading PDF...</p>
                                )}
                            </div>
                        </div>
                    </Grid>
                    <Grid item xs={3} md={4} lg={5} xl={6}>
                        <div align='left'>
                            <ChatBox/>
                        </div>
                        <br/>
                    </Grid>
                </Grid>
                <div style={uploadButton}>
                    <PDFUploader/>
                </div>
            {/*</Container>*/}
        </div>


    )
}


export default App;
