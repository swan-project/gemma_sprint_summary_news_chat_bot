import requests
from bs4 import BeautifulSoup

def extract_article(link: str):
    response = requests.get(link)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    title='Untitled'
    title_content = soup.find(class_='tit')
    view_content = soup.find(class_='view_content')
    paragraphs = []
        
    if not view_content:
        return False, title, "view_content 클래스를 찾을 수 없습니다."

    # 제목 텍스트만 추출 (p 태그의 텍스트는 제외)
    if title_content:
        # strong 태그 내의 텍스트를 가져오되 p 태그는 제외
        title = title_content.contents[0].strip()

    # view_content 내의 모든 <p> 태그를 찾아 텍스트 추출
    for p in view_content.find_all('p'):
        paragraph_text = p.get_text(strip=True)
        if paragraph_text:  # 빈 문단 제외
            paragraphs.append(paragraph_text)
            # 결과 출력

    print(f"제목: {title}")  # 제목 출력
    print(f"총 {len(paragraphs)}개의 문단을 찾았습니다.")
    for i, para in enumerate(paragraphs, 1):
        print(f"문단 {i}: {para[:50]}...")  # 각 문단의 처음 50자만 출력
    
    return True, title, paragraphs
    