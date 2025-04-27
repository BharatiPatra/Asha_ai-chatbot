import React from "react";

interface WelcomeMessagesProps {
  onSuggestionClick: (prompt: string) => void;
}

const WelcomeMessages: React.FC<WelcomeMessagesProps> = ({ onSuggestionClick }) => {
  const suggestions = [
    "java jobs for freshers",
    "find me cloud events in banglore",
    "Find me cyber security events",
    "find me AI community",
  ];

  return (
    <div className="flex flex-col items-center justify-center w-full max-w-2xl mx-auto p-6">
      <h2 className="text-xl font-medium text-gray-800 mb-4">How can I help you today?</h2>
      <div className="flex flex-wrap justify-center gap-3">
        {suggestions.map((suggestion, idx) => (
          <button
            key={idx}
            onClick={() => onSuggestionClick(suggestion)}
            className="bg-blue-50 hover:bg-blue-100 text-gray-700 px-4 py-2 rounded-xl shadow transition duration-200"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
};

export default WelcomeMessages;