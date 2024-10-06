import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import '../style/G_button.css';

const G_button = ({ setUserPhoto }) => {
  const client_id = process.env.REACT_APP_CLIENT_ID;
  const redirect_uri = 'http://localhost:5000/auth/callback';  // Flask server callback URI
  const navigate = useNavigate(); // To redirect to another route

  const handleSignIn = () => {
    const scope = 'openid email profile https://www.googleapis.com/auth/gmail.readonly';
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


      // Fetch the user picture from Flask
      fetch(`http://localhost:5000/get_profile_pic`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ access_token: token }),  // Send the token to Flask
      })
        .then(response => response.json())  // Get image as blob
        .then(data => {
            let profilePicUrl = data.profile_pic_url;

            profilePicUrl = './image.png'


            setUserPhoto(profilePicUrl);  // Set the profile picture URL using the prop
        })
        .catch(error => console.error('Error fetching profile picture:', error));
      // Redirect to the private route
      navigate('/Selected');
    }
  }, [navigate]);

  return (
    <div>
      <button className="google-sign-in-button" onClick={handleSignIn}>
          <img src="./google-logo.png" alt="" className="google-logo" />
          התחבר עם Google
      </button>
    </div>

  );
};

export default G_button;