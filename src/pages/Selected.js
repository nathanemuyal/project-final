// import React from 'react';
// import '../style/Selected.css';
// import Haeding from '../component/Haeding';

// const Selected = () => {
//     return (
//         <div>
//             <Haeding/>
//             <div className='sel_button'>
//                 <button className="select">
//                     energy
//                 </button>
//                 <button className="select">
//                     property tax
//                 </button>
//                 <button className="select">
//                     communication
//                 </button>
//                 <button className="select">
//                     health
//                 </button>
//                 <button className="select">
//                     sewerage charge
//                 </button>
//                 <button className="select">
//                     other
//                 </button>
//                 <button className="personalised">
//                     personalised
//                 </button>
//             </div>
//         </div>
//     );
// };

// export default Selected


import React from 'react';
import { useNavigate } from 'react-router-dom'; // for navigation
import '../style/Selected.css';
import Haeding from '../component/Haeding';

const Selected = () => {
    const navigate = useNavigate();

    const handleButtonClick = async (category) => {
        const token = localStorage.getItem('auth_token'); // Retrieve token from localStorage

        if (!token) {
            console.error('No access token found');
            return;
        }

        try {
            // Send POST request to the server
            const response = await fetch('http://localhost:5000/sort', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    access_token: token,
                    category: category
                }),
            });

            const data = await response.json();


            navigate('/result', { state: { data: data } });

        } catch (error) {
            console.error('Error while fetching data from the server:', error);
        }
    };

    return (
        <div>
            <Haeding />
            <div className='sel_button'>
                <button className="select" onClick={() => handleButtonClick('energy')}>
                    energy
                </button>
                <button className="select" onClick={() => handleButtonClick('property tax')}>
                    property tax
                </button>
                <button className="select" onClick={() => handleButtonClick('communication')}>
                    communication
                </button>
                <button className="select" onClick={() => handleButtonClick('health')}>
                    health
                </button>
                <button className="select" onClick={() => handleButtonClick('sewage bill')}>
                    sewerage charge
                </button>
                <button className="select" onClick={() => handleButtonClick('other')}>
                    other
                </button>
                <button className="personalised" onClick={() => handleButtonClick('personalised')}>
                    personalised (implement)
                </button>
            </div>
        </div>
    );
};

export default Selected;