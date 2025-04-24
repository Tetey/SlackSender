import React, { useState } from 'react';
import { sendSlackMessage } from '../services/slackService';

interface SlackMessageSenderProps {
  onMessageSent?: () => void;
}

const SlackMessageSender: React.FC<SlackMessageSenderProps> = ({ onMessageSent }) => {
  const [channel, setChannel] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!channel || !message) {
      setError('Please provide both channel and message');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      // Format channel name if needed
      const formattedChannel = channel.startsWith('#') || 
                              channel.startsWith('C') || 
                              channel.startsWith('D') || 
                              channel.startsWith('G') ? 
                              channel : `#${channel}`;
      
      const result = await sendSlackMessage(formattedChannel, message);
      
      if (result.success) {
        setSuccess(`Message sent to ${formattedChannel} successfully!`);
        setChannel('');
        setMessage('');
        if (onMessageSent) {
          onMessageSent();
        }
      } else {
        setError(`Failed to send message: ${result.message}`);
      }
    } catch (err) {
      setError('An error occurred while sending the message');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Send Slack Message</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {success}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="channel" className="block text-sm font-medium text-gray-700 mb-1">
            Channel
          </label>
          <input
            type="text"
            id="channel"
            value={channel}
            onChange={(e) => setChannel(e.target.value)}
            placeholder="e.g. #general or general"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
          <p className="mt-1 text-xs text-gray-500">
            For public channels, you can use the name (e.g., "general") or with a # prefix.
            For private channels and DMs, use the channel/user ID.
          </p>
        </div>
        
        <div className="mb-4">
          <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
            Message
          </label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[#4A154B] hover:bg-[#611f69] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4A154B] disabled:opacity-50"
          >
            {isLoading ? 'Sending...' : 'Send Message'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SlackMessageSender;
