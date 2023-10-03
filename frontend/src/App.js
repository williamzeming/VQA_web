import axios from 'axios';
import React, {useEffect, useState} from 'react';
import Button from "@material-ui/core/Button";
import Grid from '@material-ui/core/Grid';
import PDFUploader from "./PDFUploader";
import ChatBox from "./ChatBox";
import simple from './simple_img.png'

import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import ImageIcon from '@material-ui/icons/Image';
import WorkIcon from '@material-ui/icons/Work';
import BeachAccessIcon from '@material-ui/icons/BeachAccess';
import PictureAsPdfSharpIcon from '@mui/icons-material/PictureAsPdfSharp';
import {Divider, ListSubheader, Paper} from "@mui/material";
import {FixedSizeList} from 'react-window';
import pdf from "./a075795_e2801187_2007ps_final_070823_14413304_1.pdf"


function App() {
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
        <div>
            <h1 align='center'>VQA is Query Application!</h1>
            <Grid container spacing={3}>
                <Grid item xs={2}>
                    <Paper elevation={2} style={{backgroundColor: 'white'}} sx={{
                        borderColor: 'black',
                        borderWidth: 2,
                        borderStyle: 'solid'
                    }}>
                        <ListSubheader>Uploaded Files</ListSubheader>
                        <FixedSizeList height={600} itemSize={60} itemCount={files.length}>
                            {renderRow}
                        </FixedSizeList>
                    </Paper>
                    <br/>
                </Grid>
                <Grid item xs={5} lg={5}>
                    <div align='center'>
                        <div className="App">
                            {pdfUrl ? (
                                <iframe
                                    src={pdfUrl}
                                    width="600"
                                    height="800"
                                    type="application/pdf"
                                >
                                </iframe>
                            ) : (
                                <p>Loading PDF...</p>
                            )}
                        </div>
                    </div>
                </Grid>
                <Grid item xs={4} lg={4}>
                    <div align='left'>
                        <br/>
                        <br/>
                        <br/>
                        <br/>
                        <br/>
                        <ChatBox/>
                    </div>
                    <br/>
                    <div>
                        <PDFUploader/>
                    </div>

                </Grid>
            </Grid>
        </div>


    )
}


export default App;
