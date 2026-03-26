"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";

interface QuranDetail {
  id: number;
  surah: string;
  nomor_ayat: number;
  teks_arab: string;
  terjemah: string;
  tafsir: string;
  navigation: { prev_id: number | null; next_id: number | null };
  share: { text_copy: string; image_api_url: string };
}

export default function QuranDetailPage() {
  const params = useParams();
  const id = params.id;
  const [data, setData] = useState<QuranDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDetail() {
      setLoading(true);
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://api-alhuda.masmuf.cloud";
        const res = await fetch(`${apiUrl}/api/v1/quran/${id}`);
        const result = await res.json();

        if (json.status === "success") setData(json.data);
      } catch (error) {
        console.error("Fetch detail failed:", error);
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchDetail();
  }, [id]);

  if (loading) return <div className="p-10 text-center text-gray-500 animate-pulse font-medium">Membuka lembaran suci al-Huda...</div>;
  if (!data) return <div className="p-10 text-center">Ayat tidak ditemukan.</div>;

  return (
    <main className="min-h-screen bg-white pb-20">
      {/* Detail Header */}
      <header className="sticky top-0 bg-white border-b border-[#f2f2f2] p-4 flex items-center justify-between z-50">
        <Link href="/" className="flex items-center gap-2">
          <Image src="/logo.png" alt="al-Huda" width={28} height={28} />
          <span className="text-xl font-medium text-[#202124]">al-Huda</span>
        </Link>
        <h2 className="text-sm font-medium text-[#70757a]">{data.surah} Ayat {data.nomor_ayat}</h2>
        <div className="w-10"></div>
      </header>

      <article className="max-w-[800px] mx-auto px-6 py-12">
        {/* Arabic Text */}
        <div className="text-right mb-12">
          <p className="text-4xl md:text-5xl leading-[1.8] text-[#202124] font-serif" dir="rtl">
            {data.teks_arab}
          </p>
        </div>

        {/* Translation & Tafsir */}
        <div className="space-y-8">
          <section>
            <h3 className="text-xs font-bold text-[#70757a] uppercase tracking-widest mb-2">Terjemahan</h3>
            <p className="text-lg text-[#202124] leading-relaxed">{data.terjemah}</p>
          </section>

          <section className="bg-[#f8f9fa] p-6 rounded-xl">
            <h3 className="text-xs font-bold text-[#70757a] uppercase tracking-widest mb-2">Tafsir Wajiz</h3>
            <p className="text-[#4d5156] leading-relaxed italic">{data.tafsir}</p>
          </section>
        </div>

        {/* Action Button: Share */}
        <div className="mt-12 flex justify-center">
          <button 
            onClick={() => window.open(`http://127.0.0.1:8000${data.share.image_api_url}`, '_blank')}
            className="flex items-center gap-2 px-8 py-3 bg-[#1a73e8] text-white rounded-full hover:bg-[#1557b0] transition-colors shadow-sm"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
            Bagikan Ayat
          </button>
        </div>

        {/* Navigation */}
        <div className="mt-16 flex justify-between border-t border-[#f2f2f2] pt-8 text-[#1a73e8]">
          {data.navigation.prev_id && (
            <Link href={`/quran/${data.navigation.prev_id}`} className="hover:underline">← Ayat Sebelumnya</Link>
          )}
          {data.navigation.next_id && (
            <Link href={`/quran/${data.navigation.next_id}`} className="hover:underline">Ayat Berikutnya →</Link>
          )}
        </div>
      </article>
    </main>
  );
}
