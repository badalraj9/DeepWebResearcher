import React, { useState, useEffect } from 'react';

interface CinematicIntroProps {
  onComplete: () => void;
}

export const CinematicIntro: React.FC<CinematicIntroProps> = ({ onComplete }) => {
  const [ignited, setIgnited] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    // Reveal the menu options after a slight delay
    const timer = setTimeout(() => {
      setShowMenu(true);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  const handleIgnite = () => {
    setIgnited(true);
    // Wait for the "explosion" animation to finish before calling onComplete
    setTimeout(() => {
      setFadeOut(true);
      setTimeout(() => {
        onComplete();
      }, 1000); // Allow fade out
    }, 800);
  };

  if (fadeOut) {
    return (
      <div className="fixed inset-0 z-[100] bg-white animate-[fadeOut_1s_ease-out_forwards] pointer-events-none flex items-center justify-center">
        <style>{`
          @keyframes fadeOut {
            0% { opacity: 1; transform: scale(1); filter: brightness(1); }
            50% { opacity: 1; transform: scale(1.1); filter: brightness(10); }
            100% { opacity: 0; transform: scale(1.5); filter: brightness(20); }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-[100] bg-background-dark text-slate-100 overflow-hidden flex flex-col items-center justify-center font-display antialiased selection:bg-primary/30 selection:text-white">
      {/* Intro Background */}
      <div className="fixed inset-0 z-0 bg-void-gradient pointer-events-none">
        <div className="absolute inset-0 noise-overlay mix-blend-overlay opacity-40"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/20 rounded-full blur-[80px] opacity-40 animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-secondary/10 rounded-full blur-[100px] opacity-30"></div>
      </div>

      <div className={`relative z-10 flex flex-col h-full w-full items-center justify-center p-6 transition-all duration-1000 ${ignited ? 'scale-150 opacity-0 blur-xl' : ''}`}>

        {/* Header (Minimal) */}
        <header className="absolute top-0 left-0 w-full p-8 flex justify-between items-center opacity-80">
          <div className="flex items-center gap-3">
            <div className="size-10 rounded-xl bg-gradient-to-br from-primary/20 to-blue-900/40 border border-primary/40 flex items-center justify-center text-primary shadow-neon">
              <span className="material-symbols-outlined text-[24px]">diamond</span>
            </div>
            <div className="flex flex-col">
              <h1 className="font-bold text-lg tracking-widest uppercase bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-500">Digital Alchemy</h1>
              <span className="text-[10px] text-primary/60 tracking-[0.2em] font-mono">GENESIS V4.0</span>
            </div>
          </div>
        </header>

        <main className="w-full max-w-4xl relative flex flex-col items-center">
          <div className="text-center mb-12 space-y-4 relative">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-glass-border bg-glass-surface backdrop-blur-sm mb-4">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span className="text-xs font-mono text-primary tracking-wider">SYSTEM INITIALIZED</span>
            </div>

            <h2 className="text-5xl md:text-7xl font-extralight text-white tracking-tight leading-tight">
              Create from the <span className="font-normal bg-clip-text text-transparent bg-gradient-to-r from-primary via-white to-secondary">Void</span>
            </h2>
            <p className="text-slate-400 max-w-lg mx-auto text-lg font-light leading-relaxed">
              The spark has ignited. Transmute your raw data into golden knowledge. Begin by defining the parameters of your new universe.
            </p>
          </div>

          {/* Ignition Bar */}
          <div className="w-full relative group z-20 max-w-xl">
            <div className="absolute -inset-1 bg-gradient-to-r from-primary via-white to-secondary rounded-full opacity-30 group-hover:opacity-50 blur transition duration-500"></div>
            <div className="relative flex items-center bg-[#0a111e]/80 backdrop-blur-xl border border-glass-border rounded-full p-2 shadow-neon-strong transition-all duration-300 group-hover:shadow-[0_0_80px_rgba(6,232,249,0.25)]">
              <div className="pl-6 text-primary">
                <span className="material-symbols-outlined text-[28px] animate-pulse">bolt</span>
              </div>
              <input
                autoFocus
                className="w-full bg-transparent border-none text-white text-xl placeholder-slate-500 focus:ring-0 px-6 py-4 font-light outline-none"
                placeholder="Initialize session..."
                type="text"
                onKeyDown={(e) => { if (e.key === 'Enter') handleIgnite(); }}
              />
              <button
                onClick={handleIgnite}
                className="bg-white text-black rounded-full px-8 py-4 font-semibold hover:bg-primary hover:text-black hover:scale-105 transition-all duration-300 flex items-center gap-2 shadow-[0_0_20px_rgba(255,255,255,0.3)]"
              >
                <span>Ignite</span>
                <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
              </button>
            </div>
          </div>

          {/* Options Grid */}
          <div className={`grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 w-full transition-all duration-1000 ${showMenu ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>

            <div onClick={handleIgnite} className="glass-panel p-6 rounded-2xl group hover:bg-glass-surface cursor-pointer transition-all hover:-translate-y-2 border-l-2 border-l-transparent hover:border-l-primary">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-primary/10 rounded-lg text-primary group-hover:shadow-neon transition-shadow">
                  <span className="material-symbols-outlined">add_circle</span>
                </div>
                <span className="text-xs font-mono text-slate-500">NEW</span>
              </div>
              <h3 className="text-lg font-medium text-slate-200 group-hover:text-white mb-2">New Workspace</h3>
              <p className="text-sm text-slate-400">Initialize a blank canvas for data ingestion and alchemical processing.</p>
            </div>

            <div onClick={handleIgnite} className="glass-panel p-6 rounded-2xl group hover:bg-glass-surface cursor-pointer transition-all hover:-translate-y-2 border-l-2 border-l-transparent hover:border-l-alchemy">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-alchemy/10 rounded-lg text-alchemy group-hover:shadow-alchemy-glow transition-shadow">
                  <span className="material-symbols-outlined">folder_open</span>
                </div>
                <span className="text-xs font-mono text-slate-500">LOAD</span>
              </div>
              <h3 className="text-lg font-medium text-slate-200 group-hover:text-white mb-2">Open Archive</h3>
              <p className="text-sm text-slate-400">Access previous transmutations and stable golden knowledge bases.</p>
            </div>

            <div onClick={handleIgnite} className="glass-panel p-6 rounded-2xl group hover:bg-glass-surface cursor-pointer transition-all hover:-translate-y-2 border-l-2 border-l-transparent hover:border-l-secondary">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-secondary/10 rounded-lg text-secondary group-hover:shadow-[0_0_15px_rgba(255,0,212,0.3)] transition-shadow">
                  <span className="material-symbols-outlined">auto_awesome</span>
                </div>
                <span className="text-xs font-mono text-slate-500">AI</span>
              </div>
              <h3 className="text-lg font-medium text-slate-200 group-hover:text-white mb-2">Auto-Synthesis</h3>
              <p className="text-sm text-slate-400">Let the engine analyze raw inputs and suggest optimal transformation paths.</p>
            </div>

          </div>
        </main>

        <footer className="absolute bottom-8 text-center w-full">
          <div className="flex items-center justify-center gap-6 text-xs text-slate-600 font-mono">
            <div className="flex items-center gap-2">
              <span className="size-1.5 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]"></span>
              <span>CORE: STABLE</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="size-1.5 rounded-full bg-primary shadow-[0_0_5px_rgba(6,232,249,0.5)]"></span>
              <span>PARTICLES: 14M</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[12px]">memory</span>
              <span>MEMORY: 12%</span>
            </div>
          </div>
        </footer>
      </div>

      {/* Abstract floating particles */}
      <div className="fixed top-1/4 left-1/4 w-2 h-2 bg-primary rounded-full blur-[1px] opacity-60 animate-pulse"></div>
      <div className="fixed top-3/4 left-1/5 w-1 h-1 bg-white rounded-full blur-[1px] opacity-40"></div>
      <div className="fixed top-1/3 right-1/4 w-1.5 h-1.5 bg-alchemy rounded-full blur-[2px] opacity-50"></div>
    </div>
  );
};
