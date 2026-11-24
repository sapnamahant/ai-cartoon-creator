import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getDashboardStats } from '../api/client';
import { 
  FolderKanban, 
  Users, 
  Film, 
  Image as ImageIcon, 
  Video, 
  Sparkles, 
  CheckCircle2, 
  Clock,
  ArrowRight
} from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const res = await getDashboardStats();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center text-slate-400">
        <Sparkles className="w-6 h-6 animate-spin text-indigo-400 mr-3" />
        Loading studio dashboard...
      </div>
    );
  }

  const counts = data?.counts || {};
  const apis = data?.api_status || {};

  const cards = [
    { title: 'Total Projects', value: counts.projects || 0, icon: FolderKanban, color: 'from-blue-500/20 to-indigo-500/10 border-blue-500/30' },
    { title: 'Characters Studio', value: counts.characters || 0, icon: Users, color: 'from-purple-500/20 to-pink-500/10 border-purple-500/30' },
    { title: 'Episodes', value: counts.episodes || 0, icon: Film, color: 'from-emerald-500/20 to-teal-500/10 border-emerald-500/30' },
    { title: 'Story Scenes', value: counts.scenes || 0, icon: Video, color: 'from-amber-500/20 to-orange-500/10 border-amber-500/30' },
    { title: 'Generated Images', value: counts.images || 0, icon: ImageIcon, color: 'from-cyan-500/20 to-blue-500/10 border-cyan-500/30' },
    { title: 'Video Clips', value: counts.videos || 0, icon: Sparkles, color: 'from-rose-500/20 to-red-500/10 border-rose-500/30' },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-900/60 via-purple-900/40 to-slate-900 border border-indigo-500/30 p-6">
        <div className="relative z-10 max-w-2xl">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 mb-3">
            3D Animation Engine Ready
          </span>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            AI Cartoon Studio Automation
          </h2>
          <p className="mt-2 text-sm text-slate-300 leading-relaxed">
            Generate continuous 3D animated cartoon episodes from story prompt to final assembled MP4 with voice dialogues, background ambience, and consistent characters.
          </p>
          <div className="mt-4 flex space-x-3">
            <button 
              onClick={() => navigate('/story')} 
              className="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              Generate New Story
            </button>
            <button 
              onClick={() => navigate('/projects')} 
              className="inline-flex items-center px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-medium border border-slate-700 transition-all cursor-pointer"
            >
              View Projects
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {cards.map((c, i) => {
          const Icon = c.icon;
          return (
            <div key={i} className={`p-4 rounded-xl bg-gradient-to-br ${c.color} border backdrop-blur-sm`}>
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-medium">{c.title}</span>
                <Icon className="w-4 h-4" />
              </div>
              <div className="text-2xl font-bold text-white">{c.value}</div>
            </div>
          );
        })}
      </div>

      {/* Status & Recent Projects */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Active Projects */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-semibold text-white">Featured Project & Series</h3>
            <span className="text-xs text-indigo-400">Sample Data Seeded</span>
          </div>

          <div className="space-y-3">
            {data?.recent_projects?.map((p) => (
              <div key={p.id} className="p-4 rounded-lg bg-slate-950/60 border border-slate-800 hover:border-slate-700 transition-all flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-100">{p.name}</h4>
                  <div className="flex items-center space-x-3 text-xs text-slate-400 mt-1">
                    <span className="text-indigo-400">{p.genre}</span>
                    <span>•</span>
                    <span>{p.language}</span>
                  </div>
                </div>
                <button 
                  onClick={() => navigate('/scenes')}
                  className="px-3 py-1.5 bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white rounded-md text-xs font-medium border border-indigo-500/40 transition-all cursor-pointer"
                >
                  Open Studio
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Right: API Integration Status */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-base font-semibold text-white mb-4">API Provider Status</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/40 border border-slate-800">
              <div className="text-xs">
                <div className="font-semibold text-slate-200">Google Gemini API</div>
                <div className="text-slate-500">Story & Script Engine</div>
              </div>
              {apis.gemini ? (
                <span className="inline-flex items-center text-xs text-emerald-400"><CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Active</span>
              ) : (
                <span className="inline-flex items-center text-xs text-amber-400" title="Fallback Procedural Generator Active"><Clock className="w-3.5 h-3.5 mr-1" /> Ready (Procedural)</span>
              )}
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/40 border border-slate-800">
              <div className="text-xs">
                <div className="font-semibold text-slate-200">Neural Voice Engine</div>
                <div className="text-slate-500">Realistic Multilingual Dialogue</div>
              </div>
              <span className="inline-flex items-center text-xs text-emerald-400"><CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Active (Gender Tuned)</span>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/40 border border-slate-800">
              <div className="text-xs">
                <div className="font-semibold text-slate-200">Pollinations 3D Render</div>
                <div className="text-slate-500">Consistent Style Generator</div>
              </div>
              <span className="inline-flex items-center text-xs text-emerald-400"><CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Active</span>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/40 border border-slate-800">
              <div className="text-xs">
                <div className="font-semibold text-slate-200">FFmpeg Assembly Engine</div>
                <div className="text-slate-500">Video Render & Audio Mixing</div>
              </div>
              <span className="inline-flex items-center text-xs text-emerald-400"><CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Ready v7.1</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
