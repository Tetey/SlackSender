import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SlackAuthButton: React.FC = () => {
  const [authUrl, setAuthUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAuthUrl = async () => {
      try {
        setIsLoading(true);
        // In a real application, we would fetch the auth URL from the backend
        // For now, we'll just use the API endpoint directly
        setAuthUrl(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/slack/auth/`);
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
    // Open the Slack authorization page in a new window
    window.open(authUrl, '_blank', 'width=800,height=600');
  };

  if (isLoading) {
    return <div className="text-center">Loading Slack authentication...</div>;
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <button
      onClick={handleAuth}
      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[#4A154B] hover:bg-[#611f69] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4A154B]"
    >
      <svg className="h-5 w-5 mr-2" viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg">
        <path d="M19.712.133a5.381 5.381 0 0 0-5.376 5.387 5.381 5.381 0 0 0 5.376 5.386h5.376V5.52A5.381 5.381 0 0 0 19.712.133m0 14.365H5.376A5.381 5.381 0 0 0 0 19.884a5.381 5.381 0 0 0 5.376 5.387h14.336a5.381 5.381 0 0 0 5.376-5.387 5.381 5.381 0 0 0-5.376-5.386" fill="#36C5F0" />
        <path d="M53.76 19.884a5.381 5.381 0 0 0-5.376-5.386 5.381 5.381 0 0 0-5.376 5.386v5.387h5.376a5.381 5.381 0 0 0 5.376-5.387m-14.336 0V5.52A5.381 5.381 0 0 0 34.048.133a5.381 5.381 0 0 0-5.376 5.387v14.364a5.381 5.381 0 0 0 5.376 5.387 5.381 5.381 0 0 0 5.376-5.387" fill="#2EB67D" />
        <path d="M34.048 54a5.381 5.381 0 0 0 5.376-5.387 5.381 5.381 0 0 0-5.376-5.386h-5.376v5.386A5.381 5.381 0 0 0 34.048 54m0-14.365h14.336a5.381 5.381 0 0 0 5.376-5.386 5.381 5.381 0 0 0-5.376-5.387H34.048a5.381 5.381 0 0 0-5.376 5.387 5.381 5.381 0 0 0 5.376 5.386" fill="#ECB22E" />
        <path d="M0 34.249a5.381 5.381 0 0 0 5.376 5.386 5.381 5.381 0 0 0 5.376-5.386v-5.387H5.376A5.381 5.381 0 0 0 0 34.25m14.336-.001v14.364A5.381 5.381 0 0 0 19.712 54a5.381 5.381 0 0 0 5.376-5.387V34.25a5.381 5.381 0 0 0-5.376-5.387 5.381 5.381 0 0 0-5.376 5.387" fill="#E01E5A" />
      </svg>
      Connect with Slack
    </button>
  );
};

export default SlackAuthButton;
