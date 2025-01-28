import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Header from './components/Header';
import NotFoundPage from './components/NotFoundPage';
import EventsPage from '../events/EventsPage';
import LoginPage from '../login/LoginPage';
import FullPage from './components/FullPage';

const App = () => {
    return (
        <div style={{ backgroundColor: '#f8f9fa' }}>
            <Router>
                <Routes>
                    <Route element={<FullPage />}>
                        <Route path="/" element={<EventsPage />} />
                        <Route path="*" element={<NotFoundPage />} />
                    </Route>
                    <Route path='/login' element={<LoginPage />} />
                </Routes>
            </Router>
        </div>
    );
};

export default App;