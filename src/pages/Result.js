import React from 'react';
import Result_line from '../component/Result_line';
import Haeding from '../component/Haeding';


const invoiceData = [
    { date: '01/01/2024', time: '24:00', description: 'energy', amount: '10,000$', status: 'paid' },
    { date: '01/01/2024', time: '24:00', description: 'energy', amount: '10,000$', status: 'paid' },
    { date: '01/01/2024', time: '24:00', description: 'energy', amount: '10,000$', status: 'paid' },
    { date: '01/01/2024', time: '24:00', description: 'energy', amount: '10,000$', status: 'paid' },
    { date: '01/01/2024', time: '24:00', description: 'energy', amount: '10,000$', status: 'paid' },
    { date: '01/01/2024', time: '24:00', description: 'energy', amount: '10,000$', status: 'paid' },
];

const Result = () => {
    return (
        <div>
            <Haeding />
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Description</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {invoiceData.map((invoice, index) => (
                        <Result_line
                            key={index}
                            date={invoice.date}
                            time={invoice.time}
                            description={invoice.description}
                            amount={invoice.amount}
                            status={invoice.status}
                        />
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Result;
