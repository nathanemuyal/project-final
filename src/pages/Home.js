import G_button from '../component/G_button';
import Haeding from '../component/Haeding';
import '../style/Home.css';
import React, { useState } from 'react';

const Home = () => {


    const [userPhoto, setUserPhoto] = useState('./image.png');  // State to hold the user's photo URL


    return (
        <div className='Home'>
            {/* <Haeding /> */}
            {/* <G_button /> */}


            <Haeding photoURL={{userPhoto }} />
            <G_button setUserPhoto={setUserPhoto} />



            <p>conect your Gmail account for starting</p>
        </div>
    );
};

export default Home;