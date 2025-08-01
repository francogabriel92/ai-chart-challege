import { Button } from "@/components/ui/button";

export const ErrorView = () => {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-green-600">Oops!</h1>
        <p className="mt-4 text-lg text-gray-700">
          An unexpected error has occurred. Please try again later.
        </p>
        <div className="mt-6 flex justify-center">
          <Button onClick={() => window.location.reload()}>Reload Page</Button>
        </div>
      </div>
    </div>
  );
};
