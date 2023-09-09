import React from 'react';
import ReactDOM from 'react-dom';
import {makeStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import PhotoCamera from '@material-ui/icons/PhotoCamera';


const hidden_input = {
    display: 'none',
};

class App extends React.Component {
    render() {
        return (
            <div>
                <h1>VQA is Query Application!</h1>
                <p>Hello World!!!</p>
                <div>
                    <input
                        style={hidden_input}
                        accept="application/pdf"
                        id="contained-button-file"
                        multiple
                        type="file"
                    />
                    <label htmlFor="contained-button-file">
                        <Button variant="contained" color="primary" component="span">
                            Upload
                        </Button>
                    </label>
                </div>

            </div>
        );
    }
}

ReactDOM.render(<App/>, document.getElementById('root'))
