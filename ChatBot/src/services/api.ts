import { Draft, ResearchResult, Playlist } from '../types';

const API_BASE_URL = 'http://localhost:5000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new ApiError(response.status, errorBody.error || errorBody.message || 'Unknown API error');
  }
  return response.json();
}

export const api = {
  // Research
  async startResearch(query: string, style: number = 2): Promise<{ status: string; research_id: string }> {
    const response = await fetch(`${API_BASE_URL}/research/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, style }),
    });
    return handleResponse(response);
  },

  async getResearchResult(researchId: string): Promise<ResearchResult> {
    const response = await fetch(`${API_BASE_URL}/research/results/${researchId}`);
    return handleResponse(response);
  },

  // Library / Drafts
  async getDrafts(tag?: string): Promise<{ count: number; drafts: Draft[] }> {
    const url = new URL(`${API_BASE_URL}/library/drafts`);
    if (tag) url.searchParams.append('tag', tag);
    const response = await fetch(url.toString());
    return handleResponse(response);
  },

  async getDraftById(draftId: string): Promise<Draft> {
    const response = await fetch(`${API_BASE_URL}/library/drafts/${draftId}`);
    return handleResponse(response);
  },

  async saveDraft(researchId: string, title: string, tags: string[] = [], content?: string): Promise<{ status: string; draft_id: string }> {
    const response = await fetch(`${API_BASE_URL}/library/save-draft`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ research_id: researchId, title, tags, content }),
    });
    return handleResponse(response);
  },

  async updateDraft(draftId: string, title?: string, tags?: string[], content?: string): Promise<{ status: string; draft: Draft }> {
    // Note: The backend update_draft endpoint (PUT /library/drafts/<id>) currently only accepts title and tags.
    // If we want to update content, we might need to modify the backend or use save_copy.
    // Checking backend code: updates.append("title = ?"), updates.append("tags = ?").
    // It does NOT update content.
    // So for now, we can only update metadata.
    // To update content, we should likely create a new version or fix backend.
    // I will assume for now we only update title/tags.
    const response = await fetch(`${API_BASE_URL}/library/drafts/${draftId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, tags }),
    });
    return handleResponse(response);
  },

  async deleteDraft(draftId: string): Promise<{ status: string }> {
      const response = await fetch(`${API_BASE_URL}/library/drafts/${draftId}`, {
          method: 'DELETE'
      });
      return handleResponse(response);
  },

  // Playlists
  async getPlaylists(): Promise<{ count: number; playlists: Playlist[] }> {
      const response = await fetch(`${API_BASE_URL}/library/playlists`);
      return handleResponse(response);
  }
};

// Export standalone function for compatibility with existing code (useResearch.ts)
export const startResearch = api.startResearch;
