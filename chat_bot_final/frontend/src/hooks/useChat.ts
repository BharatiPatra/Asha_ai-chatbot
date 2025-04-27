import { useState } from "react";
import { Message } from "@/types/chat";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const addMessage = (
    content: string | Message,
    sender: "user" | "bot" = "user"
  ) => {
    const newMessage: Message =
      typeof content === "string"
        ? {
            id: `msg_${Date.now()}`,
            content,
            sender,
            timestamp: new Date(),
          }
        : content;

    setMessages((prev) => [...prev, newMessage]);
  };
  const updateMessages = (msgs: Message[]) => {
    setMessages(msgs);
  };

  return {
    messages,
    addMessage,
    setMessages: updateMessages,
  };
}
