import { useEffect, useRef } from "react";
import { Message } from "@/types/chat";
import MessageBubble from "./message-bubble";

import WelcomeMessages from "./WelcomeMessage";

interface ChatMessagesProps {
  messages: Message[];
  isLoading: boolean;
  onSuggestionClick: (suggestion: string) => void;
}

export function ChatMessages({
  messages,
  isLoading,
  onSuggestionClick
}: ChatMessagesProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
   if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-4 space-y-4 custom-scrollbar"
      style={{
        scrollbarWidth: "thin",
        scrollbarColor: "#d1d5db #f1f1f1",
      }}
    >
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full">
          <WelcomeMessages onSuggestionClick={onSuggestionClick} />
        </div>
      ) : (
        messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))
      )}

      {isLoading && (
        <div className="message flex flex-col items-start">
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatMessages;