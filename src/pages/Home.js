import React from 'react';
import G_button from '../component/G_button';
import Haeding from '../component/Haeding';
import '../style/Home.css';

const Home = () => {
    return (
        <div className='Home'>
            <Haeding />
            <G_button />
            <p>conect your Gmail account for starting</p>
        </div>
    );
};

export default Home;