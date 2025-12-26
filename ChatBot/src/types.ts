export interface LibraryItem {
  id: string;
  title: string;
  category: string;
  content: string;
  timestamp: number;
  references?: string[];
  researchId?: string;
}

export interface ResearchResult {
  research_id: string;
  status: 'queued' | 'processing' | 'completed' | 'error';
  created_at: string;
  query: {
    original: string;
    optimized: string;
  };
  research_output: string;
  content: {
    style: string;
    draft: string;
  };
  references: string[];
}

export interface Draft {
    draft_id: string;
    title: string;
    tags: string[];
    created_at: string;
    updated_at: string;
    research_id?: string;
    query?: string;
    content_style?: string;
    draft_content: string;
    reference_list?: string[]; // Backend returns 'reference_list' in some endpoints, or 'references' in others. We need to be careful.
    references?: string[];
}

export interface Playlist {
    playlist_id: string;
    name: string;
    description: string;
    draft_count: number;
    created_at: string;
}
