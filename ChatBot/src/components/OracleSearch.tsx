import React, { useState } from 'react';
import { useResearch } from '../hooks/useResearch';

export const OracleSearch: React.FC = () => {
  const { startResearch, isLoading } = useResearch();
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<'deep' | 'basic' | 'history' | 'config'>('deep');

  const handleSearch = () => {
    if (!query.trim()) return;

    // Trigger research based on mode
    if (mode === 'deep' || mode === 'basic') {
      startResearch(query, mode === 'deep');
    } else {
        // Fallback for now if other modes aren't connected yet
         startResearch(query, true);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="relative z-10 w-full max-w-7xl mx-auto flex flex-col items-center justify-center min-h-screen pt-20 pb-10 px-4">

      {/* Headline */}
      <div className="text-center mb-12 relative z-20 animate-in fade-in zoom-in duration-1000">
        <h1 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-primary to-white tracking-widest drop-shadow-[0_0_15px_rgba(0,238,255,0.5)]">
            ASK THE ORACLE
        </h1>
        <p className="text-primary/60 text-sm mt-2 tracking-[0.5em] uppercase font-light">
            Transmute Raw Data into Gold
        </p>
      </div>

      {/* The Oracle Eye (Central Interactive Area) */}
      <div className="relative flex items-center justify-center w-full max-w-3xl aspect-square md:aspect-video group/eye perspective-1000">

        {/* 3D Ring Simulation (Outer Torus) */}
        <div className="absolute w-[300px] h-[300px] md:w-[500px] md:h-[500px] rounded-full border border-white/10 shadow-[0_0_50px_rgba(0,238,255,0.1)] opacity-40 transition-all duration-1000 group-hover/eye:scale-105"></div>
        <div className="absolute w-[280px] h-[280px] md:w-[480px] md:h-[480px] rounded-full border border-dashed border-primary/20 animate-spin-slow group-hover/eye:border-primary/40 transition-colors"></div>
        <div className="absolute w-[320px] h-[320px] md:w-[540px] md:h-[540px] rounded-full border border-dotted border-white/5 opacity-30 animate-spin-reverse-slow"></div>

        {/* Glowing Energy Field */}
        <div className="absolute w-[200px] h-[200px] md:w-[350px] md:h-[350px] bg-primary/5 rounded-full blur-3xl group-hover/eye:bg-primary/10 transition-colors duration-500"></div>

        {/* Input Field (The Pupil) */}
        <div className="relative z-30 w-full max-w-lg">
          <div className="glass-panel rounded-full p-2 border border-primary/30 neon-box-cyan transition-all duration-500 hover:border-primary/60 hover:shadow-[0_0_40px_rgba(0,238,255,0.4)] focus-within:shadow-[0_0_50px_rgba(0,238,255,0.5)] focus-within:border-primary">
            <label className="flex items-center w-full h-14 md:h-16 px-4">
              <input
                className="w-full bg-transparent border-none text-white placeholder-primary/40 focus:ring-0 text-lg md:text-xl font-light tracking-wide text-center outline-none"
                placeholder="Enter transmutation query..."
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
              />
              <button
                onClick={handleSearch}
                disabled={isLoading}
                className="hidden md:flex size-12 rounded-full bg-primary text-background-dark items-center justify-center hover:bg-white transition-colors duration-300 shadow-[0_0_15px_rgba(0,238,255,0.6)] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                    <span className="material-symbols-outlined animate-spin">cyclone</span>
                ) : (
                    <span className="material-symbols-outlined font-bold">arrow_forward</span>
                )}
              </button>
            </label>
          </div>
        </div>

        {/* Orbital Category Moons (Radio List Replacement) */}
        <div className="absolute w-full h-full pointer-events-none z-20">

            {/* Deep Research Moon (Top) */}
            <div className={`absolute top-[10%] left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-auto transition-all duration-500 hover:scale-110 ${mode === 'deep' ? 'scale-110' : ''}`}>
                <label className="cursor-pointer group flex flex-col items-center gap-2" onClick={() => setMode('deep')}>
                    <div className={`size-14 rounded-full glass-panel border flex items-center justify-center text-white transition-all duration-300 ${mode === 'deep' ? 'bg-primary text-background-dark border-primary shadow-[0_0_20px_#00eeff]' : 'border-white/10 group-hover:border-primary/50'}`}>
                        <span className="material-symbols-outlined">dataset</span>
                    </div>
                    <span className={`text-[10px] uppercase tracking-wider transition-colors ${mode === 'deep' ? 'text-primary' : 'text-white/50 group-hover:text-primary'}`}>Deep Research</span>
                </label>
            </div>

            {/* Basic / Models Moon (Right) */}
            <div className={`absolute top-1/2 right-[10%] md:right-[15%] translate-x-1/2 -translate-y-1/2 pointer-events-auto transition-all duration-500 hover:scale-110 ${mode === 'basic' ? 'scale-110' : ''}`}>
                <label className="cursor-pointer group flex flex-col items-center gap-2" onClick={() => setMode('basic')}>
                    <div className={`size-14 rounded-full glass-panel border flex items-center justify-center text-white transition-all duration-300 ${mode === 'basic' ? 'bg-secondary text-white border-secondary shadow-[0_0_20px_#ff0099]' : 'border-white/10 group-hover:border-secondary/50'}`}>
                        <span className="material-symbols-outlined">model_training</span>
                    </div>
                    <span className={`text-[10px] uppercase tracking-wider transition-colors ${mode === 'basic' ? 'text-secondary' : 'text-white/50 group-hover:text-secondary'}`}>Basic Search</span>
                </label>
            </div>

            {/* History Moon (Bottom) */}
            <div className={`absolute bottom-[10%] left-1/2 -translate-x-1/2 translate-y-1/2 pointer-events-auto transition-all duration-500 hover:scale-110 ${mode === 'history' ? 'scale-110' : ''}`}>
                <label className="cursor-pointer group flex flex-col items-center gap-2" onClick={() => setMode('history')}>
                    <div className={`size-14 rounded-full glass-panel border flex items-center justify-center text-white transition-all duration-300 ${mode === 'history' ? 'bg-alchemy text-background-dark border-alchemy shadow-[0_0_20px_#ffd700]' : 'border-white/10 group-hover:border-alchemy/50'}`}>
                        <span className="material-symbols-outlined">history</span>
                    </div>
                    <span className={`text-[10px] uppercase tracking-wider transition-colors ${mode === 'history' ? 'text-alchemy' : 'text-white/50 group-hover:text-alchemy'}`}>History</span>
                </label>
            </div>

            {/* Config Moon (Left) */}
            <div className={`absolute top-1/2 left-[10%] md:left-[15%] -translate-x-1/2 -translate-y-1/2 pointer-events-auto transition-all duration-500 hover:scale-110 ${mode === 'config' ? 'scale-110' : ''}`}>
                <label className="cursor-pointer group flex flex-col items-center gap-2" onClick={() => setMode('config')}>
                    <div className={`size-14 rounded-full glass-panel border flex items-center justify-center text-white transition-all duration-300 ${mode === 'config' ? 'bg-white text-background-dark border-white shadow-[0_0_20px_white]' : 'border-white/10 group-hover:border-white/50'}`}>
                        <span className="material-symbols-outlined">tune</span>
                    </div>
                    <span className={`text-[10px] uppercase tracking-wider transition-colors ${mode === 'config' ? 'text-white' : 'text-white/50 group-hover:text-white'}`}>Config</span>
                </label>
            </div>

        </div>

      </div>
    </div>
  );
};
