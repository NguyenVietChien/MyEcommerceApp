
import axios from 'axios';
// import Box from '@mui/material/Box';
// import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

// import MediaCard from "./components/card/Card.js";
import * as React from 'react';
import ReactPaginate from "react-paginate";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
// import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import MediaCard from '../card/Card.js';
import { flexbox } from '@mui/system';


export default class PersonAdd extends React.Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    state = {
        minPrice: '',
        maxPrice: '',
        items: [],
        api: 'http://127.0.0.1:8008/purchases/?minPrice=',
        pageCount: 0,
        ordering: 'product_name',
        age2: `asc`,
    }


    componentDidMount() {
        let url = `http://127.0.0.1:8008/purchases/?ordering=${this.state.ordering}`;
        this.continuousRender(url);
    }

    handleChangeMinPrice = event => {
        this.setState({ minPrice: event.target.value }, () => {
            console.log(this.state.minPrice)
        });
    }
    handleChangeMaxPrice = event2 => {
        this.setState({ maxPrice: event2.target.value }, () => {
            console.log(this.state.maxPrice)
        });
    }

    handleChange = (events) => {
        events.preventDefault();
        this.setState({ ordering: events.target.value }, () => {
            console.log(this.state.ordering);
            let url = `http://127.0.0.1:8008/purchases/?ordering=${this.state.ordering}`;
            // let url = `http://127.0.0.1:8008/purchases/?minPrice=${this.state.minPrice}&maxPrice=${this.state.maxPrice}&ordering=${this.state.ordering}`;

            this.continuousRender(url);
        });
    };

    // handleChange2 = (event2) => {
    //     this.setState({ age2: event2.target.value });
    //     console.log(this.state.ordering)
    // };

    handleSubmit = event => {
        event.preventDefault();

        let url = `http://127.0.0.1:8008/purchases/?minPrice=${this.state.minPrice}&maxPrice=${this.state.maxPrice}&ordering=${this.state.ordering}`;

        this.continuousRender(url);
    }

    continuousRender(url) {
        this.setState({ api: url });

        axios.get(url)
            .then(res => {
                // console.log(res)
                const list = res.data.results;
                const total = res.data.count;
                let limit = 40;
                this.setState({
                    items: list,
                    pageCount: Math.ceil(total / limit),
                });
            })
    }

    fetchComments = async (url, currentPage) => {
        const res = await fetch(
            `${url}&p=${currentPage}`
        );
        const data = await res.json();
        return data;
    };

    handlePageClick = async (data) => {
        // console.log(data.selected + 1);
        let currentPage = data.selected + 1;
        const commentsFormServer = await this.fetchComments(this.state.api, currentPage);
        // console.log(commentsFormServer);
        this.setState({ items: commentsFormServer.results });
    };

    render() {
        const items = this.state.items;

        const styleDropdown = {
            justifyContent: `center`,
            display: `flexbox`,
            alignItems: `center`
        }
        return (
            <div>
                <Box sx={{ minWidth: 120 }} s
                // tyle={{ justifyContent: `center`, alignItems: `center`, margin: "10" }}
                >
                    <FormControl
                        style={styleDropdown}
                    >
                        <InputLabel id="demo-simple-select-label">Sắp xếp theo:</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={this.state.ordering}
                            label="Sắp xếp theo:"
                            size="small"
                            sx={{ minWidth: 160 }}
                            defaultValue="product_name"
                            style={styleDropdown}
                            onChange={this.handleChange}
                        // ref={this.input}
                        >
                            <MenuItem value={'product_name'}>Tên Sản Phẩm</MenuItem>
                            <MenuItem value={`product_price`}>Giá Sản Phẩm</MenuItem>
                            <MenuItem value={`rating_point`}>Điểm Đánh Giá</MenuItem>
                            <MenuItem value={`total_comments`}>Lượt Bình Luận</MenuItem>
                        </Select>
                        <h1>{this.state.ordering}</h1>
                    </FormControl>
                    {/* <FormControl style={{ justifyContent: `center`, display: `flexbox` }}> */}


                    {/* <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={this.state.ordering2}
                        label="Age"
                        size="small"
                        sx={{ minWidth: 120 }}
                        onChange={this.handleChange2}
                    >
                        <MenuItem value={`desc`}>Tăng dần</MenuItem>
                        <MenuItem value={`asc`}>Giảm dần</MenuItem>
                    </Select> */}


                    {/* </FormControl> */}
                    <TextField id="outlined-basic" label="Outlined" variant="outlined" size="small" onChange={this.handleChangeMinPrice} /> Đến
                    <TextField id="outlined-basic2" label="Outlined2" variant="outlined" size="small" onChange={this.handleChangeMaxPrice} />
                    <Button variant="contained" onClick={this.handleSubmit}>Lọc</Button>

                </Box>
                <br />
                <ReactPaginate
                    previousLabel={"previous"}
                    nextLabel={"next"}
                    breakLabel={"..."}
                    pageCount={this.state.pageCount}
                    marginPagesDisplayed={2}
                    pageRangeDisplayed={4}
                    onPageChange={this.handlePageClick}
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

                <div className="row m-2">
                    {items.map((item) => {
                        return (
                            <div key={Math.random()} className="col-sm-6 col-md-3 v my-3">
                                <MediaCard Product={item}></MediaCard>
                            </div>

                        );
                    })}
                </div>
            </div>
        )
    }
}