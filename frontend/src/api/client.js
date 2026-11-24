import axios from 'axios';

const api = axios.create({
  baseURL: '',
  timeout: 60000,
});

export const getDashboardStats = () => api.get('/api/dashboard/stats').then(r => r.data);
export const getProjects = () => api.get('/api/projects').then(r => r.data);
export const getProject = (id) => api.get(`/api/projects/${id}`).then(r => r.data);
export const createProject = (data) => api.post('/api/projects', data).then(r => r.data);

export const createCharacter = (data) => api.post('/api/characters', data).then(r => r.data);
export const generateCharacterRef = (character_id) => api.post('/api/characters/generate-ref', { character_id }).then(r => r.data);
export const approveCharacter = (character_id) => api.post(`/api/characters/${character_id}/approve`).then(r => r.data);

export const generateStory = (data) => api.post('/api/stories/generate', data).then(r => r.data);

export const getEpisodeScenes = (episode_id) => api.get(`/api/scenes/episode/${episode_id}`).then(r => r.data);
export const generateSceneImage = (scene_id, custom_prompt) => api.post('/api/scenes/generate-image', { scene_id, custom_prompt }).then(r => r.data);
export const generateSceneVideo = (scene_id, animation_prompt) => api.post('/api/scenes/generate-video', { scene_id, animation_prompt }).then(r => r.data);

export const getAvailableVoices = () => api.get('/api/voice/available-voices').then(r => r.data);
export const generateVoice = (dialogue_id, voice_id, speed) => api.post('/api/voice/generate', { dialogue_id, voice_id, speed }).then(r => r.data);

export const exportEpisode = (episode_id) => api.post('/api/assembly/export', { episode_id }).then(r => r.data);

export default api;
