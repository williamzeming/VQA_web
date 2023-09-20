import React, {useState} from 'react';
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
import PropTypes from 'prop-types';

function renderRow(props) {
    const {index, style} = props;

    return (
        <div>
            <ListItem button style={style} key={index}>
            <ListItemAvatar>
            <Avatar>
                <PictureAsPdfSharpIcon/>
            </Avatar>
            </ListItemAvatar>
            <ListItemText primary={`Filename ${index + 1}`} secondary="File path"/>
            </ListItem>
        </div>
    );
}

renderRow.propTypes = {
    index: PropTypes.number.isRequired,
    style: PropTypes.object.isRequired,
};


class App extends React.Component {
    render() {
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
                            <FixedSizeList height={600} itemSize={60} itemCount={15}>
                                {renderRow}
                            </FixedSizeList>
                        </Paper>
                        <br/>
                    </Grid>
                    <Grid item xs={4}>
                        <div align='center'>
                            <img src={simple} height={"800px"}/>
                        </div>
                    </Grid>
                    <Grid item xs={5}>
                        <div align='left'>
                            <ChatBox/>
                        </div>
                        <br />
                        <Paper elevation={2} style={{backgroundColor: 'white'}} sx={{
                            borderColor: 'black',
                            borderWidth: 2,
                            borderStyle: 'solid'
                        }}>
                            <div align='center'>
                            <PDFUploader/>
                        </div>
                        </Paper>
                    </Grid>
                </Grid>
            </div>


        )
    }
}

export default App;
