"use client"
 
import { ThemeProvider } from "@/components/theme-provider"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { PrismEditorPage } from './pages/PrismEditorPage';
import { GlassLibraryPage } from './pages/GlassLibraryPage';
import { InstructionsPage } from './pages/InstructionsPage';
import { Toaster } from './components/ui/Toaster';
import './App.css';

// App wrapper component to handle router context
const AppRouter = () => {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/editor" element={<PrismEditorPage />} />
          <Route path="/editor/research/:researchId" element={<PrismEditorPage />} />
          <Route path="/editor/draft/:draftId" element={<PrismEditorPage />} />
          <Route path="/library" element={<GlassLibraryPage />} />
          <Route path="/instructions" element={<InstructionsPage />} />
        </Routes>
        <Toaster />
      </Router>
    </ThemeProvider>
  );
};

export default AppRouter;
