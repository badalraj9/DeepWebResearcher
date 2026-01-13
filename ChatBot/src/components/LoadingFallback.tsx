import { Loader2 } from "lucide-react";

export const LoadingFallback = () => {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-950 text-gray-100">
      <Loader2 className="h-10 w-10 animate-spin text-primary" />
    </div>
  );
};
