import React, { useState, useEffect } from 'react';
import { getProjects, getProject, getEpisodeScenes, getAvailableVoices, generateVoice } from '../api/client';
import { Mic2, Play, Volume2, Sparkles, RefreshCw, UserCheck } from 'lucide-react';

export default function VoiceStudio() {
  const [scenes, setScenes] = useState([]);
  const [voices, setVoices] = useState([]);
  const [selectedVoiceMap, setSelectedVoiceMap] = useState({});
  const [loading, setLoading] = useState(true);
  const [generatingDiagId, setGeneratingDiagId] = useState(null);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const v = await getAvailableVoices();
      setVoices(v);
      const p = await getProjects();
      if (p.length > 0) {
        const full = await getProject(p[0].id);
        if (full.episodes.length > 0) {
          const sc = await getEpisodeScenes(full.episodes[0].id);
          setScenes(sc);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceChange = (diagId, voiceId) => {
    setSelectedVoiceMap((prev) => ({ ...prev, [diagId]: voiceId }));
  };

  const handleGenerateVoice = async (diagId) => {
    setGeneratingDiagId(diagId);
    try {
      const chosenVoice = selectedVoiceMap[diagId];
      await generateVoice(diagId, chosenVoice, 1.0);
      const p = await getProjects();
      const full = await getProject(p[0].id);
      const sc = await getEpisodeScenes(full.episodes[0].id);
      setScenes(sc);
    } catch (e) {
      alert('Voice generation failed: ' + e.message);
    } finally {
      setGeneratingDiagId(null);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Voice Studio...</div>;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-white">Voice & Audio Studio</h2>
          <p className="text-sm text-slate-400">Realistic gender-accurate vocal mastering with distinct acoustic profiles for each character</p>
        </div>
      </div>

      {/* Voice Profiles Roster */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 bg-slate-900/60 border border-slate-800 rounded-xl p-4">
        {voices.slice(0, 4).map((v) => (
          <div key={v.id} className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white">{v.name.split(' (')[0]}</span>
              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                v.gender === 'Male' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' : 'bg-pink-500/20 text-pink-300 border border-pink-500/30'
              }`}>
                {v.gender}
              </span>
            </div>
            <div className="text-[11px] text-slate-400 mt-1">{v.name.split(' - ')[1]?.replace(')', '') || v.gender}</div>
          </div>
        ))}
      </div>

      <div className="space-y-4">
        {scenes.map((sc) => (
          <div key={sc.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-indigo-400">Scene #{sc.scene_number}: {sc.title}</h3>

            <div className="space-y-3">
              {sc.dialogues?.map((d) => (
                <div key={d.id} className="p-3.5 bg-slate-950 rounded-lg border border-slate-800 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  <div className="space-y-1.5 flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-indigo-300">{d.speaker_name}</span>
                      <span className="text-[10px] text-slate-500">Dialogue #{d.order}</span>
                    </div>
                    <p className="text-xs text-slate-200 font-medium">"{d.text}"</p>
                  </div>

                  <div className="flex flex-wrap items-center gap-3 shrink-0">
                    {/* Voice selector */}
                    <select
                      value={selectedVoiceMap[d.id] || ''}
                      onChange={(e) => handleVoiceChange(d.id, e.target.value)}
                      className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                    >
                      <option value="">Auto: {d.speaker_name} profile</option>
                      {voices.map((v) => (
                        <option key={v.id} value={v.id}>
                          {v.gender === 'Male' ? '♂' : '♀'} {v.name}
                        </option>
                      ))}
                    </select>

                    {d.audio_path ? (
                      <audio controls src={d.audio_path} className="h-8 max-w-[210px]" />
                    ) : null}

                    <button
                      disabled={generatingDiagId === d.id}
                      onClick={() => handleGenerateVoice(d.id)}
                      className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded text-xs font-bold flex items-center cursor-pointer shadow-sm"
                    >
                      {generatingDiagId === d.id ? (
                        <RefreshCw className="w-3.5 h-3.5 animate-spin mr-1.5" />
                      ) : (
                        <Mic2 className="w-3.5 h-3.5 mr-1.5" />
                      )}
                      {d.audio_path ? 'Regenerate Voice' : 'Generate Voice'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
