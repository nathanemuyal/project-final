import React from 'react';
import '../style/Date.css';

const Date = () => {
    return (
        <div>
            <span className="label">date</span>
            <input type="date" className="date-input" defaultValue="2024-10-10" />
            <span className="arrow">→</span>
            <input type="date" className="date-input" defaultValue="2024-10-10" />

        </div>
    );
};

export default Date;