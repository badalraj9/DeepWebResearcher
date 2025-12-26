import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BackgroundEffects } from '../components/ui/BackgroundEffects';
import { LiquidNav } from '../components/ui/LiquidNav';
import { api } from '../services/api';
import { Draft } from '../types';

export const GlassLibraryPage: React.FC = () => {
  const navigate = useNavigate();
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDrafts = async () => {
      try {
        const response = await api.getDrafts();
        setDrafts(response.drafts);
      } catch (error) {
        console.error("Failed to fetch drafts", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDrafts();
  }, []);

  const formatDate = (dateString: string) => {
    try {
        const date = new Date(dateString);
        return new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
            Math.ceil((date.getTime() - Date.now()) / (1000 * 60 * 60 * 24)), 'day'
        );
    } catch (e) {
        return 'Unknown';
    }
  };

  return (
    <div className="relative min-h-screen w-full flex flex-col font-display antialiased selection:bg-primary/20 selection:text-white bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-100 overflow-hidden">

      <BackgroundEffects />

      <div className="relative z-10 flex h-full w-full flex-1">

        {/* Sidebar (simplified for now) */}
        <aside className="hidden xl:flex w-80 flex-col border-r border-glass-border bg-glass-surface/30 backdrop-blur-md relative z-20 h-screen">
             <div className="p-6 border-b border-glass-border">
                <div className="flex items-center gap-3">
                    <div className="size-8 rounded-lg bg-gradient-to-br from-primary/20 to-blue-600/20 border border-primary/30 flex items-center justify-center text-primary shadow-[0_0_15px_rgba(6,232,249,0.3)]">
                        <span className="material-symbols-outlined text-[20px]">diamond</span>
                    </div>
                    <h1 className="font-bold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Alchemy</h1>
                </div>
            </div>
             <div className="p-4">
                <button
                    onClick={() => navigate('/')}
                    className="w-full py-2 px-4 rounded-lg bg-glass-surface border border-glass-border hover:bg-primary/10 hover:border-primary/50 text-slate-300 hover:text-white transition-all flex items-center justify-center gap-2 text-sm">
                    <span className="material-symbols-outlined text-[18px]">add</span>
                    New Analysis
                </button>
            </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 flex flex-col h-screen overflow-hidden relative">

            <header className="w-full h-20 px-8 flex items-center justify-between z-20 border-b border-glass-border bg-background-dark/30 backdrop-blur-sm">
                <h2 className="text-2xl font-light text-white tracking-wide">Transmutation Archive</h2>
            </header>

            <div className="flex-1 overflow-y-auto p-8 relative scroll-smooth pb-24">
                <div className="max-w-7xl mx-auto">

                    {/* Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                        {loading ? (
                            <div className="col-span-full text-center text-slate-500 animate-pulse">Scanning Archive...</div>
                        ) : drafts.length === 0 ? (
                            <div className="col-span-full text-center text-slate-500">The Void is empty. Create a new transmutation.</div>
                        ) : (
                            drafts.map((draft) => (
                                <div
                                    key={draft.draft_id}
                                    onClick={() => navigate(`/editor/draft/${draft.draft_id}`)}
                                    className="glass-card bg-card-surface border border-glass-border rounded-2xl p-6 relative group overflow-hidden flex flex-col h-72 cursor-pointer hover:border-primary/30 transition-all"
                                >
                                    <div className="absolute -right-10 -top-10 w-32 h-32 bg-primary/10 blur-[50px] rounded-full group-hover:bg-primary/20 transition-all duration-500"></div>
                                    <div className="flex justify-between items-start mb-4 relative z-10">
                                        <div className="p-2 rounded-lg bg-[#1a1810] border border-white/10 text-primary">
                                            <span className="material-symbols-outlined text-[24px]">description</span>
                                        </div>
                                    </div>
                                    <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-primary transition-colors line-clamp-2">{draft.title}</h3>
                                    <p className="text-sm text-slate-400 leading-relaxed line-clamp-3 mb-auto">
                                        {draft.query || "No description available."}
                                    </p>
                                    <div className="pt-4 mt-4 border-t border-white/5 flex items-center justify-between text-xs text-slate-500">
                                        <div className="flex items-center gap-2">
                                            <span className="material-symbols-outlined text-[14px]">calendar_today</span>
                                            <span>{formatDate(draft.created_at)}</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}

                    </div>
                </div>
            </div>

        </main>

        <LiquidNav />
      </div>
    </div>
  );
};
