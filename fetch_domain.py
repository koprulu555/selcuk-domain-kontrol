import requests
from bs4 import BeautifulSoup

def main():
    target_url = "https://amp-c8c5091b63.selcuksportshdamp-d2329a81bd.click/amp.html"
    proxy_url = "https://api.codetabs.com/v1/proxy/?quest="
    
    html_content = None
    
    try:
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        print("Normal bağlantı başarılı")
    except:
        try:
            response = requests.get(f"{proxy_url}{target_url}", timeout=10)
            response.raise_for_status()
            html_content = response.text
            print("Proxy bağlantısı başarılı")
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        target_div = soup.find('div', class_='mobile-button-container mobile')
        
        if target_div:
            first_link = target_div.find('a')
            if first_link and first_link.get('href'):
                domain = first_link['href']
                
                with open('selcuk_sports_guncel_domain.txt', 'w') as f:
                    f.write(f"guncel_domain={domain}")
                print(f"Domain yazıldı: {domain}")
                return
        
        print("Domain bulunamadı")
        with open('selcuk_sports_guncel_domain.txt', 'w') as f:
            f.write("guncel_domain=")
            
    except Exception as e:
        print(f"Hata: {e}")
        with open('selcuk_sports_guncel_domain.txt', 'w') as f:
            f.write("guncel_domain=")

if __name__ == "__main__":
    main()
