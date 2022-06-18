import PersonList from "./components/tests/PersonList.jsx";
import PersonAdd from "./components/tests/PersonAdd.jsx";
import { useEffect, useState } from "react";
import ReactPaginate from "react-paginate";
import FruitSelector from "./components/tests/Select.jsx";
import Select from "./components/tests/Select.jsx";
import MediaCard from "./components/card/Card.js";
import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

// import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
// import Select from '@mui/material/Select';

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
        const getProduct = async () => {
            const res = await fetch(
                `http://127.0.0.1:8008/api/tasks/?p=1`
            );
            const data = await res.json();

            const total = data.count;
            setpageCount(Math.ceil(total / limit));

            setItems(data.results)
        };

        let query = async () => {
            const res = await fetch(
                `http://127.0.0.1:8008/api/tasks`
            );
        }

        getProduct();

    }, [limit]);



    const fetchComments = async (currentPage) => {
        const res = await fetch(
            `http://127.0.0.1:8008/api/tasks/?p=${currentPage}`
        );
        const data = await res.json();

        return data;
    };

    const handlePageClick = async (data) => {
        console.log(data.selected + 1);

        let currentPage = data.selected + 1;

        const commentsFormServer = await fetchComments(currentPage);
        console.log(commentsFormServer);
        setItems(commentsFormServer.results);
        // scroll to the top
        //window.scrollTo(0, 0)
    };



    const [age, setAge] = React.useState('1');

    const handleChange = (event) => {
        setAge(event.target.value);
    };



    return (
        <div className="container">
            <Box sx={{ minWidth: 120 }}>
                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Age</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={age}
                        label="Age"
                        onChange={handleChange}
                    >
                        <MenuItem value={10}>Ten</MenuItem>
                        <MenuItem value={20}>Twenty</MenuItem>
                        <MenuItem value={30}>Thirty</MenuItem>
                    </Select>
                </FormControl>
            </Box>

            <PersonAdd></PersonAdd>
            <div className="row m-2">
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
            />
        </div >
    )
}

export default App3;