import { useState, useRef, useEffect, FormEvent, ChangeEvent } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle, Send, Mic } from "lucide-react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

interface ChatInputProps {
  onSendMessage: (message: string, sessionId: string) => void; // Include sessionId
  isSending: boolean;
  error?: string | null;
  sessionId: string; // Passing sessionId as a prop
}

export function ChatInput({
  onSendMessage,
  isSending,
  error,
  sessionId,
}: ChatInputProps) {
  const [inputValue, setInputValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <span>Your browser does not support speech recognition.</span>;
  }
  useEffect(() => {
    if (listening) {
      setInputValue(transcript); // live update while speaking
    }
  }, [transcript, listening]);

  // Handle form submission
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    // Stop listening before sending
    if (listening) {
      SpeechRecognition.stopListening();
    }
    const message = inputValue.trim();
    if (!message || isSending) return;

    // Send message to the backend with session ID
    onSendMessage(message, sessionId);
    setInputValue("");
    resetTranscript(); // reset voice transcript as well

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = "60px";
    }
  };

  // Handle input changes, including auto-resizing the textarea
  const handleInput = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    autoResizeTextarea();
  };

  const autoResizeTextarea = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      const newHeight = Math.min(
        200,
        Math.max(60, textareaRef.current.scrollHeight)
      );
      textareaRef.current.style.height = `${newHeight}px`;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const form = e.currentTarget.form;
      if (form)
        form.dispatchEvent(
          new Event("submit", { cancelable: true, bubbles: true })
        );
    }
  };

  // Focus the textarea on mount and clean up timeout on unmount
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
    return () => {
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    };
  }, []);

  // Handle the microphone input
  const handleMicClick = () => {
    if (!listening) {
      resetTranscript();
      SpeechRecognition.startListening({ continuous: true });
    } else {
      SpeechRecognition.stopListening();
    }
  };

  return (
    <div className="px-4 bg-white sticky bottom-0 mx-auto border-gray-400">
      {error && (
        <Alert variant="destructive" className="mb-3">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form
        onSubmit={handleSubmit}
        className="flex flex-wrap items-end gap-2 w-full max-w-screen-lg mx-auto"
      >

        <div className="relative flex-1 min-w-0 rounded-full">
          <Textarea
            ref={textareaRef}
            value={inputValue}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="Message AI Assistant..."
            className="w-full text-sm pr-10 py-2.5 min-h-[60px] rounded-full resize-none overflow-hidden bg-white focus:outline-none sm:min-w-[300px] md:min-w-[500px] lg:min-w-[700px] xl:min-w-[900px]"
            disabled={isSending}
          />

          <button
            type="button"
            onClick={handleMicClick}
            className="absolute top-1/2 right-2 -translate-y-1/2 text-gray-700 hover:text-gray-700"
          >
            <Mic
              className={`h-4 w-4 ${listening ? "text-red-500" : "text-black"}`}
            />
          </button>
        </div>

        <Button
          type="submit"
          size="icon"
          className={`h-[44px] w-[44px] rounded-full transition-all duration-200 ${
            inputValue.trim()
              ? "bg-primary hover:bg-primary/90"
              : "bg-gray-200 text-gray-500"
          }`}
          disabled={!inputValue.trim() || isSending}
        >
          {isSending ? (
            <div className="h-5 w-5 rounded-full border-2 border-current border-t-transparent animate-spin" />
          ) : (
            <Send className="h-5 w-5 " />
          )}
        </Button>
      </form>

      <div className="text-xs text-center text-gray-500 mt-2">
        Press Enter to send, Shift+Enter for a new line
      </div>
    </div>
  );
}

export default ChatInput;
