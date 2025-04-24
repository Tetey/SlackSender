import React from 'react';
import Layout from '../components/Layout';
import MessageForm from '../components/MessageForm';

const NewMessagePage: React.FC = () => {
  return (
    <Layout>
      <MessageForm />
    </Layout>
  );
};

export default NewMessagePage;
