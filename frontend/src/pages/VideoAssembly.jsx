import React, { useState, useEffect } from 'react';
import { getProjects, getProject, getEpisodeScenes, exportEpisode } from '../api/client';
import { Film, Play, Download, Sparkles, CheckCircle2, Layers } from 'lucide-react';

export default function VideoAssembly() {
  const [project, setProject] = useState(null);
  const [episode, setEpisode] = useState(null);
  const [scenes, setScenes] = useState([]);
  const [exporting, setExporting] = useState(false);
  const [finalVideoUrl, setFinalVideoUrl] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const p = await getProjects();
      if (p.length > 0) {
        const full = await getProject(p[0].id);
        setProject(full);
        if (full.episodes.length > 0) {
          setEpisode(full.episodes[0]);
          setFinalVideoUrl(full.episodes[0].video_export_path);
          const sc = await getEpisodeScenes(full.episodes[0].id);
          setScenes(sc);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!episode) return;
    setExporting(true);
    try {
      const res = await exportEpisode(episode.id);
      setFinalVideoUrl(res.export_url);
    } catch (e) {
      alert('Video export failed: ' + e.message);
    } finally {
      setExporting(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Video Assembly Timeline...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Video Assembly & Timeline Editor</h2>
          <p className="text-sm text-slate-400">Automatic FFmpeg video stitching, character voice dub sync & MP4 episode export</p>
        </div>

        <button
          disabled={exporting}
          onClick={handleExport}
          className="px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 text-white rounded-lg text-xs font-bold shadow-lg shadow-indigo-600/30 flex items-center cursor-pointer"
        >
          {exporting ? (
            <>
              <Sparkles className="w-4 h-4 animate-spin mr-2" />
              Assembling Video with FFmpeg...
            </>
          ) : (
            <>
              <Film className="w-4 h-4 mr-2" />
              Export Full Episode (MP4)
            </>
          )}
        </button>
      </div>

      {/* Final Render Player */}
      {finalVideoUrl && (
        <div className="bg-slate-900 border border-emerald-500/40 rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-400 flex items-center">
              <CheckCircle2 className="w-4 h-4 mr-1.5" /> Episode Exported Successfully
            </span>
            <a
              href={finalVideoUrl}
              download
              className="inline-flex items-center text-xs font-bold text-indigo-400 hover:text-white"
            >
              <Download className="w-3.5 h-3.5 mr-1" /> Download MP4
            </a>
          </div>
          <div className="aspect-video max-h-96 rounded-lg overflow-hidden bg-black flex items-center justify-center">
            <video src={finalVideoUrl} controls className="w-full h-full object-contain" />
          </div>
        </div>
      )}

      {/* Timeline Scenes */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-200">Episode Scene Sequence</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {scenes.map((sc, i) => (
            <div key={sc.id} className="bg-slate-950 border border-slate-800 rounded-lg p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-indigo-400">Clip {i + 1}</span>
                <span className="text-slate-400">{sc.duration_seconds}s</span>
              </div>

              <div className="h-28 bg-slate-900 rounded border border-slate-800/80 overflow-hidden flex items-center justify-center">
                {sc.video_path ? (
                  <video src={sc.video_path} className="w-full h-full object-cover" />
                ) : sc.image_path ? (
                  <img src={sc.image_path} alt="Scene" className="w-full h-full object-cover" />
                ) : (
                  <span className="text-[11px] text-slate-500">Pending image</span>
                )}
              </div>

              <div className="text-[11px] text-slate-300 truncate font-medium">
                {sc.title}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
