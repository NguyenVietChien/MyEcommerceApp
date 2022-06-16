import { useState, useEffect } from "react";
import axios from "axios";
// import List from "./"

function Crawl() {

    const [notes, setNewNotes] = useState(null)
    const [formNote, setFormNote] = useState({
        title: "",
        content: ""
    })

    useEffect(() => {
        getNotes()
    }, [])

    function getNotes() {
        axios({
            method: "GET",
            url: "api/crawl/",
        }).then((response) => {
            const data = response.data
            setNewNotes(data)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response);
                console.log(error.response.status);
                console.log(error.response.headers);
            }
        })
    }

    return (
        <div className="App"></div>
    );

}

export default Crawl;