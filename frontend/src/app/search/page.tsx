"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import Image from "next/image";

interface SearchResult {
  id: number;
  sumber: string;
  judul: string;
  snippet: string;
  skor_relevansi: number;
  detail_url: string;
}

function SearchHeader() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQ = searchParams?.get("q") || "";
  const [inputValue, setInputValue] = useState(initialQ);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      router.push(`/search?q=${encodeURIComponent(inputValue.trim())}`);
    }
  };

  return (
    <header className="sticky top-0 bg-white border-b border-[#f2f2f2] z-50">
      <div className="flex items-center p-4 gap-4 max-w-[1200px]">
        <Link href="/" className="flex items-center gap-2">
          <Image src="/logo.png" alt="al-Huda" width={32} height={32} />
          <span className="hidden md:block text-2xl font-medium text-[#202124]">al-Huda</span>
        </Link>
        <div className="flex-grow max-w-[692px] relative">
          <form onSubmit={handleSearch} className="flex items-center px-4 py-2 rounded-full border border-[#dfe1e5] shadow-sm focus-within:shadow-md transition-shadow">
            <input
              type="text"
              className="flex-grow bg-transparent outline-none text-base"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <button type="submit" className="p-1 hover:bg-gray-100 rounded-full transition-colors">
              <svg className="w-5 h-5 text-[#4285f4]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </header>
  );
}

function SearchContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const q = searchParams?.get("q") || "";
  const source = searchParams?.get("source") || "semua";
  const page = parseInt(searchParams?.get("page") || "1");
  
  const [results, setResults] = useState<SearchResult[]>([]);
  const [meta, setMeta] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchResults() {
      setLoading(true);
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "https://api-alhuda.masmuf.cloud";
        const res = await fetch(`${apiUrl}/api/v1/search?q=${encodeURIComponent(q)}&source=${source}&page=${page}`);
        const data = await res.json();
        if (data.status === "success") {
          setResults(data.results);
          setMeta(data.meta);
        }
      } catch (error) {
        console.error("Search failed:", error);
      } finally {
        setLoading(false);
      }
    }
    if (q) fetchResults();
  }, [q, source, page]);

  const handlePageChange = (newPage: number) => {
    router.push(`/search?q=${encodeURIComponent(q)}&source=${source}&page=${newPage}`);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="max-w-[652px] mx-auto px-4 md:ml-[160px] py-4 pb-20">
      {loading ? (
        <p className="text-[#70757a] text-sm animate-pulse">Menghimpun petunjuk dari al-Huda hal. {page}...</p>
      ) : (
        <>
          <p className="text-[#70757a] text-sm mb-6">
            Sekitar {meta?.total_results || 0} hasil ditemukan. (Halaman {page})
          </p>
          <div className="space-y-8">
            {results.map((res, index) => (
              <div key={`${res.sumber}-${res.id}-${index}`} className="group">
                <p className="text-xs text-[#202124] mb-1 opacity-80">
                  {res.sumber} <span className="mx-1">›</span> {res.judul.split(":")[0]}
                </p>
                <Link 
                  href={res.detail_url.replace("/api/v1", "")} 
                  className="text-xl text-[#1a0dab] hover:underline cursor-pointer decoration-1"
                >
                  {res.judul}
                </Link>
                <div 
                  className="text-[#4d5156] text-sm mt-1 leading-relaxed line-clamp-3"
                  dangerouslySetInnerHTML={{ __html: res.snippet }}
                />
              </div>
            ))}
          </div>

          {/* Pagination Controls */}
          {meta && meta.total_results > meta.per_page && (
            <div className="mt-12 flex items-center gap-2 border-t border-gray-100 pt-8">
              {page > 1 && (
                <button 
                  onClick={() => handlePageChange(page - 1)}
                  className="px-4 py-2 text-[#1a73e8] hover:bg-blue-50 rounded-lg transition-colors text-sm font-medium"
                >
                  Sebelumnya
                </button>
              )}
              
              <div className="flex gap-1">
                {[...Array(Math.min(meta.max_pages, Math.ceil(meta.total_results / meta.per_page)))].map((_, i) => (
                  <button
                    key={i + 1}
                    onClick={() => handlePageChange(i + 1)}
                    className={`w-8 h-8 flex items-center justify-center rounded-full text-xs transition-colors ${
                      page === i + 1 
                        ? "bg-[#1a73e8] text-white font-bold" 
                        : "text-[#70757a] hover:bg-gray-100"
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}
              </div>

              {page < Math.min(meta.max_pages, Math.ceil(meta.total_results / meta.per_page)) && (
                <button 
                  onClick={() => handlePageChange(page + 1)}
                  className="px-4 py-2 text-[#1a73e8] hover:bg-blue-50 rounded-lg transition-colors text-sm font-medium"
                >
                  Berikutnya
                </button>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default function SearchPage() {
  return (
    <main className="min-h-screen bg-white">
      <Suspense fallback={<p className="p-10 text-center">Memuat antarmuka pencarian...</p>}>
        <SearchHeader />
        <SearchContent />
      </Suspense>
    </main>
  );
}
