import ChatWindow from "./components/ChatWindow";
import FileUpload from "./components/FileUpload";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
            🎯 EventEase
          </h1>
          <p className="text-xl text-gray-600 font-medium">
            Your Smart Event Planning Companion
          </p>
          <p className="text-gray-500 text-sm mt-2">
            Get instant answers and upload documents to enhance your event planning
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 h-[600px]">
          <ChatWindow />
          <FileUpload />
        </div>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-gray-500 text-sm">
            Powered by <span className="font-semibold text-blue-600">Gradient AI</span> •
            Built with <span className="font-semibold text-purple-600">FastAPI + React</span>
          </p>
        </div>
      </div>
    </div>
  );
}
