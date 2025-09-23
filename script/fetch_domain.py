import requests
from bs4 import BeautifulSoup
import re

def fetch_with_proxy(url, proxy_url):
    """Proxy kullanarak URL'ye istek yapar"""
    try:
        full_url = f"{proxy_url}{url}"
        print(f"Proxy URL: {full_url}")
        response = requests.get(full_url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Proxy bağlantı hatası: {e}")
        return None

def extract_domain(html_content):
    """HTML içeriğinden domaini çıkarır"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Regex ile daha geniş bir arama yapalım
        mobile_button_div = soup.find('div', class_=re.compile(r'mobile-button-container'))
        
        if mobile_button_div:
            first_link = mobile_button_div.find('a')
            if first_link and first_link.get('href'):
                domain = first_link['href']
                print(f"Bulunan domain: {domain}")
                return domain
        
        # Alternatif arama yöntemi
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'selcuksports' in href or 'http' in href:
                print(f"Alternatif domain bulundu: {href}")
                return href
                
        return None
    except Exception as e:
        print(f"HTML ayrıştırma hatası: {e}")
        return None

def main():
    target_url = "https://amp-c8c5091b63.selcuksportshdamp-d2329a81bd.click/amp.html"
    proxy_url = "https://api.codetabs.com/v1/proxy/?quest="
    
    html_content = None
    
    # Önce normal erişim dene
    try:
        print("1. Normal bağlantı deneniyor...")
        response = requests.get(target_url, timeout=15)
        response.raise_for_status()
        html_content = response.text
        print("✅ Normal bağlantı başarılı!")
    except Exception as e:
        print(f"❌ Normal bağlantı başarısız: {e}")
        print("2. Proxy ile deneniyor...")
        html_content = fetch_with_proxy(target_url, proxy_url)
        if html_content:
            print("✅ Proxy bağlantısı başarılı!")
        else:
            print("❌ Her iki yöntem de başarısız oldu.")
            return
    
    # Domaini çıkar
    domain = extract_domain(html_content)
    
    if domain:
        # Domaini temizle ve formatla
        if domain.startswith('//'):
            domain = 'https:' + domain
        elif not domain.startswith('http'):
            domain = 'https://' + domain
            
        # Dosyaya yaz
        with open('selcuk_sports_guncel_domain.txt', 'w', encoding='utf-8') as f:
            f.write(f"guncel_domain={domain}")
        print(f"✅ Domain başarıyla güncellendi: {domain}")
    else:
        print("❌ HTML içeriğinden domain çıkarılamadı.")
        # Hata durumunda boş bir dosya oluştur
        with open('selcuk_sports_guncel_domain.txt', 'w', encoding='utf-8') as f:
            f.write("guncel_domain=")

if __name__ == "__main__":
    main()
