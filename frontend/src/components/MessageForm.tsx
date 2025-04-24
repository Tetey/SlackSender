import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ScheduledMessage } from '../types';
import { messageService } from '../services/api';

interface MessageFormProps {
  initialMessage?: ScheduledMessage;
  isEditing?: boolean;
}

const MessageForm: React.FC<MessageFormProps> = ({ 
  initialMessage,
  isEditing = false
}) => {
  const navigate = useNavigate();
  const [message, setMessage] = useState<string>('');
  const [channel, setChannel] = useState<string>('');
  const [scheduledTime, setScheduledTime] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialMessage) {
      setMessage(initialMessage.message);
      setChannel(initialMessage.channel);
      // Format the date-time for the input
      if (initialMessage.scheduled_time) {
        const date = new Date(initialMessage.scheduled_time);
        setScheduledTime(date.toISOString().slice(0, 16));
      }
    }
  }, [initialMessage]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const messageData: ScheduledMessage = {
        message,
        channel,
        scheduled_time: new Date(scheduledTime).toISOString(),
      };

      if (isEditing && initialMessage?.id) {
        await messageService.updateMessage(initialMessage.id, messageData);
      } else {
        await messageService.createMessage(messageData);
      }

      navigate('/messages');
    } catch (err) {
      console.error('Error saving message:', err);
      setError('Failed to save the message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">
        {isEditing ? 'Edit Scheduled Message' : 'Schedule New Message'}
      </h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="channel" className="block text-sm font-medium text-gray-700">
            Channel
          </label>
          <input
            type="text"
            id="channel"
            value={channel}
            onChange={(e) => setChannel(e.target.value)}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="#general"
          />
        </div>

        <div>
          <label htmlFor="message" className="block text-sm font-medium text-gray-700">
            Message
          </label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
            rows={4}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Your message content..."
          />
        </div>

        <div>
          <label htmlFor="scheduledTime" className="block text-sm font-medium text-gray-700">
            Scheduled Time
          </label>
          <input
            type="datetime-local"
            id="scheduledTime"
            value={scheduledTime}
            onChange={(e) => setScheduledTime(e.target.value)}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={() => navigate('/messages')}
            className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {loading ? 'Saving...' : isEditing ? 'Update Message' : 'Schedule Message'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default MessageForm;
