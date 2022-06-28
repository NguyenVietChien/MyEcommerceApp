import Sidebar from "../../components/sidebar/Sidebar";
import Navbar from "../../components/navbar/Navbar";
import "./home.scss";
import Widget from "../../components/widget/Widget";
import Featured from "../../components/featured/Featured";
import Chart from "../../components/chart/Chart";
import Table from "../../components/table/Table";
import App3 from "../../App3";
import PersonAdd from "../../components/tests/PersonAdd";
import * as React from 'react';
import ReactPaginate from "react-paginate";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
// import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import MediaCard from "../../components/card/Card";
import axios from 'axios';
// import Box from '@mui/material/Box';
// import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

class Home extends React.Component {
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
    total_product: 1,
    total_price: 1,
    priceDesc: false,
    sort: "default",
    priceAsc: false,
    soldOut: false,
    total_comments: 1,

  }


  componentDidMount() {
    let url;

    url = `http://127.0.0.1:8008/purchases/?ordering=${this.state.ordering}`;
    this.continuousRender(url);
    this.totalRender(`http://127.0.0.1:8008/api/tasks/set_query/`)
  }

  componentDidUpdate() {
    let url;
    if (this.state.minPrice !== '' && this.state.maxPrice !== '') {
      url = `http://127.0.0.1:8008/purchases/?minPrice=${this.state.minPrice}&maxPrice=${this.state.maxPrice}&sort=${this.state.sort}`;
      console.log(url)
      // this.continuousRender(url);
    }

  }

  totalRender(url) {

    axios.get(url)
      .then(res => {
        // console.log(res)
        this.setState({
          total_product: res.data.total,
          total_price: res.data.total_price,
          total_comments: res.data.total_comments,
        }, () => {
          // console.log(this.state.total_price.product_price__sum)

        })

      })
  }

  handleChangeMinPrice = event => {
    this.setState({ minPrice: event.target.value }, () => {
      // console.log(this.state.minPrice)
    });
  }
  handleChangeMaxPrice = event2 => {
    this.setState({ maxPrice: event2.target.value }, () => {
      // console.log(this.state.maxPrice)
    });
  }

  handleChange = (events) => {
    events.preventDefault();
    this.setState({ ordering: events.target.value }, () => {
      console.log(this.state.ordering);
      console.log("sort=" + this.state.sort);

      let url = `http://127.0.0.1:8008/purchases/?ordering=${this.state.ordering}`;
      // let url = `http://127.0.0.1:8008/purchases/?minPrice=${this.state.minPrice}&maxPrice=${this.state.maxPrice}&ordering=${this.state.ordering}`;

      this.continuousRender(url);
    });
  };


  // Start Handle event ratio Filter
  handleChangeHighPrice = (event2) => {
    this.setState({ sort: event2.target.value }, () => {
      // console.log("sort=" + this.state.sort);
      let url = `http://127.0.0.1:8008/purchases/?sort=${this.state.sort}`;

    });
  };

  handleChangeLowPrice = (event2) => {
    this.setState({ priceAsc: event2.target.value }, () => {
      console.log("Giá Cao :" + this.state.priceDesc);
      console.log("Giá Thấp :" + this.state.priceAsc);
      console.log("Bán Chạy :" + this.state.soldOut)
    });
  };

  handleChangeSoldOut = (event2) => {
    this.setState({ soldOut: event2.target.value }, () => {
      console.log("Giá Cao :" + this.state.priceDesc);
      console.log("Giá Thấp :" + this.state.priceAsc);
      console.log("Bán Chạy :" + this.state.soldOut)
    });
  };

  // End Handle event ratio Filter

  handleSubmit = event => {
    event.preventDefault();

    let url = `http://127.0.0.1:8008/purchases/?minPrice=${this.state.minPrice}&maxPrice=${this.state.maxPrice}&ordering=${this.state.ordering}`;

    this.continuousRender(url);
  }

  continuousRender(url) {

    axios.get(url)
      .then(res => {
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
      <div className="home">
        <Sidebar />
        <div className="homeContainer">
          <Navbar />
          <div className="widgets">
            <Widget type="user" amount={this.state.total_product} />
            <Widget type="order" amount={this.state.total_price.product_price__sum} />
            <Widget type="earning" amount={130} />
            <Widget type="balance" amount={140} />
          </div>
          <div className="charts">
            {/* <Featured /> */}
            {/* <Chart title="Last 6 Months (Revenue)" aspect={2 / 1} /> */}
          </div>
          <div className="listContainer">
            <div className="listTitle">Latest Transactions</div>
            {/* <Table /> */}
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
                  {/* <h1>{this.state.ordering}</h1> */}
                  <div onChange={this.handleChangeHighPrice.bind(this)} style={{ margin: 10 }}>

                    <input type="radio" className="btn-check" name="options" id="btn-check-outlined4" value="default" autoComplete="off" style={{ margin: 10 }} defaultChecked></input>
                    <label className="btn btn-outline-primary" htmlFor="btn-check-outlined4">Phổ Biến</label>

                    <input type="radio" className="btn-check" name="options" id="btn-check-outlined1" value="priceDesc" autoComplete="off" style={{ margin: 10 }}></input>
                    <label className="btn btn-outline-primary" htmlFor="btn-check-outlined1">Giá Cao</label>

                    <input type="radio" className="btn-check" name="options" id="btn-check-outlined2" value="priceAsc" autoComplete="off" style={{ margin: 10 }}></input>
                    <label className="btn btn-outline-primary" htmlFor="btn-check-outlined2">Gía Thấp</label>

                    <input type="radio" className="btn-check" name="options" id="btn-check-outlined3" value="topSelling" autoComplete="off" style={{ margin: 10 }}></input>
                    <label className="btn btn-outline-primary" htmlFor="btn-check-outlined3">Bán Chạy</label>
                  </div>

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

          </div>
        </div>
      </div>
    );
  }
};

export default Home;
