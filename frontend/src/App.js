import axios from 'axios';
import React, {useEffect, useState} from 'react';
import Grid from '@material-ui/core/Grid';
import PDFUploader from "./PDFUploader";
import ChatBox from "./ChatBox";

import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import PictureAsPdfSharpIcon from '@mui/icons-material/PictureAsPdfSharp';
import {Divider, ListSubheader, Paper} from "@mui/material";
import {FixedSizeList} from 'react-window';
import './App.css';
import Box from "@mui/material/Box";
import logo from './logo.png';

function App() {

    const uploadButton = {
        display: 'flex',
        justifyContent: 'center',
        marginTop: 'auto',
        paddingBottom: '5%'
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
                if (response.data.includes("[SAMPLE] welcome.pdf")) {
                    handleClick("[SAMPLE] welcome.pdf");
                }
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
        <div style={{backgroundColor: 'aliceblue', height: '100vh'}}>
            {/*<Container maxWidth='xl' style={{backgroundColor: 'aliceblue'}}>*/}

            <Grid container spacing={3} style={{height: '100%'}}>
                <Grid item xs={3} md={4} lg={2} xl={2} style={{height: '100%'}}>
                    <Paper
                        elevation={5}
                        style={{
                            backgroundColor: 'white',
                            height: '100%',
                            display: 'flex',
                            flexDirection: 'column',
                            justifyContent: 'space-between'
                        }}
                        sx={{
                            borderColor: 'grey',
                            borderWidth: 1,
                            borderStyle: 'black'
                        }}
                    >
                        {/*<ListSubheader>Uploaded Files</ListSubheader>*/}
                        <Box
                            component="img"
                            sx={{
                                width: '100%',
                                borderRadius: '8px',
                                paddingTop:2,
                                paddingBottom:5
                            }}
                            alt="logo"
                            src={logo}
                        />

                        <FixedSizeList height={730} itemSize={50} itemCount={files.length}>
                            {renderRow}
                        </FixedSizeList>
                        <div style={uploadButton}>
                            <PDFUploader/>
                        </div>
                    </Paper>
                </Grid>
                <Grid item xs={4} md={5} lg={6} xl={5} style={{height: '100vh', padding: 0}}>
                    <div style={{height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                        <Paper elevation={5} style={{height: '100%', width: '100%'}}>
                            <div className="App" style={{height: '100%'}}>
                                {pdfUrl ? (
                                    <iframe
                                        src={pdfUrl}
                                        width="100%"
                                        height="100%"
                                        type="application/pdf"
                                        className="PdfFrame"
                                        style={{border: 'none'}}  // to remove any default borders
                                    ></iframe>
                                ) : (
                                    <p>Loading PDF...</p>
                                )}
                            </div>
                        </Paper>
                    </div>
                </Grid>

                <Grid item xs={4} md={3} lg={4} xl={5} style={{height: '100%'}}>
                    <Paper elevation={5}>
                        <div align='left'>
                            <ChatBox/>
                        </div>
                    </Paper>

                </Grid>
            </Grid>
        </div>


    )
}


export default App;
