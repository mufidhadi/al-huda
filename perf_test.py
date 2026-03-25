import time
import os
import psutil
import statistics
from search_engine import QuranHadithSearch

# Database Configuration
DB_CONFIG = {
    "host": "DB_HOST_PLACEHOLDER",
    "user": "DB_USER_PLACEHOLDER",
    "password": "DB_PASS_PLACEHOLDER",
    "dbname": "tanya_quran_hadist"
}

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) # Return in MB

def run_performance_test():
    print("🚀 STARTING PERFORMANCE & RESOURCE AUDIT\n")
    
    # 1. Baseline Memory
    mem_before = get_memory_usage()
    print(f"📊 RAM Usage (Baseline): {mem_before:.2f} MB")
    
    # 2. Init Engine (Model Loading)
    start_init = time.time()
    engine = QuranHadithSearch(DB_CONFIG)
    end_init = time.time()
    
    mem_after_init = get_memory_usage()
    print(f"📊 RAM Usage (Model Loaded): {mem_after_init:.2f} MB")
    print(f"⏱️  Model Initialization Time: {end_init - start_init:.2f} seconds")
    print(f"📈 Net RAM for Model: {mem_after_init - mem_before:.2f} MB\n")
    
    # 3. Search Latency Test
    test_queries = [
        "shalat", "puasa", "zakat", "haji", "sabar", 
        "anak yatim", "hari kiamat", "surga", "neraka", "niat"
    ]
    
    latencies = []
    print(f"🔍 Benchmarking {len(test_queries)} search queries...")
    
    for query in test_queries:
        start_search = time.time()
        results = engine.search(query, source="semua", limit=10)
        end_search = time.time()
        
        latency = (end_search - start_search) * 1000 # in ms
        latencies.append(latency)
        # print(f"   - '{query}': {latency:.2f} ms")
        
    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[18] # 95th percentile
    
    print(f"\n⏱️  Average Latency: {avg_latency:.2f} ms")
    print(f"⏱️  P95 Latency: {p95_latency:.2f} ms")
    print(f"📊 RAM Usage (After Searches): {get_memory_usage():.2f} MB")
    
    return {
        "mem_init": mem_after_init - mem_before,
        "avg_lat": avg_latency,
        "p95_lat": p95_latency
    }

if __name__ == "__main__":
    run_performance_test()
