import React from 'react';
import '../style/Result_line.css'
const Result_line = ({ date, company, category, amount, status }) => {
    return (
        <tr>
            <td>{date}</td>
            <td>{company}</td>
            <td>{category}</td>
            <td>{amount}</td>
            <td>{status}</td>
            <td>
                <button>view PDF</button>
            </td>
        </tr>
    );
};

export default Result_line;

