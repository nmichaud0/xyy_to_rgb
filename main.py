import streamlit as st
import pandas as pd
from conversion import xyY_to_RGB
import io


@st.cache
def convert_df(dataframe: pd.DataFrame):
    return dataframe.to_excel('converted.xlsx')


def to_excel(df_):
    output = io.BytesIO()
    writer_ = pd.ExcelWriter(output, engine='xlsxwriter')
    df_.to_excel(writer_, index=False, sheet_name='Sheet_1')
    workbook = writer_.book
    worksheet = writer_.sheets['Sheet_1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer_.save()
    return output.getvalue()


st.title('XyY to RGB Converter')

# empty space
st.write('')
st.write('')

# File requirements
st.write('File requirements:')
st.write('1. File must be in .xlsx format')
st.write('2. File must have 3 columns: X, Y, and y')
st.write('3. If file has different columns (more, less or with different names – even with spaces),'
         ' an error will be thrown')

file = st.file_uploader("Upload excel file", type=["xlsx"])

if file is not None:

    try:
        df = pd.read_excel(file)

        assert list(df.columns) == ['X', 'Y', 'y'], f'Invalid file format, columns are {list(df.columns)};' \
                                                    f' should be: ["X", "Y", "y"]'

        x_vector = df['X'].values
        y_vector = df['y'].values
        Y_vector = df['Y'].values

        R, G, B = [], [], []

        # Conversion
        for x, y, Y in zip(x_vector, y_vector, Y_vector):
            r, g, b = xyY_to_RGB(x, y, Y)
            R.append(r)
            G.append(g)
            B.append(b)

        # New DF
        RGB_df = pd.DataFrame({'R': R, 'G': G, 'B': B})

        # Download
        converted_file = to_excel(RGB_df)
        st.download_button(label='Download converted file',
                           data=converted_file,
                           file_name='converted.xlsx')

    except Exception as e:
        st.write('Error: ', e)

    st.write('File uploaded successfully')

    # empty space

