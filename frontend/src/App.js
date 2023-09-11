import React, {useState} from 'react';
import Button from "@material-ui/core/Button";
import Grid from '@material-ui/core/Grid';
import PDFUploader from "./PDFUploader";
import ChatBox from "./ChatBox";
import simple from './simple_img.png'
const hidden_input = {
    display: 'none',
};

class App extends React.Component {
    render() {
        return (
            <div>
                <h1 align='center'>VQA is Query Application!</h1>
                <div align='left'>
                    <img src={simple} height={"500px"}/>
                </div>
                <div align='left'>
                    <ChatBox />
                </div>
                <div align='left'>
                    <PDFUploader />
                </div>

            </div>


        )
    }
}

export default App;
