import { useState, useEffect, useRef } from "react";
import { chat } from "../api";
import MessageBubble from "./MessageBubble";

export default function ChatWindow() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom when new messages are added
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = { sender: "user", text: input };
        const userInput = input; // Store input before clearing

        // Add user message and clear input immediately
        setMessages((m) => [...m, userMessage]);
        setInput("");
        setIsLoading(true);

        try {
            const res = await chat(userInput);
            const botMsg = { sender: "bot", text: res.answer || "No response." };
            setMessages((m) => [...m, botMsg]);
        } catch {
            const errorMsg = { sender: "bot", text: "Sorry, I encountered an error. Please try again." };
            setMessages((m) => [...m, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
            {/* Chat Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-t-2xl">
                <h2 className="text-lg font-semibold">EventEase AI Assistant</h2>
                <p className="text-blue-100 text-sm">Ask me anything about your event!</p>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 bg-gradient-to-b from-gray-50 to-white">
                <div className="space-y-4 max-w-4xl mx-auto">
                    {messages.length === 0 && (
                        <div className="text-center text-gray-500 mt-8">
                            <div className="text-4xl mb-4">💬</div>
                            <p className="text-lg">Welcome to EventEase!</p>
                            <p className="text-sm">Start by asking a question about your event.</p>
                        </div>
                    )}
                    {messages.map((msg, i) => (
                        <MessageBubble key={i} {...msg} />
                    ))}
                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="bg-gray-100 px-4 py-3 rounded-xl max-w-[70%] flex items-center space-x-2">
                                <div className="flex space-x-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                </div>
                                <span className="text-gray-500 text-sm">AI is thinking...</span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 p-4 bg-white">
                <div className="flex gap-3 max-w-4xl mx-auto">
                    <input
                        className="flex-1 border border-gray-300 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder-gray-400"
                        placeholder="Type your message here..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
                        disabled={isLoading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={!input.trim() || isLoading}
                        className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-full hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                    >
                        {isLoading ? (
                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        ) : (
                            "Send"
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
