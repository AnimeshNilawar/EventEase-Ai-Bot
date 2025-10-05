export default function MessageBubble({ sender, text }) {
    const isUser = sender === "user";
    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
            <div className={`flex items-end space-x-2 max-w-[80%] ${isUser ? "flex-row-reverse space-x-reverse" : ""}`}>
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ${isUser
                        ? "bg-gradient-to-br from-blue-500 to-purple-600 text-white"
                        : "bg-gradient-to-br from-gray-400 to-gray-600 text-white"
                    }`}>
                    {isUser ? "U" : "AI"}
                </div>

                {/* Message Bubble */}
                <div className={`px-4 py-3 rounded-2xl shadow-sm ${isUser
                        ? "bg-gradient-to-br from-blue-600 to-purple-600 text-white rounded-br-md"
                        : "bg-white text-gray-800 border border-gray-200 rounded-bl-md"
                    }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{text}</p>
                </div>
            </div>
        </div>
    );
}
