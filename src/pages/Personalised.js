import React from 'react';
import Haeding from '../component/Haeding';
import ToggleSwitch from '../component/ToggleSwitch';
import Date from '../component/Date';
import '../style/Personalised.css';

const Personalised = () => {
    return (
        <div>
            <Haeding />
            <div className="invoice-search">
                <div className="row">
                    <Date />
                    <span className="label">paid</span>
                    <ToggleSwitch />
                </div>
                <div className="row">
                    <span className="label">energy</span>
                    <ToggleSwitch />
                    <span className="label">property tax</span>
                    <ToggleSwitch />
                    <span className="label">communication</span>
                    <ToggleSwitch />
                </div>
                <div className="row">
                    <span className="label">health</span>
                    <ToggleSwitch />
                    <span className="label">sewerage charge</span>
                    <ToggleSwitch />
                    <span className="label">other</span>
                    <ToggleSwitch />
                </div>
                <button className="search-button">Search</button>
            </div>
        </div>
    );
};

export default Personalised;