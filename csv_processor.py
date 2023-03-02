import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io
from scipy import stats
import numpy as np

class DataProcessor:
    def __init__(self):
        self.data = None
        self.selected_column = None
        self.plot_color = '#FF4B4B'
        
    def set_color(self):
        self.plot_color = st.color_picker('Select plot color', self.plot_color)
    
    # load data
    def load_data(self, file, delimiter):
        try:
            if file is not None:
                if file.type == "application/vnd.ms-excel":
                    self.data = pd.read_excel(file, engine="openpyxl", header=0)
                else:
                    self.data = pd.read_csv(file, header=0, delimiter=delimiter)
                st.success("Data berhasil diunggah!")
            else:
                st.warning("Data gagal dimuat. Silakan upload file CSV atau Excel.")
        except Exception as e:
            st.error("Terjadi kesalahan dalam memuat data: {}".format(str(e)))

    # menampilkan head data
    def show_head(self):
        if self.data is not None:
            st.write("#### Head Data")
            st.write(self.data.head())
            st.write("#### Info Data Type")
            buffer = io.StringIO()
            self.data.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)
        else:
            st.warning("Data belum dimuat.")
    
    # menampilkan missing value
    def show_missing_value(self):
        if self.data is not None:
            st.write("#### Missing Value")
            missing_values = self.data.isnull().sum()
            missing_cols = list(missing_values[missing_values > 0].index)
            if len(missing_cols) > 0:
                fig = px.bar(x=missing_values[missing_values > 0].index, y=missing_values[missing_values > 0], labels={
                    "x": "Kolom",
                    "y": "Jumlah Missing Value"
                })
                st.plotly_chart(fig)
                st.write("Kolom dengan missing value:")
                st.write(", ".join(missing_cols))
            else:
                st.write("Tidak ada kolom dengan missing value.")
        else:
            st.warning("Data belum dimuat.")
    
    def show_duplicate(self):
        if self.data is not None:
            st.write("#### Data Duplicate")
            duplicate_rows = self.data.duplicated()
            duplicate_count = duplicate_rows.sum()
            if duplicate_count > 0:
                st.write("Jumlah baris data duplicate: {}".format(duplicate_count))
            else:
                st.write("Tidak ada data duplicate.")
        else:
            st.warning("Data belum dimuat.")
    

    def show_descriptive_statistics(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=["int64", "float64"]).columns.tolist()
            datetime_cols = self.data.select_dtypes(include=["datetime64"]).columns.tolist()
            categorical_cols = self.data.select_dtypes(include=["object"]).columns.tolist()

            if len(numeric_cols) > 0:
                st.write("Kolom Numerik")
                st.write(self.data[numeric_cols].describe())

            if len(datetime_cols) > 0:
                st.write("Kolom Tanggal/Waktu")
                st.write(self.data[datetime_cols].describe())

            if len(categorical_cols) > 0:
                st.write("Kolom Kategori")
                st.write(self.data[categorical_cols].describe())

        else:
            st.warning("Data belum dimuat.")


    def plot_univariate(self, column):
        if self.data is not None:
            if pd.api.types.is_numeric_dtype(self.data[column]):
                try:
                    unique_values = self.data[column].value_counts()
                    unique_df = pd.concat([unique_values.rename("jumlah"), (unique_values/unique_values.sum()*100).rename("persentase")], axis=1)
                    unique_df.index.name = column
                    st.write("Unique values in column '{}':".format(column))
                    st.write(unique_df)
                    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))
                    sns.kdeplot(self.data[column], color=self.plot_color, ax=ax1)
                    sns.boxplot(self.data[column], color=self.plot_color, ax=ax2)
                    st.pyplot(fig)
                except:
                    st.warning("Data kolom {} tidak dapat diubah menjadi numerik. Silakan pilih kolom lain".format(column))
            elif pd.api.types.is_categorical_dtype(self.data[column]) or pd.api.types.is_object_dtype(self.data[column]):
                try:
                    unique_values = self.data[column].value_counts()
                    unique_df = pd.concat([unique_values.rename("jumlah"), (unique_values/unique_values.sum()*100).rename("persentase")], axis=1)
                    unique_df.index.name = column
                    st.write("Unique values in column '{}':".format(column))
                    st.write(unique_df)
                    fig, ax = plt.subplots()
                    sns.countplot(x=column, data=self.data, color=self.plot_color, ax=ax)
                    st.pyplot(fig)
                except:
                    st.warning("Data kolom {} tidak dapat ditampilkan. Silakan pilih kolom lain".format(column))
            else:
                st.warning("Data kolom {} tidak dapat ditampilkan. Silakan pilih kolom lain".format(column))
        else:
            st.warning("Data belum dimuat.")

    def plot_bivariate(self, x_axis=None, y_axis=None, hue=None):
        if self.data is not None:
            # if x_axis is not None and y_axis is not None:
            if pd.api.types.is_numeric_dtype(self.data[x_axis]) and pd.api.types.is_numeric_dtype(self.data[y_axis]):
                try:
                    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(12, 6))
                    sns.scatterplot(x=x_axis, y=y_axis, hue=hue, data=self.data, ax=ax1)
                    sns.kdeplot(x=self.data[x_axis], hue=self.data[hue], fill=True, alpha=.4, ax=ax2)
                    sns.kdeplot(x=self.data[y_axis], hue=self.data[hue], fill=True, alpha=.4, ax=ax3)
                    st.pyplot(fig)
                except:
                    st.warning("Gagal membuat plot. Silakan periksa kembali nama kolom yang dimasukkan.")
            elif pd.api.types.is_categorical_dtype(self.data[x_axis]) or pd.api.types.is_object_dtype(self.data[x_axis]):
                try:
                    fig, ax = plt.subplots()
                    sns.countplot(x=x_axis, data=self.data, hue=hue, ax=ax)
                    st.pyplot(fig)
                except:
                    st.warning("Gagal membuat plot. Silakan periksa kembali nama kolom yang dimasukkan.")
            else:
                st.warning("Kolom yang dipilih bukan merupakan kolom numerik.")
        # else:
        #     st.warning("Mohon pilih kolom untuk sumbu x dan sumbu y.")
        else:
            st.warning("Data belum dimuat.")
      
    def multivariate_analysis(self):
        if self.data is not None:    
            # Correlation matrix
            st.write('Matrik Korelasi:')
            st.write(self.data.corr())
            sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm')
            st.pyplot()
    
            # Pairplot
            st.write('Pairplot:')
            sns.pairplot(self.data)
            st.pyplot()
    
            # Outlier detection
            st.write('Deteksi Outlier Menggunakan Z-Score:')
            outlier_dict = {}
            for col in self.data.columns:
                if self.data[col].dtype != 'object':
                    z_score = np.abs(stats.zscore(self.data[col]))
                    outliers = self.data.loc[z_score > 3, col]
                    outlier_dict[col] = len(outliers)
    
            outlier_df = pd.DataFrame.from_dict(outlier_dict, orient='index', columns=['Jumlah outliers'])
            outlier_df = outlier_df.sort_values(by='Jumlah outliers', ascending=False)
            st.write(outlier_df)
        else:
            st.warning("Data belum dimuat.")
