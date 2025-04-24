import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import MessageForm from '../components/MessageForm';
import { ScheduledMessage } from '../types';
import { messageService } from '../services/api';

const EditMessagePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [message, setMessage] = useState<ScheduledMessage | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMessage = async () => {
      if (!id) {
        navigate('/messages');
        return;
      }

      try {
        setLoading(true);
        const data = await messageService.getMessage(parseInt(id, 10));
        setMessage(data);
      } catch (err) {
        console.error('Error fetching message:', err);
        setError('Failed to load message. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchMessage();
  }, [id, navigate]);

  if (loading) {
    return (
      <Layout>
        <div className="text-center py-6">Loading message...</div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
          <button 
            onClick={() => navigate('/messages')}
            className="ml-4 text-sm underline"
          >
            Go Back to Messages
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {message ? (
        <MessageForm initialMessage={message} isEditing={true} />
      ) : (
        <div className="text-center py-6">
          <p className="text-gray-500 mb-4">Message not found.</p>
          <button
            onClick={() => navigate('/messages')}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Go Back to Messages
          </button>
        </div>
      )}
    </Layout>
  );
};

export default EditMessagePage;
