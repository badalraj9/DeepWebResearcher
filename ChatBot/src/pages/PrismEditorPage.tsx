import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { BackgroundEffects } from '../components/ui/BackgroundEffects';
import { LiquidNav } from '../components/ui/LiquidNav';
import { NeuralThinking } from '../components/NeuralThinking';
import { api } from '../services/api';
import { useToast } from '../components/ui/use-toast';

export const PrismEditorPage: React.FC = () => {
  const { researchId, draftId } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [content, setContent] = useState<string>('');
  const [title, setTitle] = useState('Untitled Transmutation');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'polling' | 'completed' | 'error'>('idle');
  const [progress, setProgress] = useState<string>('Initializing...');

  const editorRef = useRef<HTMLDivElement>(null);

  // Load Content (Research or Draft)
  useEffect(() => {
    let isMounted = true;

    const loadDraft = async () => {
        if (!draftId) return;
        setLoading(true);
        try {
            const draft = await api.getDraftById(draftId);
            if (isMounted) {
                setTitle(draft.title);
                setContent(draft.draft_content);
                if (editorRef.current) {
                    editorRef.current.innerText = draft.draft_content;
                }
                setLoading(false);
            }
        } catch (error) {
            console.error(error);
            toast({ title: "Error", description: "Failed to load draft.", variant: "destructive" });
            setLoading(false);
        }
    };

    const pollResearch = async () => {
        if (!researchId) return;
        setLoading(true);
        setStatus('polling');

        const poll = async () => {
            if (!isMounted) return;
            try {
                const result = await api.getResearchResult(researchId);

                if (result.status === 'completed') {
                    if (isMounted) {
                        setContent(result.content.draft);
                        if (editorRef.current) {
                            editorRef.current.innerText = result.content.draft;
                        }
                        setTitle(result.query.original || 'New Research');
                        setLoading(false);
                        setStatus('completed');
                        toast({ title: "Alchemy Complete", description: "Research has been transmuted." });
                    }
                } else if (result.status === 'error') {
                    if (isMounted) {
                        setLoading(false);
                        setStatus('error');
                        toast({ title: "Alchemy Failed", description: "The transmutation process encountered an error.", variant: "destructive" });
                    }
                } else {
                    // Still processing
                    if (isMounted) {
                         setProgress(`Transmuting... [${result.status}]`);
                         setTimeout(poll, 3000);
                    }
                }
            } catch (error) {
                console.error(error);
                if (isMounted) setTimeout(poll, 5000); // Retry on network error
            }
        };

        poll();
    };

    if (draftId) {
        loadDraft();
    } else if (researchId) {
        pollResearch();
    } else {
        // New blank editor
        setLoading(false);
    }

    return () => { isMounted = false; };
  }, [researchId, draftId, toast]);

  const handleSave = async () => {
      if (!content && !editorRef.current?.innerText) return;

      const textToSave = editorRef.current?.innerText || content;

      try {
          if (researchId) {
              // Save as new draft from research
              const res = await api.saveDraft(researchId, title, [], textToSave);
              toast({ title: "Saved", description: "Artifact saved to Archive." });
              navigate(`/editor/draft/${res.draft_id}`);
          } else if (draftId) {
               // Logic to update draft
              toast({ title: "Notice", description: "Update functionality pending. Content preserved locally." });
          } else {
              toast({ title: "Cannot Save", description: "Start a research session to save results." });
          }
      } catch (error) {
          toast({ title: "Error", description: "Failed to save." });
      }
  };

  const executeCommand = (command: string, value: string = '') => {
      document.execCommand(command, false, value);
      editorRef.current?.focus();
  };

  return (
    <div className="relative min-h-screen w-full flex flex-col font-display antialiased selection:bg-primary/20 selection:text-white bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-100 overflow-hidden">

      <BackgroundEffects />

      {loading && <NeuralThinking />}

      {/* Top Navigation */}
      <header className="relative z-20 w-full flex items-center justify-between px-8 py-6 opacity-80 hover:opacity-100 transition-opacity duration-300">
        <div className="flex items-center gap-4 group cursor-pointer" onClick={() => navigate('/')}>
            <div className="size-8 rounded-full bg-glass-surface backdrop-blur-md border border-glass-border flex items-center justify-center shadow-neon text-primary group-hover:bg-primary group-hover:text-background-dark transition-colors duration-300">
                <span className="material-symbols-outlined text-[20px]">diamond</span>
            </div>
            <div className="flex flex-col">
                <h2 className="text-white text-sm font-semibold tracking-wide">Prism Editor</h2>
                <span className="text-xs text-primary/60 font-medium">
                    {loading ? 'Transmuting...' : (draftId ? 'Archive Artifact' : 'Active Session')}
                </span>
            </div>
        </div>
        <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-6 mr-4 text-xs font-medium text-slate-400">
                {status === 'completed' && <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.6)]"></span> Ready</span>}
                <span className="hover:text-primary cursor-pointer transition-colors" onClick={handleSave}>Save</span>
            </div>
            <button className="size-10 rounded-full bg-glass-surface backdrop-blur-md border border-glass-border flex items-center justify-center text-slate-300 hover:text-white hover:border-primary/50 transition-all duration-300">
                <span className="material-symbols-outlined text-[20px]">settings</span>
            </button>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center w-full px-4 sm:px-8 py-4 overflow-hidden">

        {/* The Glass Slate (Editor) */}
        <div className="relative w-full max-w-4xl h-full max-h-[85vh] flex flex-col group/editor">

            {/* Glass Container Background */}
            <div className="absolute inset-0 bg-glass-surface backdrop-blur-xl rounded-2xl border border-glass-border shadow-neon z-0 transition-all duration-500 group-hover/editor:shadow-[0_0_50px_rgba(6,232,249,0.15)]"></div>

            {/* Toolbar - Floating & Glowing */}
            <div className="relative z-20 mx-auto -mt-6 mb-4 flex items-center gap-2 px-6 py-2 rounded-full glass-panel border border-primary/20 shadow-neon opacity-80 hover:opacity-100 transition-all duration-300">
                <button onClick={() => executeCommand('bold')} className="p-2 hover:text-primary transition-colors" title="Bold">
                    <span className="material-symbols-outlined text-sm">format_bold</span>
                </button>
                <button onClick={() => executeCommand('italic')} className="p-2 hover:text-primary transition-colors" title="Italic">
                    <span className="material-symbols-outlined text-sm">format_italic</span>
                </button>
                <button onClick={() => executeCommand('formatBlock', 'H2')} className="p-2 hover:text-primary transition-colors" title="Heading">
                    <span className="material-symbols-outlined text-sm">title</span>
                </button>
                 <button onClick={() => executeCommand('createLink', prompt('Enter URL:') || '')} className="p-2 hover:text-primary transition-colors" title="Link">
                    <span className="material-symbols-outlined text-sm">link</span>
                </button>
                <div className="w-px h-4 bg-white/20 mx-2"></div>
                 <button onClick={() => executeCommand('undo')} className="p-2 hover:text-primary transition-colors" title="Undo">
                    <span className="material-symbols-outlined text-sm">undo</span>
                </button>
            </div>

            {/* Editor Content Area */}
            <div className="relative z-10 w-full h-full p-8 md:p-16 overflow-y-auto">

                {/* Title Input */}
                <input
                    className="w-full text-4xl md:text-5xl font-bold text-white mb-8 tracking-tight outline-none border-none bg-transparent placeholder-slate-500"
                    placeholder="Untitled Transmutation"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />

                {/* Body Text (Editable Div) */}
                <div
                    ref={editorRef}
                    className="prose prose-invert prose-lg max-w-none text-slate-300 font-light leading-relaxed tracking-wide outline-none min-h-[50vh]"
                    contentEditable
                    suppressContentEditableWarning
                    onInput={(e) => setContent(e.currentTarget.innerText)}
                >
                    {/* Content is injected via ref or logic above */}
                    {!content && !loading && <p className="text-slate-500 italic">Initiate a research session to generate content...</p>}
                </div>
            </div>

        </div>
      </main>

      <footer className="relative z-20 w-full px-8 py-4 flex justify-between items-end pointer-events-none">
        <div className="pointer-events-auto flex items-center gap-3">
             {/* Status Indicators */}
        </div>
      </footer>

      <LiquidNav />
    </div>
  );
};
