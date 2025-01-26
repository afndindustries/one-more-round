import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Header from './components/Header';
import NotFoundPage from './components/NotFoundPage';
import EventsPage from '../events/EventsPage';

const App = () => {
    return (
        <div style={{ backgroundColor: '#f8f9fa' }}>
            <Router>
                <Header />

                <Routes>
                    <Route path="/" element={<EventsPage />} />
                    <Route path="*" element={<NotFoundPage />} />
                </Routes>
            </Router>
        </div>
    );
};

export default App;