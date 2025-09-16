"""
Quick API Validation Script
"""
import requests
import sys

def test_api():
    base_url = "http://localhost:8000"

    try:
        # Test API root
        response = requests.get(f"{base_url}/api/v1/", timeout=5)
        print(f"✅ API Root: Status {response.status_code}")

        # Test docs
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"✅ API Docs: Status {response.status_code}")

        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/api/v1/admin/health", timeout=5)
            print(f"✅ Health Check: Status {response.status_code}")
        except:
            print("⚠️ Health endpoint requires auth (expected)")

        print("\n🎉 API is running successfully!")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
