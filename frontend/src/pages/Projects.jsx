import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProjects, getProject } from '../api/client';
import { Film, Users } from 'lucide-react';

export default function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
      if (data.length > 0) {
        const full = await getProject(data[0].id);
        setSelected(full);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = async (id) => {
    const full = await getProject(id);
    setSelected(full);
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading series & episodes...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Cartoon Series & Episodes</h2>
          <p className="text-sm text-slate-400">Manage series continuity, cast, and episode seasons</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Project List */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-slate-300">Your Series</h3>
          {projects.map((p) => (
            <div
              key={p.id}
              onClick={() => handleSelect(p.id)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${
                selected?.id === p.id
                  ? 'bg-slate-900 border-indigo-500 shadow-lg shadow-indigo-500/10'
                  : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
              }`}
            >
              <h4 className="font-bold text-slate-100 text-sm">{p.name}</h4>
              <p className="text-xs text-slate-400 mt-1 line-clamp-2">{p.description}</p>
              <div className="flex items-center space-x-3 text-xs text-indigo-400 mt-3">
                <span className="flex items-center"><Users className="w-3.5 h-3.5 mr-1" /> {p.character_count} Characters</span>
                <span className="flex items-center"><Film className="w-3.5 h-3.5 mr-1" /> {p.episode_count} Episodes</span>
              </div>
            </div>
          ))}
        </div>

        {/* Selected Project Details */}
        {selected && (
          <div className="lg:col-span-2 space-y-5 bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-1">
                <span>{selected.genre}</span>
                <span>•</span>
                <span>{selected.language}</span>
              </div>
              <h3 className="text-2xl font-black text-white">{selected.name}</h3>
              <p className="text-sm text-slate-300 mt-2">{selected.description}</p>
            </div>

            <div className="p-3.5 rounded-lg bg-slate-950/70 border border-slate-800 text-xs space-y-1">
              <div><strong className="text-slate-300">Visual Style:</strong> <span className="text-slate-400">{selected.visual_style}</span></div>
              <div><strong className="text-slate-300">Setting:</strong> <span className="text-slate-400">{selected.setting}</span></div>
              <div><strong className="text-slate-300">Target Duration:</strong> <span className="text-slate-400">{selected.target_duration}</span></div>
            </div>

            {/* Cast preview */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-bold text-slate-200">Main Characters ({selected.characters.length})</h4>
                <button onClick={() => navigate('/characters')} className="text-xs text-indigo-400 hover:underline cursor-pointer">
                  Character Studio →
                </button>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {selected.characters.map((c) => (
                  <div key={c.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                    <div className="font-semibold text-xs text-white">{c.name}</div>
                    <div className="text-[11px] text-slate-400">{c.age} yrs • {c.personality.split(',')[0]}</div>
                    <div className="text-[10px] text-indigo-400 mt-1 truncate">{c.clothing}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Episodes */}
            <div>
              <h4 className="text-sm font-bold text-slate-200 mb-2">Episodes ({selected.episodes.length})</h4>
              <div className="space-y-2">
                {selected.episodes.map((ep) => (
                  <div key={ep.id} className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 flex items-center justify-between">
                    <div>
                      <div className="text-sm font-semibold text-slate-100">{ep.title}</div>
                      <div className="text-xs text-slate-400">{ep.synopsis}</div>
                    </div>
                    <button 
                      onClick={() => navigate('/scenes')}
                      className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-xs font-medium cursor-pointer"
                    >
                      Open Scenes
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
