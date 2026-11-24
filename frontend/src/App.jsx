import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import StoryStudio from './pages/StoryStudio';
import CharacterStudio from './pages/CharacterStudio';
import SceneStudio from './pages/SceneStudio';
import VoiceStudio from './pages/VoiceStudio';
import VideoAssembly from './pages/VideoAssembly';

export default function App() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/story" element={<StoryStudio />} />
            <Route path="/characters" element={<CharacterStudio />} />
            <Route path="/scenes" element={<SceneStudio />} />
            <Route path="/voice" element={<VoiceStudio />} />
            <Route path="/assembly" element={<VideoAssembly />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}
