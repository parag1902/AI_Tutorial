"use client";

import { FormEvent, useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const suggestedQuestions = [
  "Tell me about yourself",
  "What projects have you worked on?",
  "What are your technical skills?",
  "Where have you worked?",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMessage: Message = {
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat`,
        {
          method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
        body: JSON.stringify({
          question: text,
            }),
          }
        );

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the AI assistant. Please make sure the FastAPI backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await askQuestion(question);
  };

  return (
    <main className="min-h-screen bg-[#050505] text-white">
      {/* Navigation */}
      <nav className="border-b border-white/10">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div className="text-lg font-semibold">
            Parag<span className="text-cyan-400">.</span>
          </div>

          <div className="flex items-center gap-6 text-sm text-gray-400">
            <a
              href="#about"
              className="transition hover:text-white"
            >
              About
            </a>

            <a
              href="#projects"
              className="transition hover:text-white"
            >
              Projects
            </a>

            <a
              href="#assistant"
              className="transition hover:text-white"
            >
              AI Assistant
            </a>

            <a
              href="https://github.com/parag1902"
              target="_blank"
              rel="noopener noreferrer"
              className="transition hover:text-white"
            >
              GitHub
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section
        id="about"
        className="mx-auto max-w-6xl px-6 pb-24 pt-24"
      >
        <div className="max-w-3xl">
          <p className="mb-4 text-sm font-medium uppercase tracking-[0.3em] text-cyan-400">
            Agentic AI Developer
          </p>

          <h1 className="text-5xl font-bold leading-tight tracking-tight sm:text-7xl">
            Building intelligent
            <br />
            systems with{" "}
            <span className="text-cyan-400">
              AI.
            </span>
          </h1>

          <p className="mt-7 max-w-2xl text-lg leading-8 text-gray-400">
            I'm Parag Deshpande, a software engineer focused
            on Generative AI, LLMs, RAG, and agentic systems.
            Explore my work or ask my AI assistant anything
            about my resume.
          </p>

          <div className="mt-9 flex flex-wrap gap-4">
            <a
              href="#assistant"
              className="rounded-full bg-white px-6 py-3 font-medium text-black transition hover:bg-gray-200"
            >
              Ask My AI
            </a>

            <a
              href="#projects"
              className="rounded-full border border-white/20 px-6 py-3 font-medium transition hover:bg-white/10"
            >
              View Projects
            </a>
          </div>
        </div>
      </section>

      {/* Skills */}
      <section className="border-y border-white/10">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-px bg-white/10 sm:grid-cols-4">
          {[
            "Python",
            "LangChain",
            "LLMs",
            "FastAPI",
          ].map((skill) => (
            <div
              key={skill}
              className="bg-[#050505] px-6 py-8 text-center text-sm text-gray-300"
            >
              {skill}
            </div>
          ))}
        </div>
      </section>

      {/* Projects */}
      <section
        id="projects"
        className="mx-auto max-w-6xl px-6 py-24"
      >
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">
          Selected Work
        </p>

        <h2 className="mt-3 text-4xl font-bold">
          Projects
        </h2>

        <div className="mt-10 grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-7 transition hover:border-cyan-400/40">
            <p className="text-sm text-cyan-400">
              AI / Agentic Systems
            </p>

            <h3 className="mt-3 text-2xl font-semibold">
              LeadCommand
            </h3>

            <p className="mt-4 leading-7 text-gray-400">
              A scalable multi-agent AI platform designed
              for intelligent workflows and autonomous
              task execution.
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              {["Python", "LLM", "Agents", "LangChain"].map(
                (tech) => (
                  <span
                    key={tech}
                    className="rounded-full bg-white/5 px-3 py-1 text-xs text-gray-300"
                  >
                    {tech}
                  </span>
                )
              )}
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-7 transition hover:border-cyan-400/40">
            <p className="text-sm text-cyan-400">
              RAG / NLP
            </p>

            <h3 className="mt-3 text-2xl font-semibold">
              RAG-Powered IT Helpdesk
            </h3>

            <p className="mt-4 leading-7 text-gray-400">
              An AI-powered helpdesk assistant using
              retrieval augmented generation to answer
              technical support questions.
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              {["RAG", "LangChain", "Chroma", "LLMs"].map(
                (tech) => (
                  <span
                    key={tech}
                    className="rounded-full bg-white/5 px-3 py-1 text-xs text-gray-300"
                  >
                    {tech}
                  </span>
                )
              )}
            </div>
          </div>
        </div>
      </section>

      {/* AI Assistant */}
      <section
        id="assistant"
        className="border-t border-white/10"
      >
        <div className="mx-auto max-w-4xl px-6 py-24">
          <div className="text-center">
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">
              AI Resume Assistant
            </p>

            <h2 className="mt-3 text-4xl font-bold">
              Ask me anything.
            </h2>

            <p className="mx-auto mt-4 max-w-xl text-gray-400">
              Ask questions about my experience, projects,
              skills, education, or technical background.
            </p>
          </div>

          {/* Suggested questions */}
          <div className="mt-10 flex flex-wrap justify-center gap-3">
            {suggestedQuestions.map((item) => (
              <button
                key={item}
                onClick={() => askQuestion(item)}
                disabled={loading}
                className="rounded-full border border-white/10 bg-white/[0.03] px-4 py-2 text-sm text-gray-300 transition hover:border-cyan-400/40 hover:text-white disabled:opacity-50"
              >
                {item}
              </button>
            ))}
          </div>

          {/* Chat */}
          <div className="mt-10 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03]">
            <div className="min-h-[300px] max-h-[500px] space-y-5 overflow-y-auto p-6">
              {messages.length === 0 && (
                <div className="flex min-h-[250px] items-center justify-center text-center">
                  <div>
                    <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-cyan-400/10 text-xl">
                      ✦
                    </div>

                    <p className="text-gray-400">
                      Start a conversation with my AI assistant.
                    </p>
                  </div>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-5 py-3 leading-7 ${
                      message.role === "user"
                        ? "bg-cyan-400 text-black"
                        : "bg-white/10 text-gray-200"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="rounded-2xl bg-white/10 px-5 py-3 text-gray-400">
                    Thinking...
                  </div>
                </div>
              )}
            </div>

            {/* Input */}
            <form
              onSubmit={handleSubmit}
              className="border-t border-white/10 p-4"
            >
              <div className="flex gap-3">
                <input
                  type="text"
                  value={question}
                  onChange={(e) =>
                    setQuestion(e.target.value)
                  }
                  placeholder="Ask me anything about my resume..."
                  disabled={loading}
                  className="min-w-0 flex-1 rounded-xl border border-white/10 bg-black px-4 py-3 text-white outline-none placeholder:text-gray-600 focus:border-cyan-400/50"
                />

                <button
                  type="submit"
                  disabled={
                    loading || !question.trim()
                  }
                  className="rounded-xl bg-cyan-400 px-6 py-3 font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {loading ? "..." : "Ask"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10">
        <div className="mx-auto flex max-w-6xl flex-col justify-between gap-4 px-6 py-8 text-sm text-gray-500 sm:flex-row">
          <p>
            © {new Date().getFullYear()} Parag Deshpande
          </p>

          <p>
            Built with Next.js + FastAPI + Groq
          </p>
        </div>
      </footer>
    </main>
  );
}