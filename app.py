import streamlit as st
import pandas as pd

# import class CsvProcessor
from csv_processor import DataProcessor
st.set_option('deprecation.showPyplotGlobalUse', False)
def main():
    st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📊")
    # Memuat file CSS
    st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

    data_processor = DataProcessor()
    # menambahkan header 1
    st.header('Exploratory Data Analysis Dashboard')

    # menambahkan tombol untuk upload file
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

    # menambahkan selectbox untuk memilih delimiter
    delimiter_options = [",", ";", "|", "\t", " "]
    delimiter = st.selectbox("Pilih delimiter yang digunakan dalam file CSV", delimiter_options, index=0)

    st.sidebar.header('Exploratory Data Analysis Dashboard')

    # inisialisasi variabel data_processor jika file sudah diupload dan tombol submit ditekan
    if uploaded_file is not None:
        data_processor.load_data(uploaded_file, delimiter)

        menu = ["Informasi Umum", "Statistika Deskriptif", "Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"]
        choice = st.sidebar.radio("Pilih Menu", menu)

        if choice == "Informasi Umum":
            st.subheader("Informasi Umum")
            # menampilkan head dan info
            data_processor.show_head()

            # menampilkan missing value
            data_processor.show_missing_value()

            # menampilkan informasi data duplicate
            data_processor.show_duplicate()
        
        elif choice == "Statistika Deskriptif":
            st.subheader("Statistika Deskriptif")
            # menampilkan statistika descriptive
            data_processor.show_descriptive_statistics()

        elif choice == "Univariate Analysis":
            st.subheader("Univariate Analysis")
            columns = list(data_processor.data.columns)
            selected_column = st.selectbox('Select a column', columns)
            data_processor.set_color()
            data_processor.plot_univariate(selected_column)
        
        elif choice== "Bivariate Analysis":
            st.subheader("Bivariate Analysis")
            columns = list(data_processor.data.columns)
            columns.insert(0, None)
            x_ax = st.selectbox('Select a column for x axis',  columns)
            try:
                if  pd.api.types.is_numeric_dtype(data_processor.data[x_ax]):
                    try:
                        y_ax = st.selectbox('Select a column for y axis',  columns)
                        hue_plot = st.selectbox('Select a column for hue (optional)',  columns)
                        data_processor.plot_bivariate(x_ax, y_ax, hue_plot)
                    except:
                        st.warning("Anda belum memilih y axis")
                else:
                    hue_plot = st.selectbox('Select a column for hue (optional)',  columns)
                    data_processor.plot_bivariate(x_ax, y_axis=None, hue=hue_plot)
            except:
                st.warning("Anda belum memilih axis")

        else:
            st.subheader("Multivariate Analysis")
            data_processor.multivariate_analysis()


if __name__ == "__main__":
    main()

