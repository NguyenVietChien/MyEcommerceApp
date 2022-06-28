import PersonList from "./components/tests/PersonList.jsx";
import PersonAdd from "./components/tests/PersonAdd.jsx";
import { useEffect, useState } from "react";
import ReactPaginate from "react-paginate";
import FruitSelector from "./components/tests/Select.jsx";
// import Select from "./components/tests/Select.jsx";
import MediaCard from "./components/card/Card.js";
import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
// import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
// import Select from '@mui/material/Select';

import axios from 'axios';

function App3() {

    const [items, setItems] = useState([]);

    const [pageCount, setpageCount] = useState(0);

    const getInitialState = () => {
        const value = 1;
        return value;
    };

    const [value, setValue] = useState(getInitialState);

    // const handleChange = (e) => {
    //     setValue(e.target.value);
    // };

    let limit = 40;

    // console.log(limit)

    useEffect(() => {
        const getProduct = async (url, params) => {
            const res = await fetch(url, params);

            const data = await res.json();
            const total = data.count;
            setpageCount(Math.ceil(total / limit));
            setItems(data.results)
        };

        // getProduct(`http://127.0.0.1:8008/api/tasks/?p=1`, {});

        const price = {
            fromPrice: 120000,
            toPrice: 4000000,
        };

        // getProduct(urlQuery, { price });

    }, [limit]);



    // const fetchComments = async (url, currentPage) => {
    //     const res = await fetch(
    //         `${url}?p=${currentPage}`
    //     );
    //     const data = await res.json();

    //     return data;
    // };

    // const urlQuery = 'http://127.0.0.1:8008/api/tasks/set_query/';

    // const handlePageClick = async (data) => {
    //     console.log(data.selected + 1);
    //     let currentPage = data.selected + 1;
    //     const commentsFormServer = await fetchComments(urlQuery, currentPage);
    //     console.log(commentsFormServer);
    //     setItems(commentsFormServer.results);
    // };

    const [age, setAge] = React.useState('1');

    const handleChange = (event) => {
        setAge(event.target.value);
    };



    return (
        <div className="container">

            <PersonAdd></PersonAdd>

            {/* Chỗ này tạm ẩn để thử nghiệm trên PersonAdd */}
            {/* <div className="row m-2">
                {items.map((item) => {
                    return (
                        <div key={item.id} className="col-sm-6 col-md-3 v my-3">
                            <MediaCard Product={item}></MediaCard>
                        </div>

                    );
                })}
            </div>

            <ReactPaginate
                previousLabel={"previous"}
                nextLabel={"next"}
                breakLabel={"..."}
                pageCount={pageCount}
                marginPagesDisplayed={2}
                pageRangeDisplayed={4}
                onPageChange={handlePageClick}
                containerClassName={"pagination justify-content-center"}
                pageClassName={"page-item"}
                pageLinkClassName={"page-link"}
                previousClassName={"page-item"}
                previousLinkClassName={"page-link"}
                nextClassName={"page-item"}
                nextLinkClassName={"page-link"}
                breakClassName={"page-item"}
                breakLinkClassName={"page-link"}
                activeClassName={"active"}
            /> */}
        </div >
    )
}

export default App3;