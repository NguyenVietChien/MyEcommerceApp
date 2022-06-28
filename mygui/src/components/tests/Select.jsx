import React, { useState } from "react";

export default function Selects() {
    const getInitialState = () => {
        const value = 1;
        return value;
    };

    const [value, setValue] = useState(getInitialState);

    const handleChange = (e) => {
        setValue(e.target.value);
    };

    return (
        <div>
            <select value={value} onChange={handleChange}>
                <option value="10">1</option>
                <option value="15">2</option>
                <option value="20">3</option>
            </select>
            <p>{`You selected ${value}`}</p>
        </div>
    );
}

// export default Select;