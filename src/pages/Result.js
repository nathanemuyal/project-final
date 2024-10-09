import React from 'react';
import { useLocation } from 'react-router-dom';
import Heading from '../component/Heading';

const Result = () => {
    const pdfClick = (pdfUrl) => {
        window.open(pdfUrl, '_blank'); // Opens the link in a new tab
    };

    const location = useLocation();
    const data = location.state?.data || [];

    // Ensure data is an array before trying to map over it
    if (!Array.isArray(data)) {
        return <div>No valid data available.</div>;
    }

    return (
        <div>
            <Heading />
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Company</th>
                        <th>Category</th>
                        <th>Currency</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Pdf</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {data.length > 0 ? (
                        data.map((item, index) => (
                            <tr key={index}>
                                <td>{item.date}</td>
                                <td>{item.company}</td>
                                <td>{item.category}</td>
                                <td>{item.currency}</td>
                                <td>{item.amount}</td>
                                <td>{item.status}</td>
                                <td>
                                    <button onClick={() => pdfClick(item.pdf)}>View Pdf</button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="6">No data available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default Result;
