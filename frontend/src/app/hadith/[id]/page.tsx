"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";

interface HadithDetail {
  id: number;
  kitab: string;
  nomor_hadits: number;
  derajat: string;
  teks_arab: string;
  sanad: string;
  matan: string;
  share: { text_copy: string; image_api_url: string };
}

export default function HadithDetailPage() {
  const params = useParams();
  const id = params.id;
  const [data, setData] = useState<HadithDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDetail() {
      setLoading(true);
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/hadith/${id}`);
        const json = await res.json();
        if (json.status === "success") setData(json.data);
      } catch (error) {
        console.error("Fetch hadith failed:", error);
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchDetail();
  }, [id]);

  if (loading) return <div className="p-10 text-center text-gray-500 animate-pulse font-medium">Menelusuri riwayat al-Huda...</div>;
  if (!data) return <div className="p-10 text-center">Hadits tidak ditemukan.</div>;

  return (
    <main className="min-h-screen bg-white pb-20">
      <header className="sticky top-0 bg-white border-b border-[#f2f2f2] p-4 flex items-center justify-between z-50">
        <Link href="/" className="flex items-center gap-2">
          <Image src="/logo.png" alt="al-Huda" width={28} height={28} />
          <span className="text-xl font-medium text-[#202124]">al-Huda</span>
        </Link>
        <h2 className="text-sm font-medium text-[#70757a]">{data.kitab} No. {data.nomor_hadits}</h2>
        <div className="px-2 py-1 bg-green-50 text-green-700 text-[10px] font-bold rounded uppercase tracking-wider border border-green-100">
          {data.derajat}
        </div>
      </header>

      <article className="max-w-[800px] mx-auto px-6 py-12">
        {/* Arabic Text */}
        <div className="text-right mb-12">
          <p className="text-3xl md:text-4xl leading-[2] text-[#202124] font-serif" dir="rtl">
            {data.teks_arab}
          </p>
        </div>

        {/* Sanad & Matan Split */}
        <div className="space-y-10">
          <section>
            <h3 className="text-xs font-bold text-[#b0b3b8] uppercase tracking-widest mb-3">Rantai Perawi (Sanad)</h3>
            <p className="text-base text-[#70757a] leading-relaxed italic border-l-2 border-[#dfe1e5] pl-4">
              {data.sanad}
            </p>
          </section>

          <section>
            <h3 className="text-xs font-bold text-[#1a73e8] uppercase tracking-widest mb-3">Sabda Nabi (Matan)</h3>
            <p className="text-xl text-[#202124] leading-relaxed font-medium">
              {data.matan}
            </p>
          </section>
        </div>

        {/* Share Button */}
        <div className="mt-16 flex justify-center">
          <button 
            onClick={() => window.open(`http://127.0.0.1:8000${data.share.image_api_url}`, '_blank')}
            className="flex items-center gap-2 px-8 py-3 bg-[#1a73e8] text-white rounded-full hover:bg-[#1557b0] transition-colors shadow-lg"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Bagikan Sebagai Gambar
          </button>
        </div>
      </article>
    </main>
  );
}
