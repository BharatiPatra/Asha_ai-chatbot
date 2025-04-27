import axios from "axios";
import { getSessionId } from "../lib/session"; 

const API_BASE = import.meta.env.VITE_API_BASE_URL;

interface ChatResponse {
  reply: string;
  timestamp: string;
  session_id: string;
}

interface MessagesResponse {
  messages: Array<{
    id: string;
    role: string;
    message: string;
    timestamp: string;
  }>;
  session_id: string;
}

export const sendMessage = async (content: string): Promise<ChatResponse> => {
  const sessionId = getSessionId();
  if (!sessionId) {
    throw new Error("No active session ID");
  }

  try {
    const response = await axios.post<ChatResponse>(`${API_BASE}/chat`, {
      session_id: sessionId, 
      content: content,
    });

    return response.data;
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
};
export const getMessages = async (): Promise<MessagesResponse> => {
  const sessionId = getSessionId();

  if (!sessionId) {
    return { messages: [], session_id: "" };
  }

  try {
    const response = await axios.post<MessagesResponse>(
      `${API_BASE}/chat/history`,
      {
        session_id: sessionId, 
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error fetching messages:", error);
    throw error;
  }
};
