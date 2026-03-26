"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { ShareModal } from "@/components/ShareModal";

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
  const router = useRouter();
  const id = params.id;
  const [data, setData] = useState<QuranDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);

  useEffect(() => {
    async function fetchDetail() {
      setLoading(true);
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://api-alhuda.masmuf.cloud";
        const res = await fetch(`${apiUrl}/api/v1/quran/${id}`);
        const result = await res.json();

        if (result.status === "success") setData(result.data);
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
      <header className="sticky top-0 bg-white border-b border-[#f2f2f2] p-4 flex items-center gap-4 z-50">
        <button 
          onClick={() => router.back()}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          aria-label="Kembali"
        >
          <svg className="w-6 h-6 text-[#5f6368]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <Link href="/" className="flex items-center gap-2">
          <Image src="/logo.png" alt="al-Huda" width={28} height={28} />
          <span className="hidden md:block text-xl font-medium text-[#202124]">al-Huda</span>
        </Link>
        <div className="h-6 w-[1px] bg-gray-300 mx-1 hidden md:block"></div>
        <h2 className="text-sm font-medium text-[#70757a] flex-grow">{data.surah} Ayat {data.nomor_ayat}</h2>
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
            onClick={() => setIsShareModalOpen(true)}
            className="flex items-center gap-2 px-8 py-3 bg-[#00675b] text-white rounded-full hover:bg-[#004d44] transition-colors shadow-lg shadow-[#00675b]/20"
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

      <ShareModal 
        isOpen={isShareModalOpen}
        onClose={() => setIsShareModalOpen(false)}
        data={{
          title: `${data.surah} Ayat ${data.nomor_ayat}`,
          arabic: data.teks_arab,
          translation: data.terjemah
        }}
      />
    </main>
  );
}
