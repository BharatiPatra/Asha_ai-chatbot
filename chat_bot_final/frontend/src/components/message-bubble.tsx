import { cn } from "@/lib/utils";
import { Message } from "@/types/chat";
import { Copy, Check } from "lucide-react";
import { useState, type ReactNode } from "react";
import {
  Tooltip,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { marked } from 'marked';


interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === "user";
  const [copied, setCopied] = useState(false);

  const formatContent = (): ReactNode => {
    const paragraphs: ReactNode[] = [];
    const bulletPoints: ReactNode[] = [];
    const lines = message.content
      .split("\n")
      .filter((line) => line.trim().length > 0);

    lines.forEach((line, index) => {
      if (line.startsWith("•")) {
        bulletPoints.push(
          <li key={`bullet-${index}`} className="ml-5">
            {line.slice(1).trim()} 
          </li>
        );
      } else {
        paragraphs.push(
          <p key={`para-${index}`} className={index > 0 ? "mt-2" : ""}>
            {line}
          </p>
        );
      }
    });
    const html = marked.parse(message.content);

    return (
      <div
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  };

  const handleCopyText = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}
    >
      <div className="max-w-[80%] relative">
        <div
          className={cn(
            "rounded-lg px-4 py-3 text-sm shadow-sm",
            isUser
              ? "bg-gray-200 text-black rounded-tr-none"
              : "bg-indigo-500 text-white rounded-tl-none"
          )}
        >
          {formatContent()}
        </div>

        {!isUser && (
          <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <div className="flex gap-1">
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button
                      onClick={handleCopyText}
                      className="p-1 rounded-md bg-white/10 hover:bg-white/20 transition-colors"
                    >
                      {copied ? (
                        <Check className="h-3 w-3" />
                      ) : (
                        <Copy className="h-3 w-3" />
                      )}
                    </button>
                  </TooltipTrigger>
                </Tooltip>
              </TooltipProvider>
            </div>
          </div>
        )}
        <div className="text-xs text-gray-500 mt-1 font-medium">
          {isUser ? "You" : "AI Assistant"}
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
