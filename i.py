import requests
from bs4 import BeautifulSoup
import random
# Hàm để lấy danh sách doanh nghiệp từ một trang web với địa chỉ chứa từ khoá mà bạn chỉ định
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
]
def get_businesses_from_page(url, keyword):
    try:
        headers = {
        'User-Agent': random.choice(user_agents)
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            businesses = soup.find_all('div', class_='search-results')
            filtered_businesses = []
            for business in businesses:
                address_tag = business.find('p')
                address_text = address_tag.get_text().strip()
                lines = address_text.splitlines()
                if len(lines) > 1:
                    address_line = lines[1].strip()
                if address_line and keyword.lower() in address_line.lower():
                    filtered_businesses.append(business)
            return len(filtered_businesses)
        else:
            print(f'Không thể truy cập trang web: {url} - Mã trạng thái: {response.status_code}')
            return 0
    except requests.exceptions.RequestException as e:
        print(f'Không thể truy cập trang web: {url} - Lỗi: {e}')
        return 0

# URL của trang web
Base_url = "https://www.tratencongty.com/thanh-pho-ha-noi/huyen-thach-that/xa-phung-xa/?page="

# Từ khoá để tìm kiếm trong địa chỉ
print("Nhập vào địa chỉ mà cần tìm kiếm :")
keyword = input()
num_businesses = 0
for i in range(13):
    url = Base_url + str(i)
    num = get_businesses_from_page(url, keyword)
    num_businesses += num


print(f'Số lượng doanh nghiệp có tên chứa từ khoá "{keyword}": {num_businesses}')
