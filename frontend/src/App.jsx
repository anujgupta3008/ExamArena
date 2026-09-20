import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import Navbar from './components/Shared/Navbar';
import LandingNavbar from './components/Shared/LandingNavbar';
import ProtectedRoute from './components/Shared/ProtectedRoute';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';
import MockExam from './pages/MockExam';
import PrivacyPolicy from './pages/PrivacyPolicy';

export default function App() {
  const location = useLocation();

  return (
    <div className="min-h-screen flex flex-col text-slate-100 font-body relative overflow-x-hidden bg-[#0a0b10]">
      <Toaster position="top-right" toastOptions={{
        className: '!bg-slate-800 !text-slate-100 !border !border-slate-700 !shadow-xl',
      }} />
      {['/', '/privacy'].includes(location.pathname) ? <LandingNavbar /> : <Navbar />}
      
      <main className="flex-grow pb-20">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/mock-exam" element={<MockExam />} />
          
          <Route path="/exam/:id" element={<Dashboard />} />
          
          {/* Protected Routes */}
          <Route element={<ProtectedRoute adminOnly={true} />}>
            <Route path="/internal-admin" element={<Admin />} />
          </Route>
          
          <Route path="/privacy" element={<PrivacyPolicy />} />
        </Routes>
      </main>
      
      <footer className="relative z-10 border-t border-white/5 py-6 mt-auto text-center text-slate-500 text-sm">
        <div className="flex items-center justify-center gap-4">
          <span>&copy; {new Date().getFullYear()} Exam Arena</span>
          <a href="/privacy" className="hover:text-indigo-400 transition-colors">Privacy Policy</a>
        </div>
      </footer>

    </div>
  );
}
