import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import NotFoundPage from './components/NotFoundPage';
import EventsPage from '../events/EventsPage';
import LoginPage from '../login/LoginPage';
import FullPage from './components/FullPage';
import UserPage from '../user/UserPage';
import DrinksPage from '../drinks/DrinksPage';

const App = () => {
    return (
            <Router>
                <Routes>
                    <Route element={<FullPage />}>
                        <Route path="/" element={<EventsPage />} />
                        <Route path="/profile" element={<UserPage />} />
                        <Route path="/drinks" element={<DrinksPage />} />
                        <Route path="*" element={<NotFoundPage />} />
                    </Route>
                    <Route path='/login' element={<LoginPage />} />
                </Routes>
            </Router>
    );
};

export default App;