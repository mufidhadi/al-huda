"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function Home() {
  const [query, setQuery] = useState("");
  const [source, setSource] = useState("semua");
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query)}&source=${source}`);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      {/* Branding: Logo & Name */}
      <div className="flex flex-col items-center mb-8">
        <Image 
          src="/logo.png" 
          alt="al-Huda Logo" 
          width={120} 
          height={120} 
          className="mb-4"
          priority
        />
        <h1 className="text-4xl md:text-6xl font-medium text-[#202124] tracking-tight">
          al-Huda
        </h1>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="w-full max-w-[584px] relative group">
        <div className="flex items-center px-4 py-3 rounded-full border border-[#dfe1e5] hover:shadow-md focus-within:shadow-md transition-all duration-200">
          <svg className="w-5 h-5 text-[#9aa0a6] mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            className="flex-grow bg-transparent outline-none text-base"
            placeholder="Tanyakan apa saja tentang Quran & Hadist..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
        </div>

        {/* Source Tabs */}
        <div className="flex justify-center gap-6 mt-6 text-sm text-[#70757a]">
          {["semua", "alquran", "hadist"].map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => setSource(s)}
              className={`pb-1 border-b-2 transition-all capitalize ${
                source === s ? "border-[#1a73e8] text-[#1a73e8] font-medium" : "border-transparent hover:text-[#202124]"
              }`}
            >
              {s === "hadist" ? "Hadits" : s}
            </button>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center mt-8">
          <button
            type="submit"
            className="px-6 py-2 bg-[#f8f9fa] text-[#3c4043] rounded border border- DadDadDad DadDadDad dadce0 hover:shadow-sm text-sm"
          >
            Penelusuran al-Huda
          </button>
        </div>
      </form>
    </main>
  );
}
