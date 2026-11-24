import React, { useState, useEffect } from 'react';
import { getProjects, getProject, getEpisodeScenes, generateSceneImage, generateSceneVideo } from '../api/client';
import { Clapperboard, Sparkles, Video, RefreshCw, CheckCircle } from 'lucide-react';

export default function SceneStudio() {
  const [projects, setProjects] = useState([]);
  const [episodes, setEpisodes] = useState([]);
  const [selectedEpisodeId, setSelectedEpisodeId] = useState(null);
  const [scenes, setScenes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [workingSceneId, setWorkingSceneId] = useState(null);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const pList = await getProjects();
      setProjects(pList);
      if (pList.length > 0) {
        const fullProj = await getProject(pList[0].id);
        setEpisodes(fullProj.episodes);
        if (fullProj.episodes.length > 0) {
          const epId = fullProj.episodes[0].id;
          setSelectedEpisodeId(epId);
          const sc = await getEpisodeScenes(epId);
          setScenes(sc);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSelectEpisode = async (epId) => {
    setSelectedEpisodeId(epId);
    const sc = await getEpisodeScenes(epId);
    setScenes(sc);
  };

  const handleGenImage = async (sceneId) => {
    setWorkingSceneId(sceneId);
    try {
      await generateSceneImage(sceneId);
      const sc = await getEpisodeScenes(selectedEpisodeId);
      setScenes(sc);
    } catch (e) {
      alert('Error generating scene image: ' + e.message);
    } finally {
      setWorkingSceneId(null);
    }
  };

  const handleGenVideo = async (sceneId) => {
    setWorkingSceneId(sceneId);
    try {
      await generateSceneVideo(sceneId);
      const sc = await getEpisodeScenes(selectedEpisodeId);
      setScenes(sc);
    } catch (e) {
      alert('Error generating motion video: ' + e.message);
    } finally {
      setWorkingSceneId(null);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Scene Studio...</div>;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-white">Scene Studio & 3D Render</h2>
          <p className="text-sm text-slate-400">Render 3D scene backgrounds, frame characters, and animate clips with motion camera filters</p>
        </div>

        {/* Episode Selector */}
        <select
          value={selectedEpisodeId || ''}
          onChange={(e) => handleSelectEpisode(Number(e.target.value))}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
        >
          {episodes.map((ep) => (
            <option key={ep.id} value={ep.id}>{ep.title}</option>
          ))}
        </select>
      </div>

      <div className="space-y-6">
        {scenes.map((sc) => (
          <div key={sc.id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <span className="text-xs font-bold text-indigo-400 uppercase tracking-wide">Scene #{sc.scene_number}</span>
                <h3 className="text-base font-bold text-white">{sc.title || `Scene ${sc.scene_number}`}</h3>
              </div>
              <span className="text-xs text-slate-400 bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
                Duration: {sc.duration_seconds}s
              </span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
              {/* Left: Prompts & Script */}
              <div className="lg:col-span-7 space-y-3">
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
                  <span className="text-[11px] font-bold text-slate-400 uppercase block mb-1">Scene Description</span>
                  <p className="text-xs text-slate-200">{sc.description}</p>
                </div>

                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
                  <span className="text-[11px] font-bold text-indigo-400 uppercase block mb-1">3D Visual Prompt</span>
                  <p className="text-xs text-slate-300 font-mono text-[11px]">{sc.visual_prompt}</p>
                </div>

                {/* Dialogues */}
                {sc.dialogues && sc.dialogues.length > 0 && (
                  <div className="space-y-1.5 pt-1">
                    <span className="text-[11px] font-bold text-slate-400 uppercase block">Dialogues</span>
                    {sc.dialogues.map((d) => (
                      <div key={d.id} className="text-xs p-2 rounded bg-slate-950/60 border border-slate-800/50 flex space-x-2">
                        <strong className="text-indigo-400 shrink-0">{d.speaker_name}:</strong>
                        <span className="text-slate-200">"{d.text}"</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Right: Visual Render & Video Preview */}
              <div className="lg:col-span-5 flex flex-col space-y-3">
                <div className="h-52 bg-slate-950 rounded-lg border border-slate-800 overflow-hidden relative flex items-center justify-center">
                  {sc.video_path ? (
                    <video src={sc.video_path} controls className="w-full h-full object-contain" />
                  ) : sc.image_path ? (
                    <img src={sc.image_path} alt="Scene preview" className="w-full h-full object-cover" />
                  ) : (
                    <div className="text-center p-4">
                      <Clapperboard className="w-8 h-8 text-slate-600 mx-auto mb-1" />
                      <span className="text-xs text-slate-500">No render ready yet</span>
                    </div>
                  )}

                  {sc.is_video_approved && (
                    <span className="absolute top-2 right-2 bg-emerald-500/90 text-white text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center">
                      <CheckCircle className="w-3 h-3 mr-0.5" /> Video Ready
                    </span>
                  )}
                </div>

                <div className="flex space-x-2">
                  <button
                    disabled={workingSceneId === sc.id}
                    onClick={() => handleGenImage(sc.id)}
                    className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded text-xs font-bold flex items-center justify-center cursor-pointer"
                  >
                    {workingSceneId === sc.id ? (
                      <RefreshCw className="w-3.5 h-3.5 animate-spin mr-1" />
                    ) : (
                      <Sparkles className="w-3.5 h-3.5 mr-1" />
                    )}
                    {sc.image_path ? 'Regenerate 3D Image' : 'Generate 3D Image'}
                  </button>

                  <button
                    disabled={!sc.image_path || workingSceneId === sc.id}
                    onClick={() => handleGenVideo(sc.id)}
                    className="flex-1 py-2 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white rounded text-xs font-bold flex items-center justify-center cursor-pointer"
                  >
                    <Video className="w-3.5 h-3.5 mr-1" />
                    Generate Video Clip
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
