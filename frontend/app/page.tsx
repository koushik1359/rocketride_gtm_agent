"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search, Loader2, FileText, MessageCircle, Video,
  Image as ImageIcon, CheckCircle2, Rocket, Zap,
  GitBranch, Share2,
} from "lucide-react";

export default function Home() {
  const [repo, setRepo] = useState("rocketride-org/rocketride-server");
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<any>(null);

  const run = async () => {
    setRunning(true);
    setResult(null);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) return prev;
        return prev + 5;
      });
    }, 1000);

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const res = await fetch(`${apiBase}/api/run?repo=${repo}`, { method: "POST" });
      const data = await res.json();
      clearInterval(interval);
      setProgress(100);
      setResult(data);
    } catch {
      clearInterval(interval);
      alert("Error: Backend unreachable. Make sure uvicorn is running.");
    } finally {
      setTimeout(() => setRunning(false), 500);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-white to-cyan-50 font-sans text-slate-900 pb-32 relative overflow-x-hidden">

      {/* Decorative blobs */}
      <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
        <div className="absolute -top-40 -left-40 w-[500px] h-[500px] bg-violet-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
        <div className="absolute -top-20 -right-20 w-[500px] h-[500px] bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute bottom-0 left-1/2 w-[400px] h-[400px] bg-cyan-300 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-blob animation-delay-4000" />
      </div>

      {/* Nav */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b border-white/60 px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm shadow-violet-100/40">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-violet-600 to-pink-500 rounded-xl flex items-center justify-center shadow-lg shadow-violet-200/60">
            <Rocket className="text-white w-5 h-5" />
          </div>
          <div className="flex flex-col leading-tight">
            <span className="font-black text-base tracking-tight text-slate-900">RocketRide</span>
            <span className="text-xs font-bold bg-gradient-to-r from-violet-600 to-pink-500 bg-clip-text text-transparent">GTM Agent</span>
          </div>
        </div>

        <div className="flex items-center w-full sm:w-auto gap-3">
          <div className="relative w-full sm:w-96">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={repo}
              onChange={(e) => setRepo(e.target.value)}
              disabled={running}
              placeholder="owner/repo"
              className="w-full bg-white border border-slate-200 text-slate-900 text-sm rounded-xl py-2.5 pl-9 pr-4 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent shadow-sm transition-all disabled:opacity-60"
            />
          </div>
          <button
            onClick={run}
            disabled={running}
            className="flex items-center gap-2 bg-gradient-to-r from-violet-600 to-pink-500 hover:from-violet-700 hover:to-pink-600 text-white px-5 py-2.5 rounded-xl font-semibold text-sm shadow-lg shadow-violet-200 hover:shadow-xl hover:shadow-violet-300 transition-all disabled:opacity-50 whitespace-nowrap"
          >
            {running ? <Loader2 className="w-4 h-4 animate-spin" /> : <Rocket className="w-4 h-4" />}
            {running ? "Processing…" : "Run Pipeline"}
          </button>
        </div>
      </nav>

      {/* Main */}
      <main className="max-w-7xl mx-auto px-6 mt-16">

        {/* Hero */}
        <AnimatePresence>
          {!result && !running && (
            <motion.div
              key="hero"
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.45 }}
              className="max-w-3xl mb-20"
            >
              <div className="inline-flex items-center gap-2 bg-violet-100 text-violet-700 rounded-full px-4 py-1.5 text-sm font-semibold mb-6 border border-violet-200">
                <Zap className="w-3.5 h-3.5" />
                Multi-Agent Orchestration
              </div>

              <h1 className="text-5xl sm:text-6xl font-black tracking-tight leading-[1.05] mb-6">
                <span className="bg-gradient-to-r from-violet-600 via-pink-500 to-orange-400 bg-clip-text text-transparent">
                  Agentic GTM
                </span>
                <br />
                <span className="text-slate-900">Command Center</span>
              </h1>

              <p className="text-xl text-slate-500 leading-relaxed mb-10 max-w-2xl">
                Enter any GitHub repository to deploy a swarm of AI agents. We analyze your latest issues and ship your community blog post, Twitter thread, video script, and promo thumbnail — instantly.
              </p>

              <div className="flex flex-wrap gap-3">
                {[
                  { icon: <Zap className="w-3.5 h-3.5" />, label: "4 Parallel Agents" },
                  { icon: <GitBranch className="w-3.5 h-3.5" />, label: "Real GitHub Data" },
                  { icon: <Share2 className="w-3.5 h-3.5" />, label: "Ready to Post" },
                ].map(({ icon, label }) => (
                  <div key={label} className="flex items-center gap-2 bg-white border border-slate-200 rounded-full px-4 py-2 text-sm font-semibold text-slate-600 shadow-sm">
                    <span className="text-violet-500">{icon}</span>
                    {label}
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Progress */}
        <AnimatePresence>
          {running && (
            <motion.div
              key="progress"
              initial={{ opacity: 0, scale: 0.97 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.97 }}
              transition={{ duration: 0.4 }}
              className="w-full bg-white/90 backdrop-blur-sm border border-violet-100 rounded-2xl p-8 shadow-xl shadow-violet-100/50 mb-12"
            >
              <div className="flex items-center justify-between mb-5">
                <h3 className="font-bold text-slate-900 flex items-center gap-3 text-lg">
                  <div className="w-9 h-9 bg-gradient-to-br from-violet-500 to-pink-500 rounded-xl flex items-center justify-center shadow-md shadow-violet-200">
                    <Loader2 className="w-4 h-4 text-white animate-spin" />
                  </div>
                  Orchestrating Your Campaign…
                </h3>
                <span className="text-sm font-bold text-violet-700 bg-violet-50 border border-violet-200 px-3 py-1 rounded-full">
                  {progress}%
                </span>
              </div>

              <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                <div
                  className="h-3 rounded-full transition-all duration-1000 ease-out bg-gradient-to-r from-violet-500 via-pink-500 to-orange-400"
                  style={{ width: `${progress}%` }}
                />
              </div>

              <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-4">
                <AgentStep emoji="🔍" label="Researcher"  colorKey="violet" active={progress > 0}  done={progress > 25} />
                <AgentStep emoji="✍️" label="Copywriter"  colorKey="pink"   active={progress > 25} done={progress > 50} />
                <AgentStep emoji="🎨" label="Designer"    colorKey="amber"  active={progress > 50} done={progress > 75} />
                <AgentStep emoji="🎬" label="Producer"    colorKey="rose"   active={progress > 75} done={progress >= 100} />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {result && !running && (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="flex flex-col lg:flex-row gap-8 items-start"
            >
              {/* Blog Post */}
              <div className="w-full lg:w-2/3 bg-white rounded-2xl shadow-xl shadow-violet-100 overflow-hidden border border-violet-100">
                <div className="bg-gradient-to-r from-violet-600 to-indigo-600 px-8 py-6">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white/20 rounded-xl backdrop-blur-sm">
                      <FileText className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h2 className="text-lg font-bold text-white">Community Blog Post</h2>
                      <p className="text-sm text-violet-200">Copywriter Agent · {result.issues_analyzed} issues analyzed</p>
                    </div>
                    <div className="ml-auto flex items-center gap-1.5 bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-full backdrop-blur-sm">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Publish-ready
                    </div>
                  </div>
                </div>
                <div className="p-10">
                  <article className="prose-campaign">
                    <ReactMarkdown>{result.blog_post}</ReactMarkdown>
                  </article>
                </div>
              </div>

              {/* Sidebar cards */}
              <div className="w-full lg:w-1/3 flex flex-col gap-6">

                {/* Thumbnail */}
                <div className="bg-white rounded-2xl shadow-lg shadow-amber-100 overflow-hidden border border-amber-100">
                  <div className="bg-gradient-to-r from-amber-400 to-orange-500 px-5 py-4 flex items-center gap-3">
                    <div className="p-1.5 bg-white/20 rounded-lg backdrop-blur-sm">
                      <ImageIcon className="w-4 h-4 text-white" />
                    </div>
                    <h3 className="font-bold text-white text-sm">Promotional Graphic</h3>
                    <span className="ml-auto text-xs font-semibold text-amber-100 bg-white/10 px-2 py-0.5 rounded-full">DALL-E 3</span>
                  </div>
                  <div className="p-4">
                    <img
                      src={result.thumbnail_url}
                      alt="AI-generated promotional graphic"
                      className="w-full rounded-xl shadow-sm"
                    />
                  </div>
                </div>

                {/* Twitter Thread */}
                <div className="bg-white rounded-2xl shadow-lg shadow-sky-100 overflow-hidden border border-sky-100">
                  <div className="bg-gradient-to-r from-sky-400 to-blue-500 px-5 py-4 flex items-center gap-3">
                    <div className="p-1.5 bg-white/20 rounded-lg backdrop-blur-sm">
                      <MessageCircle className="w-4 h-4 text-white" />
                    </div>
                    <h3 className="font-bold text-white text-sm">Twitter Thread</h3>
                    <span className="ml-auto text-xs font-semibold text-sky-100 bg-white/10 px-2 py-0.5 rounded-full">5 tweets</span>
                  </div>
                  <div className="p-4">
                    <pre className="whitespace-pre-wrap font-mono text-xs leading-relaxed text-slate-700 bg-sky-50 p-4 rounded-xl border border-sky-100">
                      {result.twitter_thread}
                    </pre>
                  </div>
                </div>

                {/* Video Script */}
                <div className="bg-white rounded-2xl shadow-lg shadow-rose-100 overflow-hidden border border-rose-100">
                  <div className="bg-gradient-to-r from-rose-400 to-pink-500 px-5 py-4 flex items-center gap-3">
                    <div className="p-1.5 bg-white/20 rounded-lg backdrop-blur-sm">
                      <Video className="w-4 h-4 text-white" />
                    </div>
                    <h3 className="font-bold text-white text-sm">Video Script</h3>
                    <span className="ml-auto text-xs font-semibold text-rose-100 bg-white/10 px-2 py-0.5 rounded-full">30 sec</span>
                  </div>
                  <div className="p-4">
                    <pre className="whitespace-pre-wrap font-mono text-xs leading-relaxed text-slate-700 bg-rose-50 p-4 rounded-xl border border-rose-100">
                      {result.video_script}
                    </pre>
                  </div>
                </div>

              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </main>
    </div>
  );
}

type ColorKey = "violet" | "pink" | "amber" | "rose";

const agentStyles: Record<ColorKey, { idle: string; active: string; done: string }> = {
  violet: {
    idle:   "bg-slate-50 border-slate-200 text-slate-400",
    active: "bg-violet-50 border-violet-300 text-violet-700 shadow-md shadow-violet-100",
    done:   "bg-violet-50 border-violet-200 text-violet-700",
  },
  pink: {
    idle:   "bg-slate-50 border-slate-200 text-slate-400",
    active: "bg-pink-50 border-pink-300 text-pink-700 shadow-md shadow-pink-100",
    done:   "bg-pink-50 border-pink-200 text-pink-700",
  },
  amber: {
    idle:   "bg-slate-50 border-slate-200 text-slate-400",
    active: "bg-amber-50 border-amber-300 text-amber-700 shadow-md shadow-amber-100",
    done:   "bg-amber-50 border-amber-200 text-amber-700",
  },
  rose: {
    idle:   "bg-slate-50 border-slate-200 text-slate-400",
    active: "bg-rose-50 border-rose-300 text-rose-700 shadow-md shadow-rose-100",
    done:   "bg-rose-50 border-rose-200 text-rose-700",
  },
};

function AgentStep({
  emoji, label, colorKey, active, done,
}: {
  emoji: string;
  label: string;
  colorKey: ColorKey;
  active: boolean;
  done: boolean;
}) {
  const s = agentStyles[colorKey];
  const cls = done ? s.done : active ? s.active : s.idle;

  return (
    <div className={`flex items-center gap-3 p-3.5 rounded-xl border transition-all duration-500 ${cls}`}>
      <span className="text-xl leading-none">{emoji}</span>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-bold truncate">{label}</p>
        <p className="text-xs opacity-60 mt-0.5">
          {done ? "Complete ✓" : active ? "Running…" : "Waiting"}
        </p>
      </div>
    </div>
  );
}
