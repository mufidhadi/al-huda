"use client";

import React, { useRef, useState } from 'react';
import { Download, Share2, X, Image as ImageIcon } from 'lucide-react';
import html2canvas from 'html2canvas';

interface ShareModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: {
    title: string;
    arabic: string;
    translation: string;
    source?: string;
  };
}

export function ShareModal({ isOpen, onClose, data }: ShareModalProps) {
  const contentRef = useRef<HTMLDivElement>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  if (!isOpen) return null;

  // Dynamic font sizing logic
  const getArabicFontSize = (text: string) => {
    const len = text.length;
    if (len < 100) return '1.875rem'; // text-3xl
    if (len < 200) return '1.5rem';   // text-2xl
    if (len < 400) return '1.25rem';  // text-xl
    return '1.125rem';                // text-lg
  };

  const getTranslationFontSize = (text: string) => {
    const len = text.length;
    if (len < 200) return '0.875rem'; // text-sm
    if (len < 400) return '0.75rem';  // text-xs
    return '0.65rem';                 // smaller
  };

  const arabicFontSize = getArabicFontSize(data.arabic);
  const translationFontSize = getTranslationFontSize(data.translation);

  const handleDownload = async () => {
    if (!contentRef.current) return;
    setIsGenerating(true);
    
    try {
      const canvas = await html2canvas(contentRef.current, {
        // @ts-ignore
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff'
      });
      
      const image = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.href = image;
      link.download = `al-Huda_${data.title.replace(/\s+/g, '_')}.png`;
      link.click();
    } catch (error) {
      console.error('Error generating image:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleShare = async () => {
    if (!contentRef.current) return;
    setIsGenerating(true);

    try {
      const canvas = await html2canvas(contentRef.current, {
        // @ts-ignore
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff'
      });
      
      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const file = new File([blob], 'alhuda_share.png', { type: 'image/png' });
        
        if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
          await navigator.share({
            title: `al-Huda : ${data.title}`,
            text: `Merenungi ${data.title} via al-Huda`,
            files: [file]
          });
        } else {
          handleDownload();
        }
      }, 'image/png');
    } catch (error) {
      console.error('Error sharing:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-100">
          <div className="flex items-center gap-2 text-gray-700">
            <ImageIcon size={20} />
            <span className="font-semibold">Pratinjau Gambar Share</span>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Scrollable Preview Area */}
        <div className="p-6 bg-gray-50 flex flex-col items-center max-h-[70vh] overflow-y-auto">
          {/* THE CAPTURE ELEMENT */}
          <div 
            ref={contentRef}
            className="w-full max-w-[500px] bg-white relative overflow-hidden shadow-lg border border-gray-200"
            style={{ aspectRatio: '1 / 1' }}
          >
            {/* Design Elements */}
            <div className="absolute inset-0 border-[12px] border-[#00675b]/10 m-2 pointer-events-none"></div>
            
            <div className="h-full flex flex-col p-10 text-center relative z-10">
              {/* Logo & Title */}
              <div className="flex flex-col items-center mb-6">
                <div className="text-[#00675b] font-bold text-xl mb-1 tracking-tight">al-Huda</div>
                <div className="text-gray-400 text-[10px] uppercase tracking-[0.2em] font-medium">{data.title}</div>
                <div className="w-8 h-[2px] bg-[#00675b] mt-3"></div>
              </div>

              {/* Main Content */}
              <div className="flex-1 flex flex-col justify-center items-center gap-4 overflow-hidden">
                <p 
                  className="leading-[1.8] text-gray-900 font-serif px-2" 
                  dir="rtl"
                  style={{ fontSize: arabicFontSize }}
                >
                  {data.arabic}
                </p>
                <p 
                  className="text-gray-600 leading-relaxed italic px-4"
                  style={{ fontSize: translationFontSize }}
                >
                  "{data.translation}"
                </p>
              </div>

              {/* Footer */}
              <div className="mt-6 pt-6 border-t border-gray-100">
                <p className="text-[10px] text-[#00675b] font-semibold tracking-wider">
                  al-huda.masmuf.cloud
                </p>
                <p className="text-[8px] text-gray-400 mt-1 uppercase tracking-widest">
                  Petunjuk di Ujung Jari Anda
                </p>
              </div>
            </div>
          </div>
          <p className="text-xs text-gray-400 mt-4 italic text-center">
            * Gambar akan dihasilkan secara otomatis sesuai resolusi terbaik perangkat Anda.
          </p>
        </div>

        {/* Actions */}
        <div className="p-4 bg-white border-t border-gray-100 flex gap-3">
          <button
            onClick={handleDownload}
            disabled={isGenerating}
            className="flex-1 flex items-center justify-center gap-2 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-bold transition-all active:scale-95 disabled:opacity-50"
          >
            <Download size={18} />
            Simpan
          </button>
          <button
            onClick={handleShare}
            disabled={isGenerating}
            className="flex-1 flex items-center justify-center gap-2 py-3 bg-[#00675b] hover:bg-[#004d44] text-white rounded-xl font-bold shadow-lg shadow-[#00675b]/20 transition-all active:scale-95 disabled:opacity-50"
          >
            <Share2 size={18} />
            Bagikan
          </button>
        </div>
      </div>
    </div>
  );
}
