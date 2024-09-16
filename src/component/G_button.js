import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const G_button = () => {
  const client_id = process.env.REACT_APP_CLIENT_ID;
  const redirect_uri = 'http://localhost:5000/auth/callback';  // Flask server callback URI
  const navigate = useNavigate(); // To redirect to another route

  const handleSignIn = () => {
    const scope = 'https://www.googleapis.com/auth/gmail.readonly';
    const oauth2Url = `https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope}&access_type=offline`;

    // Redirect to Google's OAuth2 consent screen
    window.location.href = oauth2Url;
  };

  // This will check if the URL has a token after redirection from the Flask server
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token'); // Assuming token comes as a query param

    if (token) {
      // Store token securely (could be localStorage or sessionStorage)
      localStorage.setItem('auth_token', token);

      // Redirect to the private route
      navigate('/Selected');
    }
  }, [navigate]);

  return (
    <button onClick={handleSignIn}>
      Sign in with Gmail Access
    </button>
  );
};

export default G_button;