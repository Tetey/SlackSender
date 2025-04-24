import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface SlackMessageRequest {
  channel: string;
  message: string;
  scheduledTime?: string; // ISO string for scheduled messages
}

export interface SlackMessageResponse {
  success: boolean;
  message: string;
}

/**
 * Send a message to a Slack channel immediately
 */
export const sendSlackMessage = async (
  channel: string,
  message: string
): Promise<SlackMessageResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/messages/send_slack_message/`, {
      channel,
      message,
    });
    
    return {
      success: true,
      message: 'Message sent successfully',
    };
  } catch (error) {
    console.error('Error sending Slack message:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'Failed to send message',
    };
  }
};

/**
 * Get a list of available Slack channels
 * Note: This would require additional backend implementation
 */
export const getSlackChannels = async (): Promise<string[]> => {
  try {
    // This would need to be implemented in the backend
    const response = await axios.get(`${API_BASE_URL}/api/slack/channels/`);
    return response.data.channels || [];
  } catch (error) {
    console.error('Error fetching Slack channels:', error);
    return [];
  }
};

/**
 * Check if the Slack integration is properly configured
 */
export const checkSlackConnection = async (): Promise<boolean> => {
  try {
    // This would need to be implemented in the backend
    const response = await axios.get(`${API_BASE_URL}/api/slack/status/`);
    return response.data.connected || false;
  } catch (error) {
    console.error('Error checking Slack connection:', error);
    return false;
  }
};
