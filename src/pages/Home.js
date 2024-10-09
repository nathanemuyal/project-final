import G_button from '../component/G_button';
import Heading from '../component/Heading';
import '../style/Home.css';
import React from 'react';

const Home = () => {
    return (
        <div className='Home'>
            <Heading />
            <G_button />
            <p>conect your Gmail account for starting</p>
        </div>
    );
};

export default Home;