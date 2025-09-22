import requests
from bs4 import BeautifulSoup
import os

def fetch_with_proxy(url, proxy_url):
    """Proxy kullanarak URL'ye istek yapar"""
    try:
        response = requests.get(f"{proxy_url}{url}", timeout=10)
        response.raise_for_status()
        return response.text
    except:
        return None

def extract_domain(html_content):
    """HTML içeriğinden domaini çıkarır"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # İlgili divi bul
    target_div = soup.find('div', class_='mobile-button-container mobile')
    if target_div:
        # İlk a etiketini bul
        first_link = target_div.find('a')
        if first_link and first_link.has_attr('href'):
            return first_link['href']
    
    return None

def main():
    target_url = "https://amp-c8c5091b63.selcuksportshdamp-d2329a81bd.click/amp.html"
    proxy_url = "https://api.codetabs.com/v1/proxy/?quest="
    
    html_content = None
    
    # Önce normal erişim dene
    try:
        print("Normal bağlantı deneniyor...")
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        print("Normal bağlantı başarılı!")
    except Exception as e:
        print(f"Normal bağlantı başarısız: {e}")
        print("Proxy ile deneniyor...")
        html_content = fetch_with_proxy(target_url, proxy_url)
        if html_content:
            print("Proxy bağlantısı başarılı!")
        else:
            print("Her iki yöntem de başarısız oldu.")
            return
    
    # Domaini çıkar
    domain = extract_domain(html_content)
    
    if domain:
        # Dosyaya yaz
        with open('selcuk_sports_guncel_domain.txt', 'w') as f:
            f.write(f"guncel_domain={domain}")
        print(f"Domain başarıyla güncellendi: {domain}")
    else:
        print("HTML içeriğinden domain çıkarılamadı.")

if __name__ == "__main__":
    main()
