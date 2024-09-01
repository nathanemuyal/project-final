import React, { useState } from 'react';
import '../style/ToggleSwitch.css';

const ToggleSwitch = () => {
    const [isOn, setIsOn] = useState(false);

    const handleToggle = () => {
        setIsOn(!isOn);
    };

    return (
        <div className="toggle-switch" onClick={handleToggle}>
            <div className={`switch ${isOn ? 'on' : 'off'}`}></div>

        </div>
    );
};

export default ToggleSwitch;

