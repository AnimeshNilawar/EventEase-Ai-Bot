export default function MessageBubble({ sender, text }) {
    const isUser = sender === "user";
    return (
        <div
            className={`flex ${isUser ? "justify-end" : "justify-start"
                } my-1`}
        >
            <div
                className={`px-3 py-2 rounded-xl max-w-[70%] ${isUser ? "bg-blue-600 text-white" : "bg-gray-200 text-black"
                    }`}
            >
                {text}
            </div>
        </div>
    );
}
