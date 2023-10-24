import React, {useState} from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Chip from '@mui/material-next/Chip';
import SendIcon from '@mui/icons-material/Send';
import {TextField} from "@mui/material";

function ChatBox() {
    const recommdMap = ['Hello', 'How are you?', 'Goodbye'];

    const [message, setMessage] = useState('');
    const [replies, setReplies] = useState([]);

    const sendMessage = async () => {
        try {
            // Add user message to chat
            setReplies(prev => [...prev, {type: 'user', message: message}]);

            // Send the message to the server
            const response = await axios.post('http://192.168.0.13:8988/chat', {message});

            // Split the received response into main message and metadata
            // Extract main message and metadata from the response
            // const [mainMessage, metaData] = response.data.reply.split("##");
            // console.log("Main Message:", mainMessage);
            // console.log("Metadata:", metaData);
            // Add bot reply to chat
            // setReplies(prev => [...prev, {type: 'bot', message: "Model: " + response.data.reply}]);
            setReplies(prev => [...prev, {type: 'bot', message: response.data.reply, metaData: response.data.source}]);
            // Clear the input
            setMessage('');
        } catch (error) {
            console.error("An error occurred while sending the message", error);
        }
    };

    const sendPresetMessage = async (presetMessage) => {
        setMessage(presetMessage);
        // await sendMessage();
    };


    return (
        <div style={{ margin: '0 auto'}}>
            <div style={{borderBottom:'1px solid #1976d2', height: '800px', overflowY: 'scroll'}}>
                {replies.map((reply, index) => (
                    <div
                        key={index}
                        style={{
                            display: 'flex',
                            justifyContent: reply.type === 'bot' ? 'flex-start' : 'flex-end',
                            marginBottom: '5px',
                            marginLeft: '8px',
                            marginRight: '8px'
                        }}
                    >
                        <p
                        style={{
                            backgroundColor: reply.type === 'bot' ? '#e0f7fa' : '#c8e6c9',
                            borderRadius: '5px',
                            padding: '10px',
                            marginBottom: '0'
                        }}
                    >
                        {reply.message}
                        {reply.metaData &&
                            <span style={{ fontStyle: 'italic', marginLeft: '5px',fontSize: 14}}>
                                <br />
                                {reply.metaData}
                            </span>
                        }
                    </p>
                    </div>
                ))}
            </div>
            <div style={{marginTop: '10px',paddingLeft:'20px'}}>
                <Stack direction="row" spacing={2}>
                    {recommdMap.map((msg, index) => (
                        <Button
                            key={index}
                            variant="outlined"
                            onClick={() => sendPresetMessage(msg)}
                        >
                            {msg}
                        </Button>
                    ))}
                </Stack>
            </div>
            <div style={{marginTop: '10px', padding: '10px'}}>
                <TextField value={message} variant="standard" placeholder="Ask a Question" size='medium'
                           onChange={(e) => setMessage(e.target.value)}
                           style={{width: '80%', marginRight: '10px'}}/>
                <Button variant="contained" endIcon={<SendIcon/>} onClick={sendMessage} style={{float: 'right'}}>
                    Send
                </Button>
            </div>
        </div>
    );
}

export default ChatBox;
