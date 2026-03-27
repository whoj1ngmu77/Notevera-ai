'use client';
import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import StarField from '@/components/StarField';
import Sidebar from '@/components/Sidebar';
import GlowCard from '@/components/GlowCard';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { useRouter } from 'next/navigation';
import {
  RiUploadCloud2Line, RiFilePdf2Line, RiImageLine, RiYoutubeLine,
  RiClipboardLine, RiCheckLine, RiLoader4Line,
} from 'react-icons/ri';

type InputMode = 'pdf' | 'image' | 'youtube' | 'text';

const modes = [
  { id: 'pdf' as InputMode, icon: RiFilePdf2Line, label: 'PDF', color: '#f472b6' },
  { id: 'image' as InputMode, icon: RiImageLine, label: 'Image / Handwritten', color: '#a855f7' },
  { id: 'youtube' as InputMode, icon: RiYoutubeLine, label: 'YouTube Link', color: '#f87171' },
  { id: 'text' as InputMode, icon: RiClipboardLine, label: 'Paste Text', color: '#60a5fa' },
];

export default function UploadPage() {
  const [mode, setMode] = useState<InputMode>('pdf');
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [text, setText] = useState('');
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) setFile(f);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      let res;
      if ((mode === 'pdf' || mode === 'image') && file) {
        const form = new FormData();
        form.append('file', file);
        form.append('title', title || file.name);
        res = await api.post('/upload/file', form, { headers: { 'Content-Type': 'multipart/form-data' } });
      } else if (mode === 'youtube') {
        const form = new FormData();
        form.append('url', youtubeUrl);
        form.append('title', title || 'YouTube Lecture');
        res = await api.post('/upload/youtube', form);
      } else if (mode === 'text') {
        const form = new FormData();
        form.append('text', text);
        form.append('title', title || 'Pasted Notes');
        res = await api.post('/upload/text', form);
      }
      toast.success('Material processed! Generating AI notes...');
      router.push(`/notes?material_id=${res?.data?.id}`);
    } catch {
      toast.error('Failed to process material. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const canSubmit = (mode === 'pdf' || mode === 'image') ? !!file : mode === 'youtube' ? !!youtubeUrl : !!text;

  return (
    <div style={{ background: '#050010', minHeight: '100vh' }}>
      <StarField />
      <Sidebar />
      <main className="main-with-sidebar">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <h1 className="font-orbitron text-3xl font-bold text-white">Upload <span className="glow-text">Study Material</span></h1>
          <p className="text-gray-400 mt-2">Add any format — AI processes it all into unified knowledge.</p>
        </motion.div>

        {/* Title Input */}
        <GlowCard delay={0.05} className="p-5 mb-4">
          <label className="block text-sm text-gray-400 mb-2">Material Title (optional)</label>
          <input value={title} onChange={e => setTitle(e.target.value)}
            placeholder="e.g. Chapter 5 - Photosynthesis" className="input-cosmic" />
        </GlowCard>

        {/* Mode Selector */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-8">
          {modes.map((m, i) => (
            <motion.button
              key={m.id}
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
              onClick={() => { setMode(m.id); setFile(null); }}
              className={`p-4 rounded-xl border text-left transition-all duration-200 ${
                mode === m.id
                  ? 'border-purple-500/50 bg-purple-500/10 shadow-glow-sm'
                  : 'border-white/10 bg-white/5 hover:border-white/20'
              }`}
            >
              <m.icon style={{ color: m.color }} className="text-2xl mb-2" />
              <p className="text-white text-sm font-medium">{m.label}</p>
            </motion.button>
          ))}
        </div>

        {/* Input Area */}
        <GlowCard delay={0.2} className="p-6 mb-6">
          <AnimatePresence mode="wait">
            {(mode === 'pdf' || mode === 'image') && (
              <motion.div key="file" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                <div
                  onDragOver={e => { e.preventDefault(); setDragging(true); }}
                  onDragLeave={() => setDragging(false)}
                  onDrop={handleDrop}
                  onClick={() => fileRef.current?.click()}
                  className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200 ${
                    dragging ? 'border-purple-400 bg-purple-500/10' : 'border-white/10 hover:border-purple-500/40 hover:bg-white/5'
                  }`}
                >
                  <input
                    ref={fileRef} type="file" className="hidden"
                    accept={mode === 'pdf' ? '.pdf' : 'image/*'}
                    onChange={e => setFile(e.target.files?.[0] || null)}
                  />
                  {file ? (
                    <div className="flex flex-col items-center gap-2">
                      <RiCheckLine className="text-4xl text-green-400" />
                      <p className="text-white font-medium">{file.name}</p>
                      <p className="text-gray-400 text-sm">{(file.size / 1024).toFixed(1)} KB</p>
                    </div>
                  ) : (
                    <>
                      <RiUploadCloud2Line className="text-5xl text-gray-500 mx-auto mb-3" />
                      <p className="text-white font-medium mb-1">Drop your {mode === 'pdf' ? 'PDF' : 'image'} here</p>
                      <p className="text-gray-500 text-sm">or click to browse files</p>
                    </>
                  )}
                </div>
              </motion.div>
            )}
            {mode === 'youtube' && (
              <motion.div key="yt" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                <label className="block text-sm text-gray-400 mb-2">YouTube Lecture URL</label>
                <div className="flex gap-3">
                  <RiYoutubeLine className="text-red-400 text-2xl flex-shrink-0 mt-2.5" />
                  <input type="url" value={youtubeUrl} onChange={e => setYoutubeUrl(e.target.value)}
                    placeholder="https://www.youtube.com/watch?v=..." className="input-cosmic" />
                </div>
                <p className="text-gray-500 text-xs mt-2 ml-9">AI will extract the transcript and create structured notes.</p>
              </motion.div>
            )}
            {mode === 'text' && (
              <motion.div key="txt" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                <label className="block text-sm text-gray-400 mb-2">Paste Your Notes</label>
                <textarea value={text} onChange={e => setText(e.target.value)}
                  placeholder="Paste your notes, lecture transcript, or any text here..."
                  rows={10} className="input-cosmic resize-none" />
                <p className="text-gray-500 text-xs mt-2">{text.length} characters</p>
              </motion.div>
            )}
          </AnimatePresence>
        </GlowCard>

        {/* Submit */}
        <motion.button
          onClick={handleSubmit}
          disabled={!canSubmit || loading}
          whileHover={canSubmit && !loading ? { scale: 1.02 } : {}}
          whileTap={canSubmit && !loading ? { scale: 0.98 } : {}}
          className="btn-neon py-3 px-8 text-sm flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? (
            <><RiLoader4Line className="animate-spin" /><span>Processing with AI...</span></>
          ) : (
            <><span>Process & Generate Notes →</span></>
          )}
        </motion.button>
      </main>
    </div>
  );
}
