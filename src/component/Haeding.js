import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { signOut } from 'firebase/auth';
import { auth } from '../firebase/firebase';
import "../style/Haeding.css"; // תיקון שם הקובץ

function Haeding() {
    const navigate = useNavigate();
    const location = useLocation();
    const user = auth.currentUser; // קבלת המשתמש המחובר

    const handleBackClick = async () => {
        await navigate(-1);
     

        if (location.pathname === '/') {
            try {
                await signOut(auth);
                console.log("User signed out");
                navigate('/'); // לאחר ניתוק, נשאר בדף הבית
            } catch (error) {
                console.error("Error signing out:", error);
            }
        } 
    };

    const handleSignOut = async () => {
        try {
            await signOut(auth);
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
                {user && (
                    <div className="user-info">
                        <img src={user.photoURL} alt="User" className="user-photo" />
                    </div>
                )}
                <img src="./image.png" alt="AI Logo" className="ai-logo" />
            </div>
        </header>
    );
}

export default Haeding;
