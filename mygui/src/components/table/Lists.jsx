import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import "./table.scss";

function Lists(props) {
    const ProductLists = props.ProductLists;
    // console.log(ProductListss);
    return (
        <TableContainer component={Paper} className="table" >
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell className="tableCell">Tracking ID</TableCell>
                        <TableCell className="tableCell">Product</TableCell>
                        <TableCell className="tableCell">Customer</TableCell>
                        <TableCell className="tableCell">Date</TableCell>
                        <TableCell className="tableCell">Amount</TableCell>
                        <TableCell className="tableCell">Payment Method</TableCell>
                        <TableCell className="tableCell">Status</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {ProductLists.map((ProductList) => (
                        <TableRow key={ProductList.id}>
                            <TableCell className="tableCell">{ProductList.id}</TableCell>
                            <TableCell className="tableCell">
                                <div className="cellWrapper">
                                    <img src={ProductList.img} alt="" className="image" />
                                    {ProductList.product}
                                </div>
                            </TableCell>
                            <TableCell className="tableCell">{ProductList.product_name}</TableCell>
                            <TableCell className="tableCell">{ProductList.total_comments}</TableCell>
                            <TableCell className="tableCell">{ProductList.rating_point}</TableCell>
                            <TableCell className="tableCell">{ProductList.method}</TableCell>
                            <TableCell className="tableCell">
                                <span className={`status ${ProductList.status}`}>{ProductList.status}</span>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}


export default Lists;