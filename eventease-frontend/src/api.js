import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const chat = async (query, conversation_id = "demo_user") => {
    const res = await axios.post(`${API_BASE}/chat`, { query, conversation_id });
    return res.data;
};

export const ingestFile = async (file, override = false) => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post(`${API_BASE}/ingest?override=${override}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
};
