import { ChatView } from "./views/chat";
import { ErrorBoundary } from "react-error-boundary";
import { ErrorView } from "./views/error";

function App() {
  return (
    <ErrorBoundary fallback={<ErrorView />}>
      <ChatView />
    </ErrorBoundary>
  );
}

export default App;
