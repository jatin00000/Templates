// eslint-disable-next-line
import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Analyzer from './components/Analyzer'
import Login from './components/Login'
import { AuthProvider } from './context/AuthContext'
export default function App() {

  
  return (
    <Router>

      <AuthProvider>
        <Routes>
          <Route path='/' element={<Analyzer/>}/>
          <Route path="/login" element={<Login />} />
        </Routes>
      </AuthProvider>
    </Router>

  );
}