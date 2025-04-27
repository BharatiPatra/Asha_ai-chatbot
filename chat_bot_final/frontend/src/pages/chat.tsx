import { useState, useEffect } from "react";
import ChatHeader from "../components/ChatHeader";
import ChatMessages from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";
import { Message } from "@/types/chat";
import { useChat } from "@/hooks/useChat";
import {
  sendMessage as apiSendMessage,
  getMessages as apiGetMessages,
} from "@/services/ChatService";
import { getSessionId, setSessionId } from "@/lib/session";

export default function ChatPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setLocalSessionId] = useState<string | null>(null);
  const { messages, addMessage, setMessages } = useChat();
  useEffect(() => {
    const initializeSession = async () => {
      try {
        let sid = getSessionId(); 

        if (!sid) {
          sid = crypto.randomUUID();
          setSessionId(sid);
        }

        setLocalSessionId(sid);
        const response = await apiGetMessages();
        const backendMessages = response?.messages || [];

        if (backendMessages.length > 0) {
          const formatted = backendMessages.map((msg) => ({
            id: msg.id || sid,
            content: msg.message,
            sender: msg.role === "user" ? "user" : "bot", 
            timestamp: new Date(msg.timestamp),
          })) as Message[]; 

          setMessages(formatted);
        }
      } catch (err) {
        console.error("Failed to initialize session or load messages:", err);
        setError("Failed to connect. Please try again.");
      }
    };

    initializeSession();
  }, []);

  const sendMessage = async (content: string) => {
    if (!sessionId) {
      setError("No active session. Please refresh the page.");
      return;
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
      content,
      sender: "user",
      timestamp: new Date(),
    };

    addMessage(userMessage);

    setIsLoading(true);
    setError(null);

    try {
      const response = await apiSendMessage(content);
      if (response && response.reply) {
        const botMessage: Message = {
          id: crypto.randomUUID(),
          content: response.reply,
          sender: "bot",
          timestamp: new Date(response.timestamp),
        };
        addMessage(botMessage);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to send message.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  return (
    <div className="flex flex-col h-screen  w-full bg-white shadow-xl">
      <ChatHeader />
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
        onSuggestionClick={handleSuggestionClick}
      />
      <ChatInput
        sessionId={sessionId || ""}
        onSendMessage={sendMessage}
        isSending={isLoading}
        error={error}
      />
    </div>
  );
}
