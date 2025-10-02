import { useEffect, useState } from 'react'
import './App.css'

export default function App() {
  const [apiStatus, setApiStatus] = useState('checking...')
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)

  useEffect(() => {
    let isMounted = true
    async function checkHealth() {
      try {
        const res = await fetch('http://localhost:8000/health')
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        if (isMounted) setApiStatus(`API: ${data.status}`)
      } catch (err) {
        if (isMounted) setApiStatus('API: unreachable')
      }
    }
    checkHealth()
    return () => { isMounted = false }
  }, [])

  return (
    <div>
      <h1>GenAI Demo</h1>
      <p>{apiStatus}</p>

      <div style={{
        display: 'flex', flexDirection: 'column', gap: '12px',
        marginTop: '16px', maxWidth: '720px'
      }}>
        <div style={{
          border: '1px solid #e5e5e5', borderRadius: '8px', padding: '12px',
          minHeight: '200px', background: '#fafafa'
        }}>
          {messages.length === 0 ? (
            <p style={{ color: '#666' }}>Start a conversation below…</p>
          ) : (
            messages.map((m, idx) => (
              <div key={idx} style={{
                display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start',
                marginBottom: '8px'
              }}>
                <div style={{
                  background: m.role === 'user' ? '#dbeafe' : '#e5e7eb',
                  color: '#111827', padding: '8px 12px', borderRadius: '12px',
                  maxWidth: '80%'
                }}>
                  {m.content}
                </div>
              </div>
            ))
          )}
        </div>

        <form onSubmit={async (e) => {
          e.preventDefault()
          const text = input.trim()
          if (!text || isSending) return
          setIsSending(true)
          setMessages(prev => [...prev, { role: 'user', content: text }])
          setInput('')
          try {
            const res = await fetch('http://localhost:8000/chat', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer demo-token'
              },
              body: JSON.stringify({ text })
            })
            if (!res.ok) {
              throw new Error(`HTTP ${res.status}`)
            }
            const data = await res.json()
            setMessages(prev => [...prev, { role: 'assistant', content: data.reply }])
          } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Fehler beim Senden.' }])
          } finally {
            setIsSending(false)
          }
        }} style={{ display: 'flex', gap: '8px' }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Nachricht eingeben…"
            style={{ flex: 1, padding: '10px 12px', borderRadius: '8px', border: '1px solid #e5e5e5' }}
          />
          <button type="submit" disabled={isSending || !input.trim()} style={{
            padding: '10px 14px', borderRadius: '8px', border: '1px solid #e5e5e5',
            background: isSending ? '#e5e7eb' : '#111827', color: isSending ? '#111827' : 'white',
            cursor: isSending ? 'not-allowed' : 'pointer'
          }}>
            {isSending ? 'Senden…' : 'Senden'}
          </button>
        </form>
      </div>
    </div>
  )
}
