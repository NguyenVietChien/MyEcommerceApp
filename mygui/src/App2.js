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
class App2 extends Component {

    // let app = App3.items;

    render() {
        let app = App3.items;
        // const app3 = App3.items;

        return (
            <>
                <div className="row">
                    {app.map(country => {
                        return country.product_name;
                    })}
                </div>
                <EnhancedTable></EnhancedTable>
            </>

        );
    }
}
export default App2;
