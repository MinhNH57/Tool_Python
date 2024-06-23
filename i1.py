import requests
from bs4 import BeautifulSoup

# Hàm để lấy danh sách doanh nghiệp từ một trang web với địa chỉ chứa từ khoá mà bạn chỉ định
def get_businesses_from_page(url, keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            businesses = soup.find_all('div', class_='search-results')
            filtered_businesses = []
            for business in businesses:
                address_tag = business.find('a')
                if address_tag and keyword.lower() in address_tag.text.lower():
                    address_p = business.find('p')
                    if address_p:
                        # Thay thế các thẻ <br> bằng dấu xuống dòng để dễ đọc hơn
                        address_text = address_p.get_text(separator='\n').strip()
                        # Tách từng dòng trong thẻ <p>
                        address_lines = address_text.split('\n')
                        # Lấy dòng cuối cùng trong thẻ <p> là địa chỉ
                        if address_lines:
                            address = address_lines[-1].strip()
                            filtered_businesses.append(address)
            return filtered_businesses
        else:
            print(f'Không thể truy cập trang web: {url} - Mã trạng thái: {response.status_code}')
            return []
    except requests.exceptions.RequestException as e:
        print(f'Không thể truy cập trang web: {url} - Lỗi: {e}')
        return []

# URL của trang web
url = "https://www.tratencongty.com/thanh-pho-ha-noi/huyen-thach-that/?page=13"

# Từ khoá để tìm kiếm trong tên công ty
keyword = "Thép"

# Lấy danh sách địa chỉ doanh nghiệp từ trang với tên công ty chứa từ khoá
addresses = get_businesses_from_page(url, keyword)

# In danh sách địa chỉ doanh nghiệp tìm thấy
for address in addresses:
    print(address)
