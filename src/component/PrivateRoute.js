/*
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebase/firebaseConfig';

const PrivateRoute = ({ children }) => {
    const navigate = useNavigate();

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            if (!user) {
                navigate('/');
            }
        });

        return () => unsubscribe();
    }, [navigate]);

    return children;
};

export default PrivateRoute;
*/

// src/component/PrivateRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { auth } from '../firebase/firebase';

const PrivateRoute = ({ children }) => {
    const user = auth.currentUser;

    return user ? children : <Navigate to="/" />;
};

export default PrivateRoute;

