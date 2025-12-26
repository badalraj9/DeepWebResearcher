import React from 'react';

export const NeuralThinking: React.FC = () => {
  return (
    <div className="fixed inset-0 z-[60] bg-background-dark text-white font-display overflow-hidden w-screen h-screen selection:bg-primary selection:text-black">

      {/* Background Gradient & Noise */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_center,_#1a3d40_0%,_#0f2123_50%,_#000000_100%)] -z-20"></div>
      <div className="fixed inset-0 opacity-10 noise-overlay -z-10 pointer-events-none"></div>

      {/* Header */}
      <header className="absolute top-0 w-full flex items-center justify-between px-8 py-5 z-50">
        <div className="flex items-center gap-4 glass-panel rounded-full px-5 py-2">
            <div className="relative flex items-center justify-center size-8">
                {/* Oracle Eye Icon */}
                <span className="material-symbols-outlined text-primary text-3xl animate-pulse">visibility</span>
                <div className="absolute inset-0 bg-primary rounded-full blur-md opacity-40"></div>
            </div>
            <div className="flex flex-col">
                <h1 className="text-white text-base font-bold leading-none tracking-widest uppercase">Digital Alchemy</h1>
                <span className="text-primary/70 text-xs font-mono">Neural Engine v4.2</span>
            </div>
        </div>
      </header>

      {/* Main Content Area (3D Visualization Simulation) */}
      <main className="flex-1 relative w-full h-full perspective-[1000px] overflow-hidden flex items-center justify-center">

        {/* SVG Layer for Lines */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
            {/* Central radiating circles */}
            <circle cx="50%" cy="50%" fill="none" r="150" stroke="rgba(6, 232, 249, 0.1)" strokeDasharray="10 5" strokeWidth="1" className="animate-spin-slow"></circle>
            <circle cx="50%" cy="50%" fill="none" r="280" stroke="rgba(6, 232, 249, 0.05)" strokeWidth="1" className="animate-spin-reverse-slow"></circle>

            {/* Connecting Lines (Static for now, could be dynamic) */}
            <line x1="30%" y1="30%" x2="50%" y2="50%" stroke="rgba(6, 232, 249, 0.2)" strokeWidth="1" />
            <line x1="70%" y1="25%" x2="50%" y2="50%" stroke="rgba(6, 232, 249, 0.2)" strokeWidth="1" />
            <line x1="20%" y1="60%" x2="50%" y2="50%" stroke="rgba(6, 232, 249, 0.2)" strokeWidth="1" />
            <line x1="80%" y1="65%" x2="50%" y2="50%" stroke="rgba(6, 232, 249, 0.2)" strokeWidth="1" />
        </svg>

        {/* Central Core Node */}
        <div className="absolute z-10 flex flex-col items-center justify-center gap-4">
            <div className="relative size-32 rounded-full bg-black border border-primary/50 flex items-center justify-center shadow-[0_0_30px_rgba(6,232,249,0.3)]">
                <div className="absolute inset-0 rounded-full bg-primary/10 blur-xl animate-pulse"></div>
                <span className="material-symbols-outlined text-primary text-5xl animate-spin-slow">neurology</span>
            </div>
            <div className="glass-panel px-4 py-1 rounded-full text-primary font-bold tracking-widest text-sm uppercase shadow-neon">Core Processor</div>
        </div>

        {/* Satellite Node 1 (Top Left) */}
        <div className="absolute left-[28%] top-[28%] z-10 flex flex-col items-center gap-2 animate-float">
            <div className="size-14 rounded-full bg-background-dark border border-white/30 flex items-center justify-center shadow-[0_0_15px_rgba(255,255,255,0.2)]">
                <span className="material-symbols-outlined text-white/80 text-2xl">database</span>
            </div>
            <div className="text-xs text-white/60 font-mono bg-black/40 px-2 rounded">Raw Data</div>
        </div>

        {/* Satellite Node 2 (Top Right) */}
        <div className="absolute left-[70%] top-[25%] z-10 flex flex-col items-center gap-2 animate-float" style={{ animationDelay: '1s' }}>
            <div className="size-16 rounded-full bg-background-dark border border-secondary flex items-center justify-center neon-box-pink">
                <span className="material-symbols-outlined text-secondary text-2xl">science</span>
            </div>
            <div className="glass-panel px-3 py-1 rounded-full">
                <p className="text-xs text-secondary font-bold">Analysis</p>
            </div>
        </div>

        {/* Satellite Node 3 (Bottom Left) */}
        <div className="absolute left-[20%] top-[60%] z-10 flex flex-col items-center gap-2 animate-float" style={{ animationDelay: '2s' }}>
            <div className="size-12 rounded-full bg-background-dark border border-primary/40 flex items-center justify-center">
                <span className="material-symbols-outlined text-primary text-xl">share</span>
            </div>
            <div className="bg-primary/10 backdrop-blur-md border border-primary/20 px-3 py-1 rounded-full">
                <p className="text-xs text-primary">Sources: Searching...</p>
            </div>
        </div>

        {/* Satellite Node 4 (Bottom Right - Gold) */}
        <div className="absolute left-[80%] top-[65%] z-10 flex flex-col items-center gap-2 animate-float" style={{ animationDelay: '3s' }}>
            <div className="size-20 rounded-full bg-background-dark border-2 border-alchemy flex items-center justify-center shadow-alchemy-glow relative">
                <div className="absolute inset-0 bg-alchemy/10 rounded-full animate-pulse"></div>
                <span className="material-symbols-outlined text-alchemy text-4xl">light_mode</span>
            </div>
            <div className="glass-panel px-4 py-2 rounded-xl border-alchemy/30">
                <p className="text-xs text-alchemy font-bold uppercase tracking-wider">Synthesizing</p>
            </div>
        </div>

        {/* Left Sidebar: Alchemical Log (Timeline) */}
        <div className="absolute top-24 left-10 w-80 z-20 flex flex-col gap-4 pointer-events-none hidden md:flex">
            <h2 className="text-2xl font-bold text-white tracking-tight drop-shadow-md">Thought Process</h2>
            <div className="flex flex-col gap-0 relative">
                <div className="absolute left-[19px] top-4 bottom-4 w-[1px] bg-gradient-to-b from-primary/50 to-transparent"></div>

                {/* Item 1 */}
                <div className="flex gap-4 items-start group animate-in slide-in-from-left duration-700">
                    <div className="relative z-10 size-10 rounded-full bg-[#102223] border border-primary flex items-center justify-center shrink-0 shadow-[0_0_10px_rgba(6,232,249,0.3)]">
                        <span className="material-symbols-outlined text-primary text-sm">database</span>
                    </div>
                    <div className="glass-panel p-3 rounded-xl rounded-tl-none mb-4 flex-1 backdrop-blur-xl border-primary/20">
                        <p className="text-primary text-xs font-bold uppercase mb-1">Phase 1: Extraction</p>
                        <p className="text-white/80 text-sm">Parsing raw unstructured data...</p>
                    </div>
                </div>

                {/* Item 2 */}
                <div className="flex gap-4 items-start group animate-in slide-in-from-left duration-700 delay-300">
                    <div className="relative z-10 size-10 rounded-full bg-[#102223] border border-primary flex items-center justify-center shrink-0 shadow-[0_0_10px_rgba(6,232,249,0.3)]">
                        <span className="material-symbols-outlined text-primary text-sm animate-spin">cyclone</span>
                    </div>
                    <div className="glass-panel p-3 rounded-xl rounded-tl-none mb-4 flex-1 backdrop-blur-xl border-primary/20">
                        <p className="text-primary text-xs font-bold uppercase mb-1">Phase 2: Transmutation</p>
                        <p className="text-white/80 text-sm">Synthesizing Neural Weave...</p>
                    </div>
                </div>
            </div>
        </div>

        {/* Right Sidebar: Stats & Progress */}
        <div className="absolute top-24 right-10 w-72 z-20 flex flex-col gap-6 pointer-events-none hidden md:flex">
            {/* Progress Card */}
            <div className="glass-panel p-5 rounded-2xl border-t border-t-primary/40">
                <div className="flex justify-between items-end mb-2">
                    <span className="text-primary font-mono text-sm">PROCESSING</span>
                    <span className="text-white text-3xl font-bold animate-pulse">...</span>
                </div>
                <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-primary to-blue-500 w-[60%] shadow-[0_0_10px_rgba(6,232,249,0.8)] animate-[shimmer_2s_infinite]"></div>
                </div>
            </div>
        </div>

      </main>

      {/* Bottom Control Dock */}
      <footer className="absolute bottom-8 left-1/2 -translate-x-1/2 z-50">
        <div className="glass-panel px-2 py-2 rounded-full flex items-center gap-2 shadow-2xl">
            <div className="flex flex-col items-center px-4 w-48">
                <span className="text-[10px] text-primary font-mono uppercase tracking-widest mb-1">Status</span>
                <span className="text-sm font-bold text-white whitespace-nowrap">Weaving Nodes...</span>
            </div>
        </div>
      </footer>

    </div>
  );
};
