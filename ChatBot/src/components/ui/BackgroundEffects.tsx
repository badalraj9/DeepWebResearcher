import React from 'react';

export const BackgroundEffects: React.FC = () => {
  return (
    <div className="fixed inset-0 z-0 bg-void-gradient pointer-events-none">
      {/* Noise Overlay */}
      <div className="absolute inset-0 noise-overlay mix-blend-overlay opacity-40 z-10"></div>

      {/* Starfield */}
      <div className="absolute inset-0 starfield mix-blend-overlay opacity-30 z-0"></div>

      {/* Abstract gradient orbs for atmosphere */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-[100px] -z-10 animate-float"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/10 rounded-full blur-[120px] -z-10 animate-float" style={{ animationDelay: '2s' }}></div>
      <div className="absolute top-1/3 right-1/3 w-64 h-64 bg-alchemy/5 rounded-full blur-[80px] -z-10 animate-float" style={{ animationDelay: '4s' }}></div>
    </div>
  );
};
