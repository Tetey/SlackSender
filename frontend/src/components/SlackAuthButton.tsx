import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Use environment variable with fallback
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const SlackAuthButton: React.FC = () => {
  const [authUrl, setAuthUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAuthUrl = async () => {
      try {
        setIsLoading(true);
        // Fetch the auth URL from the backend
        const response = await axios.get(`${API_BASE_URL}/api/slack/auth-url/`);
        setAuthUrl(response.data.url);
        setError(null);
      } catch (err) {
        console.error('Error fetching Slack auth URL:', err);
        setError('Failed to load Slack authentication URL');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAuthUrl();
  }, []);

  const handleAuth = () => {
    // Redirect to Slack OAuth page
    if (authUrl) {
      window.location.href = authUrl;
    } else {
      setError('Authentication URL not available. Please try again later.');
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <button
      onClick={handleAuth}
      className="bg-[#4A154B] hover:bg-[#611f69] text-white font-bold py-2 px-4 rounded flex items-center"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 122.8 122.8"
        className="h-5 w-5 mr-2"
      >
        <path
          d="M25.8 77.6c0 7.1-5.8 12.9-12.9 12.9S0 84.7 0 77.6s5.8-12.9 12.9-12.9h12.9v12.9zm6.5 0c0-7.1 5.8-12.9 12.9-12.9s12.9 5.8 12.9 12.9v32.3c0 7.1-5.8 12.9-12.9 12.9s-12.9-5.8-12.9-12.9V77.6z"
          fill="#e01e5a"
        />
        <path
          d="M45.2 25.8c-7.1 0-12.9-5.8-12.9-12.9S38.1 0 45.2 0s12.9 5.8 12.9 12.9v12.9H45.2zm0 6.5c7.1 0 12.9 5.8 12.9 12.9s-5.8 12.9-12.9 12.9H12.9C5.8 58.1 0 52.3 0 45.2s5.8-12.9 12.9-12.9h32.3z"
          fill="#36c5f0"
        />
        <path
          d="M97 45.2c0-7.1 5.8-12.9 12.9-12.9s12.9 5.8 12.9 12.9-5.8 12.9-12.9 12.9H97V45.2zm-6.5 0c0 7.1-5.8 12.9-12.9 12.9s-12.9-5.8-12.9-12.9V12.9C64.7 5.8 70.5 0 77.6 0s12.9 5.8 12.9 12.9v32.3z"
          fill="#2eb67d"
        />
        <path
          d="M77.6 97c7.1 0 12.9 5.8 12.9 12.9s-5.8 12.9-12.9 12.9-12.9-5.8-12.9-12.9V97h12.9zm0-6.5c-7.1 0-12.9-5.8-12.9-12.9s5.8-12.9 12.9-12.9h32.3c7.1 0 12.9 5.8 12.9 12.9s-5.8 12.9-12.9 12.9H77.6z"
          fill="#ecb22e"
        />
      </svg>
      Connect with Slack
    </button>
  );
};

export default SlackAuthButton;
