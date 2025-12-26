import React, { useState, useEffect } from 'react';
import { OracleSearch } from '../components/OracleSearch';
import { CinematicIntro } from '../components/CinematicIntro';
import { BackgroundEffects } from '../components/ui/BackgroundEffects';
import { LiquidNav } from '../components/ui/LiquidNav';

export const HomePage: React.FC = () => {
  const [showIntro, setShowIntro] = useState(true);

  // Check if we've already shown the intro in this session
  useEffect(() => {
    const hasSeenIntro = sessionStorage.getItem('hasSeenGenesisIntro');
    if (hasSeenIntro) {
      setShowIntro(false);
    }
  }, []);

  const handleIntroComplete = () => {
    sessionStorage.setItem('hasSeenGenesisIntro', 'true');
    setShowIntro(false);
  };

  return (
    <>
      {showIntro && <CinematicIntro onComplete={handleIntroComplete} />}
      
      <div className={`relative min-h-screen w-full flex flex-col transition-opacity duration-1000 ${showIntro ? 'opacity-0' : 'opacity-100'}`}>

        <BackgroundEffects />

        {/* Top Navigation (HUD) - Replaces NavMenu */}
        <header className="fixed top-0 left-0 w-full z-50 px-8 py-6 flex items-center justify-between border-b border-white/5 bg-gradient-to-b from-black/20 to-transparent backdrop-blur-sm pointer-events-none">
            <div className="flex items-center gap-4 pointer-events-auto">
                <div className="size-10 rounded-full border border-primary/30 flex items-center justify-center bg-primary/10 neon-box-cyan">
                    <span className="material-symbols-outlined text-primary text-2xl">all_inclusive</span>
                </div>
                <div>
                    <h2 className="text-white text-xl font-bold tracking-widest uppercase neon-text-cyan">Digital Alchemy</h2>
                    <span className="text-xs text-primary/60 tracking-[0.2em] uppercase">V 4.0.1 // Oracle Online</span>
                </div>
            </div>

            <div className="hidden md:flex gap-4">
                <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-primary/20 bg-background-dark/50 glass-panel">
                    <span className="size-2 rounded-full bg-primary animate-pulse"></span>
                    <span className="text-xs font-bold text-primary tracking-wider uppercase">System Potency: 98%</span>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-alchemy/20 bg-background-dark/50 glass-panel">
                    <span className="material-symbols-outlined text-alchemy text-sm">bolt</span>
                    <span className="text-xs font-bold text-alchemy tracking-wider uppercase">Aether Flow: Stable</span>
                </div>
            </div>
        </header>

        {/* Main Content */}
        <OracleSearch />

        {/* Floating Navigation Dock */}
        <LiquidNav />
      </div>
    </>
  );
};
