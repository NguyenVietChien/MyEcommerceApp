import * as React from 'react';
import './Card.css';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import Box from '@mui/material/Box';

function MediaCard(props) {
    const Product = props.Product;
    return (
        <Card sx={{ maxWidth: 250 }}>
            <CardMedia
                component="img"
                height="250"
                image="https://cf.shopee.vn/file/1b5ec336bea8aee0114c0bf9518d1f02_tn"
                alt="green iguana"

            />
            <CardContent class="product_name" >

                <Typography variant="" color="text.secondary" class="product_name">
                    {Product.product_name}
                </Typography>

                <Typography variant="" color="text.secondary" class="price">
                    đ{Product.product_price}
                </Typography>

                <Box component="div" sx={{ p: 2, border: '1px dashed grey' }} class="product_details">
                    <Rating name="half-rating-read" defaultValue={Product.rating_point} precision={0.25} size="small" readOnly />{Product.rating_point} |
                    <Typography variant="" color="text.secondary" class="product_name">
                        Đã bán 5,1K
                    </Typography>
                </Box>

                <Box component="div" sx={{ p: 2, border: '1px dashed grey' }} class="product_details">

                    <Typography variant="" color="text.secondary" class="product_name">
                        Hà Nội
                    </Typography>
                </Box>
            </CardContent>

        </Card>
    );
}




export default MediaCard;