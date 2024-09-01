import React from 'react';
import { signInWithPopup } from 'firebase/auth';
import { auth, googleProvider } from '../firebase/firebase';
import { useNavigate } from 'react-router-dom';
import { checkAndCreateUserPersonalArea } from '../services/firestoreService';
import { fetchAndProcessEmails } from '../services/gmailService';

import '../style/G_button.css';

function G_button() {
    const navigate = useNavigate();

    const handleSignIn = async () => {
        try {
            const result = await signInWithPopup(auth, googleProvider);
            const user = result.user;
            console.log(user);

            // בדיקה ויצירת אזור אישי למשתמש אם לא קיים
            await checkAndCreateUserPersonalArea(user);

            // קריאת אימיילים מהמשתמש ועיבוד קבצי PDF
            await fetchAndProcessEmails(user);

            // ניווט לעמוד שנבחר
            navigate('/Selected');
        } catch (error) {
            console.error('שגיאה במהלך הכניסה', error);
        }
    };

    return (
        <div>
            <button className="google-sign-in-button" onClick={handleSignIn}>
                <img src="./google-logo.png" alt="" className="google-logo" />
                התחבר עם Google
            </button>
        </div>
    );
}

export default G_button;
