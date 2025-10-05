import { useState } from "react";
import { chat } from "../api";
import MessageBubble from "./MessageBubble";

export default function ChatWindow() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        if (!input.trim()) return;
        const newMsg = { sender: "user", text: input };
        setMessages((m) => [...m, newMsg]);

        const res = await chat(input);
        const botMsg = { sender: "bot", text: res.answer || "No response." };
        setMessages((m) => [...m, newMsg, botMsg]);
        setInput("");
    };

    return (
        <div className="flex flex-col h-full p-4 bg-gray-50 rounded-2xl shadow-md">
            <div className="flex-1 overflow-y-auto space-y-2">
                {messages.map((msg, i) => (
                    <MessageBubble key={i} {...msg} />
                ))}
            </div>
            <div className="mt-2 flex gap-2">
                <input
                    className="flex-1 border border-gray-300 rounded-lg p-2"
                    placeholder="Ask about the event..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                />
                <button
                    onClick={sendMessage}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                    Send
                </button>
            </div>
        </div>
    );
}
