// import { Component } from "react";
import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { height } from '@mui/system';
import axios from 'axios';
import { FormControl } from '@mui/material';

const style = {
    // alignItems: `center`,
    // justifyContent: 'center',
    // textAlign: 'center',
    display: 'block'
}

const buttonStyle = {
    width: 80,
    height: 40
}

class CrawlSearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = { value: '1' };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange = (event) => {
        this.setState({ value: event.target.value });
        console.log(this.state.value);
    }

    handleSubmit(events) {
        alert('A name was submitted: ' + this.state.value);
        events.preventDefault();
    }

    handleChange2 = (event) => {
        // event.preventDefault();
        this.setState({ value: event.target.value });
        console.log(this.state.value);
        this.continuousRender(`http://127.0.0.1:8008/api/crawl/`);
        // event.preventDefault();
    };

    continuousRender(url) {

        const keyword = this.state.value;

        let tikiUrl = "https://tiki.vn/search?q=" + keyword.replace(/\s/g, '+');
        let shopeeUrl = "https://shopee.vn/search?keyword=" + keyword.replace(/\s/g, '%20');
        let lazadaUrl = "https://www.lazada.vn/catalog/?q=" + keyword.replace(/\s/g, '+') + "&_keyori=ss&from=input&spm=a2o4n.home.search.go.27f86afeOMumZF";

        const urls = {
            tikiUrl: tikiUrl,
            shopeeUrl: shopeeUrl,
            lazadaUrl: lazadaUrl
        }

        axios.post(url, urls)
            .then(res => {
                // console.log(res);
            })
    }


    render() {

        return (
            <FormControl
                // component="form"
                sx={{
                    '& > :not(style)': { m: 1, width: '25ch' },
                }}

                style={style}
                onSubmit={this.handleSubmit}
            >
                {/* <form onSubmit={this.handleSubmit}> */}
                <TextField id="outlined-basic" label="Tìm Kiếm" variant="outlined" size="small"
                    onChange={this.handleChange}
                />

                <Button variant="contained" size="small" color='success' style={buttonStyle} onClick={this.handleChange2}>Start</Button>
                {/* </form> */}

            </FormControl>
            // </Box>

        )
    }
}
export default CrawlSearch;