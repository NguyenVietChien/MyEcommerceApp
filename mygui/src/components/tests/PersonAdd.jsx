import React from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default class PersonAdd extends React.Component {
    state = {
        fromPrice: '',
        toPrice: ''
    }

    handleChange = event => {
        this.setState({ fromPrice: event.target.value });
        this.setState({ toPrice: event.target.value });
        // this.setState({ toPrince: event.target.value });
        console.log(this.state.fromPrice)
    }

    handleChange2 = event2 => {
        console.log(this.state.toPrince)
        this.setState({ toPrice: event2.target.value });
        // this.setState({ toPrince: event.target.value });
        // this.handleSubmit
    }

    handleSubmit = event => {
        event.preventDefault();

        const price = {

            fromPrice: this.state.fromPrice,
            toPrice: this.state.toPrince,
        };
        // console.log(data);
        // const data = JSON.stringify(data1)
        axios.post(`http://127.0.0.1:8008/api/tasks/set_query/`, { price })
            .then(res => {
                this.setState({ price });
                // console.log(res);
                // console.log(price);
            }

            )
    }

    render() {
        return (
            <div>
                <form>
                    {/* <label>
                        Person Name:
                        <input type="text" name="name" onChange={this.handleChange} />
                    </label>
                    <button type="submit">Add</button> */}


                    <TextField id="outlined-basic" label="Outlined" variant="outlined" size="small" onChange={this.handleChange} />
                    <TextField id="outlined-basic2" label="Outlined" variant="outlined" size="small" onChange={this.handleChange} />
                    <Button variant="contained" onClick={this.handleSubmit}>Contained</Button>
                </form>
            </div>
        )
    }
}