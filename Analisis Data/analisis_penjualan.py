import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# =========================
# MEMBACA DATA
# =========================
df = pd.read_csv('data_praktikum_analisis_data.csv')

# Konversi kolom tanggal
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

print("Data Awal:")
print(df.head())


# =========================
# DATA CLEANING
# =========================
print("\nInformasi Data:")
print(df.info())

print("\nJumlah Data Kosong:")
print(df.isnull().sum())

# (Opsional) Jika ingin memastikan tidak ada nilai negatif
df = df[df['Total_Sales'] > 0]


# =========================
# TREN PENJUALAN BULANAN
# =========================
df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
penjualan_bulanan = df.groupby('Month')['Total_Sales'].sum()

plt.figure(figsize=(10, 5))
plt.plot(penjualan_bulanan.index, penjualan_bulanan.values, marker='o')
plt.title('Tren Penjualan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Total Penjualan')
plt.xticks(rotation=45)
plt.show()


# =========================
# ANALISIS PRODUK (ADAPTASI DATA)
# =========================
analisis_produk = df.groupby('Product_Category')['Total_Sales'].sum().reset_index()

plt.figure(figsize=(8, 5))
plt.scatter(analisis_produk['Total_Sales'], analisis_produk['Total_Sales'])
plt.xlabel("Total Penjualan")
plt.ylabel("Total Penjualan")
plt.title("Analisis Penjualan per Kategori Produk")
plt.show()


# =========================
# RFM ANALYSIS
# =========================
tanggal_acuan = df['Order_Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'Order_Date': lambda x: (tanggal_acuan - x.max()).days,
    'Order_ID': 'count',
    'Total_Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RFM_Group'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

print("\nHasil Analisis RFM:")
print(rfm.head())


# =========================
# ANALISIS KATEGORI (PENGGANTI GEOGRAFIS)
# =========================
analisis_kategori = df.groupby('Product_Category')['Total_Sales'].sum().sort_values()

plt.figure(figsize=(8, 5))
analisis_kategori.plot(kind='barh')
plt.title("Total Penjualan per Kategori Produk")
plt.xlabel("Total Penjualan")
plt.ylabel("Kategori Produk")
plt.show()


# =========================
# ANALISIS HIPOTESIS (ADAPTASI IKLAN)
# =========================
rata_iklan = df['Ad_Budget'].mean()

iklan_tinggi = df[df['Ad_Budget'] > rata_iklan]
iklan_rendah = df[df['Ad_Budget'] <= rata_iklan]

print("\nRata-rata Penjualan (Iklan Tinggi):", iklan_tinggi['Total_Sales'].mean())
print("Rata-rata Penjualan (Iklan Rendah):", iklan_rendah['Total_Sales'].mean())


# =========================
# HEATMAP KORELASI
# =========================
plt.figure(figsize=(6, 4))
korelasi = df[['Total_Sales', 'Ad_Budget']].corr()

sns.heatmap(korelasi, annot=True, cmap='coolwarm')
plt.title("Peta Korelasi Antar Variabel")
plt.show()


# =========================
# REGRESI LINEAR
# =========================
X = df[['Ad_Budget']]
y = df['Total_Sales']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print("\nKoefisien Iklan:", model.coef_[0])
print("Akurasi Model (R2 Score):", model.score(X_test, y_test))


# =========================
# VISUALISASI TAMBAHAN
# =========================
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Ad_Budget', y='Total_Sales', data=df)
plt.title("Hubungan Anggaran Iklan dan Total Penjualan")
plt.xlabel("Anggaran Iklan")
plt.ylabel("Total Penjualan")
plt.show()