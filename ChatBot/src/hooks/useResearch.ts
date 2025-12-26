import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { startResearch as apiStartResearch } from '../services/api';
import { useToast } from '../components/ui/use-toast';

export const useResearch = () => {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const startResearch = async (query: string, isDeep: boolean = true) => {
    if (!query.trim()) return;

    setIsLoading(true);

    // Map mode to style number (assuming 1 is basic/blog, 2 is detailed/deep)
    const styleNumber = isDeep ? 2 : 1;

    try {
      const response = await apiStartResearch(query, styleNumber);
      const researchId = response.research_id;

      // Navigate to the editor with the research ID
      // The editor will check if it's a research ID and show the loading state
      navigate(`/editor/research/${researchId}`);

    } catch (error) {
      console.error('Error starting research:', error);
      setIsLoading(false);
      toast({
        title: "Research Failed",
        description: "Could not initiate research. Please try again.",
        variant: "destructive"
      });
    }
  };

  return { startResearch, isLoading };
};
