import React from 'react';
import axios from 'axios';
import { useEffect, useState } from "react";

export default class PersonList extends React.Component {
    state = {
        persons: [],
    }

    componentDidMount() {
        // axios.get("http://127.0.0.1:8008/api/tasks/?p=4")
        //     .then(res => {
        //         const persons = res.data;
        //         this.setState({ persons });
        //     })

        // const [items, setItems] = useState([]);

        // const [pageCount, setpageCount] = useState(0);

        // let limit = 10;

        // useEffect(() => {
        //     const getComments = async () => {
        //         const res = await fetch(
        //             // `http://localhost:3001/comments?_page=1&_limit=${limit}`
        //             `http://127.0.0.1:8008/api/tasks/?p=4`
        //         );
        //         const data = await res.json();
        //         console.log(data)

        //         // const total = res.headers.get("x-total-count");
        //         // setpageCount(Math.ceil(total / limit));
        //         // console.log(Math.ceil(total/12));
        //         // setItems(data);
        //     };

        //     getComments();
        // }, [limit]);
    }



    render() {
        return (
            <ul>
                {
                    this.state.persons
                        .map(person =>
                            <li>{person.product_name}</li>
                        )
                }
            </ul>
        )
    }
}