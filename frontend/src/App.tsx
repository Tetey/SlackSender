import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import pages
import HomePage from './pages/HomePage';
import MessagesPage from './pages/MessagesPage';
import NewMessagePage from './pages/NewMessagePage';
import EditMessagePage from './pages/EditMessagePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/messages" element={<MessagesPage />} />
        <Route path="/new" element={<NewMessagePage />} />
        <Route path="/edit/:id" element={<EditMessagePage />} />
      </Routes>
    </Router>
  );
}

export default App;
