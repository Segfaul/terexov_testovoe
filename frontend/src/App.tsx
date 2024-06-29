import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './components/Home';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="app">
        <Routes>
          <Route path='/' element={<Home />}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
