interface ChatHeaderProps {
  title?: string;
}

export function ChatHeader({ title = "AI Assistant" }: ChatHeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between z-10">
      <div className="flex items-center">
        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-white mr-3">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
            />
          </svg>
        </div>
        <h1 className="text-lg font-semibold">{title}</h1>
      </div>
    </header>
  );
}

export default ChatHeader;
