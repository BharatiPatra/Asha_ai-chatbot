export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}


export interface ChatSession {
  session_id: string;
  user_id?: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
}

export interface ApiResponse {
  reply: string;
  error?: string;
}
