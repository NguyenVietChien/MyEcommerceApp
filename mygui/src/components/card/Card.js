import * as React from 'react';
import './Card.scss';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import Box from '@mui/material/Box';
import { CardActionArea, Link } from '@mui/material';


const style = {
    display: 'flexbox',

}

function MediaCard(props) {
    const Product = props.Product;

    const currencyFormat = Product.product_price.toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,') + ' đ'


    return (
        <Card sx={{ maxWidth: 250 }}>
            <CardActionArea>
                <Link href={Product.product_link} underline="none" target="_blank">
                    <CardMedia
                        component="img"
                        height="250"
                        image={Product.product_thumbnail}
                        alt="green iguana"

                    />
                    <CardContent className="product_name" >

                        <Typography variant="" color="text.secondary" className="product_name">
                            {Product.product_name}
                        </Typography>

                        <Typography variant="" color="text.secondary" className="price">
                            {currencyFormat}
                        </Typography>

                        <Box component="div"
                            // sx={{ p: 2, border: '1px dashed grey' }}
                            className="product_details">
                            <Rating name="half-rating-read" defaultValue={Product.rating_point} precision={0.25} size="small" readOnly />{Product.rating_point} |
                            <Typography variant="" color="text.secondary" className="product_name">
                                Đã bán 5,1K
                            </Typography>
                        </Box>

                        <Box component="div"
                            // sx={{ p: 2, border: '1px dashed grey' }} 
                            className="product_details">

                            <Typography variant="" color="text.secondary" className="product_name">
                                Hà Nội
                            </Typography>
                        </Box>
                    </CardContent>
                </Link>
            </CardActionArea>
        </Card>
    );
}




export default MediaCard;