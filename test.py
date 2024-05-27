import unittest

from main               import app
from fastapi.testclient import TestClient
from database           import SessionLocal, URL, Base, engine

client = TestClient(app)

class TestUnitURLShortener(unittest.TestCase):
    def test_shorten_url(self):
        response = client.post("/shorten/", json={"url": "https://www.example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_url", response.json())

        response = client.post("/shorten/", json={"url": "invalid_url"})
        self.assertEqual(response.status_code, 400)

class TestIntegrationURLShortener(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_shorten_url_and_redirect(self):
        response = client.post("/shorten/", json={"url": "https://www.example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_url", response.json())
        short_url = response.json()["short_url"]

        response = client.get(f"/{short_url}", allow_redirects=False)
        self.assertEqual(response.status_code, 301)

    def test_get_stats(self):
        response = client.post("/shorten/", json={"url": "https://www.example.com"})
        self.assertEqual(response.status_code, 200)
        short_url = response.json()["short_url"]

        response = client.get(f"/stats/{short_url}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_key", response.json())
        self.assertIn("num_visits", response.json())

if __name__ == "__main__":
    unittest.main()
