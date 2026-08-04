import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = import.meta.env.VITE_API_BASE_URL || "";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");

  async function login(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const res = await fetch(`${API}/api/auth/login`, { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) return setMessage(data.detail || "Login failed");
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
  }

  async function register(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const res = await fetch(`${API}/api/auth/register`, { method: "POST", body: form });
    const data = await res.json();
    setMessage(res.ok ? "Registered. Please login." : data.detail);
  }

  async function loadFiles() {
    if (!token) return;
    const res = await fetch(`${API}/api/files`, { headers: { Authorization: `Bearer ${token}` } });
    if (res.ok) setFiles(await res.json());
  }

  async function upload(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const res = await fetch(`${API}/api/files/upload`, {
      method: "POST", body: form, headers: { Authorization: `Bearer ${token}` }
    });
    setMessage(res.ok ? "Uploaded successfully." : "Upload failed.");
    await loadFiles();
  }

  async function download(id) {
    const res = await fetch(`${API}/api/files/${id}/download`, { headers: { Authorization: `Bearer ${token}` } });
    const data = await res.json();
    if (res.ok) window.open(data.url, "_blank");
  }

  async function remove(id) {
    await fetch(`${API}/api/files/${id}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` } });
    await loadFiles();
  }

  useEffect(() => { loadFiles(); }, [token]);

  if (!token) {
    return <main className="container">
      <h1>SecureCloudOps Portal</h1>
      <p>Cloud Drive + AWS SecOps Mega Project</p>
      {message && <div className="message">{message}</div>}
      <div className="auth-grid">
        <form onSubmit={login}><h2>Login</h2><input name="username" placeholder="Username" required/><input name="password" type="password" placeholder="Password" required/><button>Login</button></form>
        <form onSubmit={register}><h2>Register</h2><input name="username" placeholder="Username" required/><input name="password" type="password" placeholder="Password" required/><button>Register</button></form>
      </div>
    </main>;
  }

  return <main className="container">
    <header><div><h1>My Secure Drive</h1><p>Private S3 storage with automatic classification</p></div><button onClick={() => {localStorage.removeItem("token"); setToken("");}}>Logout</button></header>
    {message && <div className="message">{message}</div>}
    <form className="upload" onSubmit={upload}><input type="file" name="upload" required/><button>Upload</button></form>
    <section className="files">
      {files.map(file => <article key={file.id}>
        <div><strong>{file.name}</strong><small>{file.classification}</small></div>
        <div><button onClick={() => download(file.id)}>Download</button><button className="danger" onClick={() => remove(file.id)}>Delete</button></div>
      </article>)}
    </section>
  </main>;
}

createRoot(document.getElementById("root")).render(<App />);
