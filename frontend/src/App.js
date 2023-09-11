import React, {useState} from 'react';
import ReactDOM from 'react-dom';
import {makeStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import PhotoCamera from '@material-ui/icons/PhotoCamera';
import {Document, Page} from "react-pdf";
import PDFViewer from "./PDFViewer";


class App extends React.Component {
    render() {
        return (
            <div>
                <h1>VQA is Query Application!</h1>
                <p>Hello World!!!</p>
                <PDFViewer />
            </div>
        );
    }
}

export default App;
