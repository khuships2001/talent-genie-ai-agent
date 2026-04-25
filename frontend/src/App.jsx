import { useState } from "react";
import axios from "axios";
import "./App.css";

// 🤖 ADD YOUR IMAGE HERE
import aiAgent from "./assets/ai-agent.jpeg";

export default function App() {
  const [jd, setJd] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const [selectedChat, setSelectedChat] = useState(null);

  const analyze = async () => {
    if (!jd.trim()) return;

    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8001/analyze", {
        jd: jd,
      });

      setResults(res.data || []);
    } catch (err) {
      console.log(err);
      alert("Backend error. Check server.");
    }

    setLoading(false);
  };

  return (
    <div className="container">

      {/* 🤖 AI IMAGE ADDED HERE */}
      <img src={aiAgent} alt="AI Agent" className="aiImage" />

      <h1>֎ TALENT GENIE <br /><br />AI Talent Scouting Agent</h1>

      <textarea
        placeholder="Paste Job Description..."
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />

      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Candidates"}
      </button>

      {/* ---------------- RESULTS ---------------- */}
      <div className="results">
        {results.length === 0 && !loading && (
          <p style={{ marginTop: "20px", opacity: 0.6 }}>
            No results yet. Paste JD and click analyze.
          </p>
        )}

        {results.map((r, i) => (
          <div key={i} className="card">
            <h2>{r.name}</h2>

            <p><b>Final Score:</b> {r.final_score}</p>
            <p><b>Match:</b> {r.match_score}</p>
            <p><b>Interest:</b> {r.interest_score}</p>

            <p><b>Matched:</b> {r.matched_skills?.join(", ") || "None"}</p>
            <p><b>Missing:</b> {r.missing_skills?.join(", ") || "None"}</p>

            <p className="reason">{r.reason}</p>

            <button
              className="chatBtn"
              onClick={() => setSelectedChat(r)}
            >
              See Chat 💬
            </button>
          </div>
        ))}
      </div>

      {/* ---------------- MODAL ---------------- */}
      {selectedChat && (
        <div className="modalOverlay" onClick={() => setSelectedChat(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>

            <h2 className="chatTitle">
  ֎ AI Interview Chat - {selectedChat.name}
</h2>

           <div className="chatBox">
  {selectedChat.chat?.map((msg, idx) => (
    <div key={idx} className={`chatMsg ${msg.role}`}>

      <div className="roleLabel">
        {msg.role === "candidate"
          ? (msg.name || selectedChat.name).toUpperCase()
          : "TALENT GENIE"}
      </div>

      <div className="msgText">
        {msg.message}
      </div>

    </div>
  ))}
</div>
            <button
              className="closeBtn"
              onClick={() => setSelectedChat(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}

    </div>
  );
}