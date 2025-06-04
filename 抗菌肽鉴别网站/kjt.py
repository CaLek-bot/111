# 文件名：app.py
import streamlit as st
import pandas as pd
from Bio import SeqIO
import io
import re


def is_amp(sequence):
    # 示例判断逻辑（可替换为模型预测）
    # 真实项目中应使用训练好的分类器
    return len(sequence) < 50 and ('K' in sequence or 'R' in sequence)


def analyze_csv(file):
    df = pd.read_csv(file)
    if 'sequence' not in df.columns:
        return None, "CSV文件中必须包含'sequence'列"

    df['is_AMP'] = df['sequence'].apply(is_amp)
    return df, None


def analyze_fasta(file):
    fasta_sequences = SeqIO.parse(io.StringIO(file.getvalue().decode("utf-8")), 'fasta')
    results = []
    for record in fasta_sequences:
        seq = str(record.seq)
        results.append({
            'id': record.id,
            'sequence': seq,
            'is_AMP': is_amp(seq)
        })
    return pd.DataFrame(results), None


st.title("抗菌肽识别网站")

uploaded_file = st.file_uploader("上传一个CSV或FASTA文件", type=['csv', 'fasta'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df, error = analyze_csv(uploaded_file)
    elif uploaded_file.name.endswith('.fasta'):
        df, error = analyze_fasta(uploaded_file)
    else:
        df, error = None, "文件格式不支持"

    if error:
        st.error(error)
    elif df is not None:
        st.success("分析完成！以下是识别结果：")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "下载结果CSV",
            data=csv,
            file_name="AMP_results.csv",
            mime='text/csv',
        )
