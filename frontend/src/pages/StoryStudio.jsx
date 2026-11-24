import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProjects, generateStory } from '../api/client';
import { Sparkles, Wand2, BookOpen } from 'lucide-react';

export default function StoryStudio() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [idea, setIdea] = useState('Four friends explore an ancient Indian temple courtyard where statues whisper warnings in the moonlight.');
  const [genre, setGenre] = useState('Horror + Mystery + Comedy');
  const [language, setLanguage] = useState('Hinglish');
  const [duration, setDuration] = useState('2–5 minutes');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    getProjects().then((data) => {
      setProjects(data);
      if (data.length > 0) setSelectedProjectId(data[0].id);
    });
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!selectedProjectId) return;
    setGenerating(true);
    setResult(null);

    try {
      const res = await generateStory({
        project_id: selectedProjectId,
        idea,
        genre,
        language,
        duration
      });
      setResult(res);
    } catch (err) {
      alert('Story generation failed: ' + err.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Story & Script Generator</h2>
        <p className="text-sm text-slate-400">Generate full episodes, scene breakdowns, dialogues, and 3D visual prompts</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <form onSubmit={handleGenerate} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Target Project Series</label>
            <select
              value={selectedProjectId || ''}
              onChange={(e) => setSelectedProjectId(Number(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
            >
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Story Idea & Premise</label>
            <textarea
              rows={4}
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              placeholder="Describe the adventure, mystery or conflict..."
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Genre</label>
              <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-2 text-xs text-white"
              >
                <option>Horror + Mystery + Comedy</option>
                <option>Mystery</option>
                <option>Comedy</option>
                <option>Adventure</option>
                <option>Fantasy</option>
                <option>Educational</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-2 text-xs text-white"
              >
                <option>Hinglish</option>
                <option>Hindi</option>
                <option>English</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Target Duration</label>
            <select
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-2 text-xs text-white"
            >
              <option>1–2 minutes</option>
              <option>2–5 minutes</option>
              <option>5–10 minutes</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={generating}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-lg text-xs font-bold shadow-md shadow-indigo-600/20 flex items-center justify-center cursor-pointer"
          >
            {generating ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin mr-2" />
                Drafting 3D Episode Script with Gemini...
              </>
            ) : (
              <>
                <Wand2 className="w-4 h-4 mr-2" />
                Generate Script & Scenes
              </>
            )}
          </button>
        </form>

        {/* Output */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
          {result ? (
            <div className="space-y-4">
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
                <h4 className="text-base font-bold text-emerald-300">Generated Episode: "{result.title}"</h4>
                <p className="text-xs text-slate-300 mt-1">Generated {result.scenes_count} scene visual prompts & dialogues ready for rendering.</p>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={() => navigate('/scenes')}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold cursor-pointer"
                >
                  Proceed to Scene Studio →
                </button>
              </div>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center text-slate-500">
              <BookOpen className="w-12 h-12 text-slate-700 mb-3" />
              <p className="text-xs">Fill out the prompt details and generate an automated episodic script.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
