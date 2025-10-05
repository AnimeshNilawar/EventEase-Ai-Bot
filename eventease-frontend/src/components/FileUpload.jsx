import { useState } from "react";
import { ingestFile } from "../api";

export default function FileUpload() {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState("");
    const [isUploading, setIsUploading] = useState(false);

    const handleUpload = async () => {
        if (isUploading) return;
        if (!file) {
            setStatus("Please choose a file first.");
            return;
        }
        setIsUploading(true);
        setStatus("Uploading...");
        try {
            const res = await ingestFile(file, true);
            setStatus(res.detail || "File uploaded and indexed!");
            // Optional: clear file after successful upload
            setFile(null);
        } catch (err) {
            const serverMsg = err?.response?.data?.detail || err?.message || "Upload failed.";
            setStatus(serverMsg);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="flex flex-col items-center p-4 border border-gray-300 rounded-2xl bg-white shadow-sm">
            <input
                type="file"
                onChange={(e) => setFile(e.target.files && e.target.files[0] ? e.target.files[0] : null)}
                className="p-2"
            />
            <p className="text-xs text-gray-500 mt-1 min-h-4">
                {file ? `Selected: ${file.name}` : "No file selected"}
            </p>
            <button
                onClick={handleUpload}
                disabled={isUploading}
                className={`mt-2 px-4 py-2 rounded-lg text-white ${
                    isUploading ? "bg-green-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"
                }`}
            >
                {isUploading ? "Uploading..." : "Upload"}
            </button>
            <p className="text-sm text-gray-600 mt-2 whitespace-pre-wrap">{status}</p>
        </div>
    );
}
