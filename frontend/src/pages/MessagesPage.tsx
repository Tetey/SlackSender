import React from 'react';
import Layout from '../components/Layout';
import MessageList from '../components/MessageList';

const MessagesPage: React.FC = () => {
  return (
    <Layout>
      <MessageList />
    </Layout>
  );
};

export default MessagesPage;
