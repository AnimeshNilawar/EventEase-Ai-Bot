import ChatWindow from "./components/ChatWindow";
import FileUpload from "./components/FileUpload";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold text-blue-700 mb-6">
        🎯 EventEase – Smart Event Companion
      </h1>
      <div className="grid md:grid-cols-2 gap-6 w-full max-w-5xl">
        <ChatWindow />
        <FileUpload />
      </div>
      <p className="text-gray-500 text-sm mt-4">
        Powered by Gradient AI • Built with FastAPI + React
      </p>
    </div>
  );
}
