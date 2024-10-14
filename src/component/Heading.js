import React, {useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import "../style/Heading.css"; // תיקון שם הקובץ

const Heading = () => {
    const imageRef = useRef(null);
    const navigate = useNavigate();
    const location = useLocation();
    const [profilePicUrl, setProfilePicUrl] = useState('');
    useEffect(() => {
        const storedProfilePicUrl = localStorage.getItem('profilePicUrl');
        if (storedProfilePicUrl) {
            setProfilePicUrl(storedProfilePicUrl);
            imageRef.current.style.display = 'inline';
        }
    }, []);

    const handleBackClick =  () => {
        navigate(-1);

        if (location.pathname === '/Selected') {
            try {
                // await signOut(auth);
                localStorage.removeItem('auth_token');
                localStorage.removeItem('profilePicUrl');
                console.log("User signed out");
                navigate('/'); // לאחר ניתוק, נשאר בדף הבית
            } catch (error) {
                console.error("Error signing out:", error);
            }
        } 
    };

    const handleSignOut = async () => {
        try {
            // await signOut(auth);
            localStorage.removeItem('auth_token');
            localStorage.removeItem('profilePicUrl');
            console.log("User signed out");
            navigate('/'); // לאחר התנתקות, נווט לדף הבית
        } catch (error) {
            console.error("Error signing out:", error);
        }
    };

    return (
        <header className="header">
            <div className="button-container">
                <button className="back-button" onClick={handleBackClick}>
                    <span className="arrow-left"></span>
                    Back
                </button>
                <button className="logout-button" onClick={handleSignOut}>
                    Log Out
                </button>
            </div>
            <h1>AI - Invoice</h1>
            <div className="user_and_logo">
                <div className="user-info">
                    <img 
                        ref={imageRef}
                        src={profilePicUrl} 
                        alt='' className="user-photo" 
                        style={{display:'none'}}
                    />
                </div>
                <img src="./image.png" alt="AI Logo" className="ai-logo"/>

            </div>
        </header>
    );
}

export default Heading;
