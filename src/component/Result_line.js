import React from 'react';
import '../style/Result_line.css'
const Result_line = ({ date, time, description, amount, status }) => {
    return (
        <tr>
            <td>{date}</td>
            <td>{time}</td>
            <td>{description}</td>
            <td>{amount}</td>
            <td>{status}</td>
            <td>
                <button>view PDF</button>
            </td>
        </tr>
    );
};

export default Result_line;

