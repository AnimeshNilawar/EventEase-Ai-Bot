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
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden h-full">
            {/* Upload Header */}
            <div className="bg-gradient-to-r from-green-600 to-teal-600 text-white p-4 rounded-t-2xl">
                <h2 className="text-lg font-semibold">Document Upload</h2>
                <p className="text-green-100 text-sm">Upload files to enhance AI responses</p>
            </div>

            {/* Upload Area */}
            <div className="p-6 flex flex-col justify-center items-center h-full">
                <div className="w-full max-w-sm">
                    {/* File Drop Zone */}
                    <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-green-500 transition-colors duration-200 bg-gradient-to-b from-gray-50 to-white">
                        <div className="text-4xl mb-4">📄</div>
                        <p className="text-lg font-medium text-gray-700 mb-2">
                            Choose a file to upload
                        </p>
                        <p className="text-sm text-gray-500 mb-4">
                            Support for PDF, TXT, and other document formats
                        </p>

                        <input
                            type="file"
                            onChange={(e) => setFile(e.target.files && e.target.files[0] ? e.target.files[0] : null)}
                            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-medium file:bg-green-50 file:text-green-700 hover:file:bg-green-100 file:cursor-pointer cursor-pointer"
                            accept=".pdf,.txt,.doc,.docx"
                        />
                    </div>

                    {/* Selected File Info */}
                    {file && (
                        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                            <div className="flex items-center space-x-2">
                                <span className="text-green-600">✓</span>
                                <span className="text-sm font-medium text-green-800">Selected:</span>
                                <span className="text-sm text-green-700 truncate">{file.name}</span>
                            </div>
                        </div>
                    )}

                    {/* Upload Button */}
                    <button
                        onClick={handleUpload}
                        disabled={!file || isUploading}
                        className="w-full mt-4 bg-gradient-to-r from-green-600 to-teal-600 text-white px-6 py-3 rounded-full font-medium shadow-lg hover:from-green-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:-translate-y-0.5"
                    >
                        {isUploading ? (
                            <div className="flex items-center justify-center space-x-2">
                                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                <span>Uploading...</span>
                            </div>
                        ) : (
                            "Upload Document"
                        )}
                    </button>

                    {/* Status Message */}
                    {status && (
                        <div className={`mt-4 p-3 rounded-lg text-sm ${status.includes("failed") || status.includes("error")
                                ? "bg-red-50 border border-red-200 text-red-700"
                                : status.includes("uploaded") || status.includes("indexed")
                                    ? "bg-green-50 border border-green-200 text-green-700"
                                    : "bg-blue-50 border border-blue-200 text-blue-700"
                            }`}>
                            {status}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
