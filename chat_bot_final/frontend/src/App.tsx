
import { Routes, Route } from "react-router-dom";
import NotFound from "@/pages/not-found";
import ChatPage from "@/pages/chat";
function App() {
  return (
 
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
  );
}

export default App;
