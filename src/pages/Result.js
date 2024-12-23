import React from 'react';
import { useLocation } from 'react-router-dom';
import Heading from '../component/Heading';
import '../style/Result_line.css'

const Result = () => {
    const pdfClick = (pdfUrl) => {
        window.open(pdfUrl, '_blank'); // Opens the link in a new tab
            // Retrieve the access token from local storage

        // const accessToken = localStorage.getItem('auth_token');
        
        // if (!accessToken) {
        //     console.error('Access token not found in local storage.');
        //     return;
        // }
        // // make requst to server along with the access token

        // // Fetch the user picture from Flask
        // fetch(`http://localhost:5000/get_pdf`, {
        //     method: 'POST',
        //     headers: {
        //     'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ access_token: accessToken , pdf_url: pdfUrl}),  // Send the token to Flask
        // })
        //     .then(response => response.json())  // Get image as blob
        //     .then(data => {
        //         alert(data)
        //     })
        //     .catch(error => console.error('Error fetching profile picture:', error));


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
