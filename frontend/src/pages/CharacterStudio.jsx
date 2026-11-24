import React, { useState, useEffect } from 'react';
import { getProjects, getProject, generateCharacterRef, approveCharacter } from '../api/client';
import { Users, Sparkles, Check, RefreshCw } from 'lucide-react';

export default function CharacterStudio() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generatingId, setGeneratingId] = useState(null);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const p = await getProjects();
      setProjects(p);
      if (p.length > 0) {
        const full = await getProject(p[0].id);
        setSelectedProject(full);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRef = async (charId) => {
    setGeneratingId(charId);
    try {
      await generateCharacterRef(charId);
      const full = await getProject(selectedProject.id);
      setSelectedProject(full);
    } catch (e) {
      alert('Error generating character reference: ' + e.message);
    } finally {
      setGeneratingId(null);
    }
  };

  const handleApprove = async (charId) => {
    await approveCharacter(charId);
    const full = await getProject(selectedProject.id);
    setSelectedProject(full);
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Character Studio...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Character Studio</h2>
          <p className="text-sm text-slate-400">Design consistent 3D cartoon characters, wardrobe locks & voice synthesis profiles</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {selectedProject?.characters?.map((c) => (
          <div key={c.id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col justify-between">
            {/* Visual Thumbnail */}
            <div className="h-48 bg-slate-950 relative flex items-center justify-center overflow-hidden border-b border-slate-800">
              {c.reference_image ? (
                <img src={c.reference_image} alt={c.name} className="w-full h-full object-cover" />
              ) : (
                <div className="text-center p-4">
                  <Users className="w-10 h-10 text-slate-600 mx-auto mb-2" />
                  <span className="text-xs text-slate-500">No reference image generated yet</span>
                </div>
              )}
              {c.is_approved && (
                <span className="absolute top-2 right-2 bg-emerald-500/90 text-white text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center">
                  <Check className="w-3 h-3 mr-0.5" /> Approved Look
                </span>
              )}
            </div>

            {/* Character Info */}
            <div className="p-4 space-y-2 flex-1">
              <div className="flex items-center justify-between">
                <h4 className="text-base font-bold text-white">{c.name}</h4>
                <span className="text-xs text-slate-400">{c.age} yrs</span>
              </div>

              <div className="text-xs text-slate-300">
                <strong>Appearance:</strong> {c.appearance}
              </div>
              <div className="text-xs text-indigo-300">
                <strong>Outfit Lock:</strong> {c.clothing}
              </div>
              <div className="text-xs text-slate-400">
                <strong>Voice:</strong> {c.voice_id} ({c.voice_style})
              </div>
            </div>

            {/* Actions */}
            <div className="p-3 bg-slate-950/60 border-t border-slate-800 flex space-x-2">
              <button
                disabled={generatingId === c.id}
                onClick={() => handleGenerateRef(c.id)}
                className="flex-1 py-1.5 px-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded text-xs font-semibold flex items-center justify-center cursor-pointer"
              >
                {generatingId === c.id ? (
                  <RefreshCw className="w-3 h-3 animate-spin mr-1" />
                ) : (
                  <Sparkles className="w-3 h-3 mr-1" />
                )}
                {c.reference_image ? 'Regenerate' : 'Generate 3D Ref'}
              </button>

              {!c.is_approved && (
                <button
                  onClick={() => handleApprove(c.id)}
                  className="py-1.5 px-3 bg-emerald-600/30 hover:bg-emerald-600 text-emerald-300 hover:text-white border border-emerald-500/40 rounded text-xs font-medium cursor-pointer"
                >
                  Approve
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
