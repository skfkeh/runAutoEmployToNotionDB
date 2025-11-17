import os
import requests

NOTION_API_KEY = os.getenv("NOTION_API_KEY")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def find_database_id(search_keyword: str):
    """Notion에서 검색 키워드로 DB를 찾아 database_id 반환"""
    query_url = "https://api.notion.com/v1/search"
    
    payload = {
        "query": search_keyword,
        "filter": {
            "value": "database",
            "property": "object"
        }
    }

    response = requests.post(query_url, json=payload, headers=headers).json()

    results = response.get("results", [])
    if not results:
        raise Exception(f"'{search_keyword}'로 검색되는 데이터베이스가 없습니다.")

    # 검색 결과 중 첫 번째 DB 반환
    return results[0]["id"]


def create_page(database_id: str):
    """추출한 database_id를 사용해 Notion 페이지 생성"""
    url = "https://api.notion.com/v1/pages"
    
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": "GitHub Action Test Page"}}
                ]
            }
        }
    }

    res = requests.post(url, json=data, headers=headers)
    print("Create Response:", res.json())


def main():
    # 🔍 여기서 원하는 DB 키워드를 넣으면 됨
    search_keyword = "지원 내역"   # 예: "EmployDB", "채용공고DB" 등

    print(f"Searching database with keyword: {search_keyword}")
    database_id = find_database_id(search_keyword)

    print("🔄 Found Database ID:", database_id)

    print("📄 Creating Notion page...")
    create_page(database_id)


if __name__ == "__main__":
    main()

