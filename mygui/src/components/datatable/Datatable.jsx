import "./datatable.scss";
import { DataGrid } from "@mui/x-data-grid";
import { userColumns, userRows } from "../../datatablesource";
import { Link } from "react-router-dom";
// import { useState } from "react";
import { useEffect, useState } from "react";
import ReactPaginate from "react-paginate";

const Datatable = () => {
  const [data, setData] = useState(userRows);


  const [items, setItems] = useState([]);

  const [pageCount, setpageCount] = useState(0);


  let limit = 40;

  // console.log(limit)

  // const getid = () => {
  //   random1 = Math.floor(Math.random() * 100);
  //   random2 = Math.floor(Math.random() * 100);
  //   var id = random1 * random2;
  //   return id
  // }

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

  const handleDelete = (id) => {
    setData(items.filter((item) => item.id !== id));
  };

  const actionColumn = [
    {
      field: "action",
      headerName: "Action",
      width: 200,
      renderCell: (params) => {
        return (
          <div className="cellAction">
            <Link to="/users/test" style={{ textDecoration: "none" }}>
              <div className="viewButton">View</div>
            </Link>
            <div
              className="deleteButton"
              onClick={() => handleDelete(params.row.id)}
            >
              Delete
            </div>
          </div>
        );
      },
    },
  ];
  return (

    <>
      <div className="datatable">
        <div className="datatableTitle">
          Add New User
          <Link to="/users/new" className="link">
            Add New
          </Link>
        </div>
        <DataGrid
          className="datagrid"
          rows={data}
          columns={userColumns.concat(actionColumn)}
          pageSize={9}
          rowsPerPageOptions={[9]}
          checkboxSelection
        />
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
    </>
  );
};

export default Datatable;
