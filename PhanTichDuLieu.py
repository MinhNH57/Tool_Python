import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Tạo dữ liệu mẫu về tiền vào của công ty
data = {
    'Date': ['2025-01-01', '2025-01-05', '2025-01-10', '2025-01-15', '2025-01-20'],
    'Income Source': ['Product Sale', 'Service Fee', 'Product Sale', 'Subscription', 'Investment'],
    'Amount': [5000, 3000, 2000, 1500, 7000],
    'Description': ['Sale of product A', 'Consulting service for client X', 'Sale of product B', 
                    'Monthly subscription fee', 'Investment income from partner']
}

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data)

# Xem thông tin cơ bản về dữ liệu
print(df.info())

# Xem vài dòng đầu tiên của dữ liệu
print(df.head())

# Thống kê mô tả
print(df.describe())

# Tính tổng và trung bình của cột 'Amount'
print(f"Tổng số tiền: {df['Amount'].sum()}")
print(f"Trung bình số tiền: {df['Amount'].mean()}")

# Vẽ biểu đồ phân phối của cột 'Amount'
sns.histplot(df['Amount'])
plt.title('Distribution of Amount')
plt.show()

# Vẽ biểu đồ tương quan giữa các cột 'Amount' và 'Income Source'
sns.boxplot(x='Income Source', y='Amount', data=df)
plt.title('Income Source vs Amount')
plt.show()
