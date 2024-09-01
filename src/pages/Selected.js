import React from 'react';
import '../style/Selected.css';
import Haeding from '../component/Haeding';

const Selected = () => {
    return (
        <div>
            <Haeding/>
            <div className='sel_button'>
                <button className="select">
                    energy
                </button>
                <button className="select">
                    property tax
                </button>
                <button className="select">
                    communication
                </button>
                <button className="select">
                    health
                </button>
                <button className="select">
                    sewerage charge
                </button>
                <button className="select">
                    other
                </button>
                <button className="personalised">
                    personalised
                </button>
            </div>
        </div>
    );
};

export default Selected;