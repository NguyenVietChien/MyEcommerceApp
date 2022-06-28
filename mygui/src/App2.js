// import Component from the react module
import React, { Component } from "react";
// import Modal from "./components/Modal";
import axios from 'axios';

import "./components/table/Lists.jsx";
import Pagination from '@mui/material/Pagination';
import Lists from "./components/table/Lists.jsx";
import { useEffect, useState } from "react";
import EnhancedTable from "./components/datatable/DataTables.jsx";
import App3 from "./App3.js";

// create a class that extends the component
class App2 extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: '' };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        event.preventDefault();
        this.setState({ value: event.target.value },
            () => {
                console.log("New state in ASYNC callback:", this.state.text);
            });
        console.log(this.state.value)
        event.preventDefault();
    }

    handleSubmit(event) {
        alert('A name was submitted: ' + this.state.value);
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Name:
                    <input type="text" value={this.state.value} onChange={this.handleChange} />
                </label>
                <input type="submit" value="Submit" />
            </form>
        );
    }
}
export default App2;
