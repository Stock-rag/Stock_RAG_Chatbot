import React, { useState, useRef, useEffect } from 'react'
import api from './api'

function Sidebar() {
  return (
    <aside className="w-80 bg-gradient-to-b from-blue-700 to-blue-600 text-white p-8 flex flex-col gap-8">
      <div className="flex items-center gap-4">
        <div className="w-14 h-14 rounded-full bg-yellow-400 flex items-center justify-center text-blue-800 text-2xl font-bold">$</div>
        <div>
          <h1 className="text-2xl font-bold">Finance</h1>
          <p className="text-sm opacity-90">RAG Playground</p>
        </div>
      </div>
      <nav className="flex flex-col gap-4 mt-6">
        <button className="flex items-center gap-3 text-lg px-4 py-3 bg-blue-800/30 hover:bg-blue-800/40">🏠 Home</button>
        <button className="flex items-center gap-3 text-lg px-4 py-3 bg-yellow-400 text-blue-900 font-semibold">💬 Chat</button>
      </nav>
      <div className="mt-auto text-sm opacity-90">
        <p className="font-semibold">Connected</p>
        <p className="text-xs">Local (dev)</p>
      </div>
    </aside>
  )
}

function MessageBubble({ from, text }) {
  const isUser = from === 'user'
  return (
    <div className={`max-w-[70%] ${isUser ? 'ml-auto text-white' : 'mr-auto text-gray-900'}`}>
      <div className={`${isUser ? 'bg-yellow-400 text-blue-900' : 'bg-blue-100'} p-5 break-words`}>
        {text}
      </div>
    </div>
  )
}

function ContextCard({ doc, idx }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border p-4 bg-white mb-3 max-w-full overflow-x-hidden">
      <div className="flex items-center justify-between">
        <div className="text-sm font-medium">Document {idx + 1}</div>
        <button onClick={() => setOpen(o => !o)} className="text-xs text-blue-600">
          {open ? 'Collapse' : 'Expand'}
        </button>
      </div>
      {open && (
        <pre className="mt-3 text-xs whitespace-pre-wrap break-words max-h-40 overflow-auto">{String(doc)}</pre>
      )}
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([
    { from: 'assistant', text: 'Hello! I am here to help with your finance RAG queries.' }
  ])
  const [contextDocs, setContextDocs] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, contextDocs])

  async function sendQuery() {
    if (!input.trim()) return
    const userMsg = { from: 'user', text: input }
    setMessages(m => [...m, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await api.post('/api/generate', { query: userMsg.text })
      const { answer, context } = res.data

      let docs = []
      if (Array.isArray(context)) {
        docs = context
      } else if (typeof context === 'string') {
        try {
          const parsed = JSON.parse(context)
          docs = Array.isArray(parsed) ? parsed : [String(context)]
        } catch {
          docs = [String(context)]
        }
      } else if (context != null) {
        docs = [String(context)]
      }

      setMessages(m => [...m, { from: 'assistant', text: String(answer ?? '') }])
      setContextDocs(docs.slice(0, 10))
    } catch (err) {
      console.error(err)
      setMessages(m => [...m, { from: 'assistant', text: 'Error: could not fetch results. Make sure backend is running.' }])
    } finally {
      setLoading(false)
    }
  }

  function onKey(e) {
    // Enter to send; Ctrl+Enter for newline
    if (e.key === 'Enter' && !e.ctrlKey) {
      e.preventDefault()
      sendQuery()
    }
  }

  return (
    <div className="h-screen w-screen">
      {/* Full-bleed layout (no rounded corners or card shadow) */}
      <div className="grid grid-cols-[20rem,1fr] h-full w-full">
        <Sidebar />
        <main className="p-6 flex flex-col gap-4 min-w-0">
          <header className="bg-blue-600 text-white p-4 text-center font-bold text-2xl">Chat</header>
          <div className="flex gap-6 h-full min-h-0">
            <section className="flex-1 bg-white p-6 flex flex-col min-w-0">
              <div className="flex-1 overflow-auto space-y-4">
                {messages.map((m, i) => (
                  <div key={i} className="flex">
                    <MessageBubble from={m.from} text={m.text} />
                  </div>
                ))}
                <div ref={scrollRef} />
              </div>
              <div className="mt-4">
                <div className="flex items-center gap-3">
                  <textarea
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={onKey}
                    rows={2}
                    placeholder="Type a message... (Enter to send, Ctrl+Enter for newline)"
                    className="flex-1 resize-none border px-6 py-4 focus:outline-none focus:ring-2 focus:ring-blue-200"
                  />
                  <button
                    onClick={sendQuery}
                    disabled={loading}
                    className="w-14 h-14 bg-yellow-400 text-blue-900 flex items-center justify-center font-bold disabled:opacity-60"
                  >
                    ➤
                  </button>
                </div>
                <div className="text-xs text-gray-400 mt-2">Tip: Press Enter to send. Use Ctrl+Enter for newline.</div>
              </div>
            </section>
            <aside className="w-96 bg-slate-50 p-6 min-w-0 overflow-x-hidden">
              <h3 className="font-semibold text-lg">Context (Retrieved Documents)</h3>
              <p className="text-xs text-gray-500 mt-1">These documents are what the retriever returned. Expand to view full content.</p>
              <div className="mt-4 h-[56vh] overflow-auto pr-2">
                {contextDocs.length === 0 ? (
                  <div className="text-sm text-gray-500">No context yet. Run a query to populate retrieved documents.</div>
                ) : (
                  contextDocs.map((d, i) => <ContextCard key={i} doc={d} idx={i} />)
                )}
              </div>
            </aside>
          </div>
        </main>
      </div>
    </div>
  )
}