import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_endpoint_structure():
    """Memastikan endpoint search mengembalikan struktur sesuai API Contract."""
    response = client.get("/api/v1/search?q=shalat&source=semua&page=1")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert "meta" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    
    if len(data["results"]) > 0:
        res = data["results"][0]
        assert "sumber" in res
        assert "judul" in res
        assert "snippet" in res
        assert "skor_relevansi" in res
        assert "detail_url" in res

def test_search_invalid_params():
    """Memastikan API menangani request tanpa query string."""
    response = client.get("/api/v1/search")
    assert response.status_code == 400

def test_quran_detail_endpoint():
    """Memastikan endpoint detail quran mengembalikan struktur yang benar."""
    # ID 153 adalah QS Al-Baqarah: 153
    response = client.get("/api/v1/quran/153")
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["id"] == 153
    assert "teks_arab" in data["data"]
    assert "navigation" in data["data"]
    assert "recommendations" in data

def test_hadith_detail_endpoint():
    """Memastikan endpoint detail hadith mengembalikan struktur yang benar."""
    response = client.get("/api/v1/hadith/1")
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["nomor_hadits"] == 1
    assert "matan" in data["data"]
    assert "recommendations" in data
