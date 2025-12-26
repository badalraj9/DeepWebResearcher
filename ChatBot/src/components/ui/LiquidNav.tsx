import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const LiquidNav: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <div
      className="fixed bottom-8 left-8 z-50 group"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <div className="relative flex flex-col-reverse items-start gap-4">
        {/* Main Orb (Trigger) */}
        <button className="relative size-16 rounded-full glass-panel bg-gradient-to-br from-white/10 to-transparent border border-primary/30 flex items-center justify-center text-primary shadow-[0_8px_32px_rgba(0,0,0,0.5)] hover:shadow-[0_0_30px_rgba(0,238,255,0.4)] hover:bg-primary hover:text-background-dark transition-all duration-500 ease-out z-20">
          <span className={`material-symbols-outlined text-3xl transition-transform duration-500 ${isOpen ? 'rotate-90' : ''}`}>
            grid_view
          </span>
          {/* Ripples */}
          <span className="absolute inset-0 rounded-full border border-primary/20 scale-100 group-hover:scale-150 opacity-0 group-hover:opacity-100 transition-all duration-700"></span>
        </button>

        {/* Expanded Menu Items */}
        <div className={`absolute bottom-full mb-4 left-1 flex flex-col gap-3 transition-all duration-500 origin-bottom ${isOpen ? 'translate-y-0 opacity-100 scale-100 pointer-events-auto' : 'translate-y-10 opacity-0 scale-75 pointer-events-none'}`}>

          <button onClick={() => navigate('/')} className="flex items-center gap-3 group/item">
            <div className="size-12 rounded-full glass-panel border border-white/10 bg-black/40 flex items-center justify-center text-white hover:bg-primary hover:border-primary hover:text-background-dark transition-colors shadow-lg">
              <span className="material-symbols-outlined text-xl">dashboard</span>
            </div>
            <span className="text-xs uppercase tracking-widest bg-black/80 px-2 py-1 rounded backdrop-blur-sm opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all text-white border border-white/10">Home</span>
          </button>

          <button onClick={() => navigate('/library')} className="flex items-center gap-3 group/item">
            <div className="size-12 rounded-full glass-panel border border-white/10 bg-black/40 flex items-center justify-center text-white hover:bg-secondary hover:border-secondary hover:text-white transition-colors shadow-lg">
              <span className="material-symbols-outlined text-xl">folder_open</span>
            </div>
            <span className="text-xs uppercase tracking-widest bg-black/80 px-2 py-1 rounded backdrop-blur-sm opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all text-white border border-white/10">Library</span>
          </button>

          <button onClick={() => navigate('/editor')} className="flex items-center gap-3 group/item">
            <div className="size-12 rounded-full glass-panel border border-white/10 bg-black/40 flex items-center justify-center text-white hover:bg-alchemy hover:border-alchemy hover:text-background-dark transition-colors shadow-lg">
              <span className="material-symbols-outlined text-xl">edit_note</span>
            </div>
            <span className="text-xs uppercase tracking-widest bg-black/80 px-2 py-1 rounded backdrop-blur-sm opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all text-white border border-white/10">Editor</span>
          </button>

        </div>
      </div>

      {/* Decorative Footer Element (Status Text) */}
      <div className="fixed bottom-6 right-8 z-40 text-right hidden md:block opacity-50 pointer-events-none">
        <div className="text-[10px] uppercase tracking-[0.3em] text-white/40">Secure Connection</div>
        <div className="text-[10px] uppercase tracking-[0.3em] text-primary/60 mt-1">Node: Alpha-Zero</div>
      </div>
    </div>
  );
};
