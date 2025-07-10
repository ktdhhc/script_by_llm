#!/usr/bin/python 3.10

import streamlit as st
import pandas as pd
from apply import get_script

# 初始化会话状态
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = {
        'title': None,
        'script': None,
        'wiki': None
    }

st.title('视频脚本生成器')
st.divider()

with st.sidebar:
    model_name = st.selectbox('请选择模型', ['Chat_GPT', 'DeepSeek'])
    online = st.checkbox('联网搜索（需要🎢）')
    st.divider()

    api_key = st.text_input('请输入api：', type='password')
    # st.markdown('[获取OpenAI api密钥](https://platform.openai.com/account/api-keys)')

subject = st.text_input('请输入主题词：')

duration = st.number_input('请输入视频大致时长（分钟）', min_value=0.1, step=0.1)

creativity = st.slider('请输入创造力（越大代表越丰富)', min_value=0.0, max_value=1.0, value=0.2, step=0.1)

submitted = st.button('生成脚本')
# if submitted:
#     st.write('提交成功')


if submitted:
    if not api_key:
        st.info('请先输入api')
        st.stop()
    elif not subject:
        st.info('请输入主题词')
        st.stop()
    elif not duration >= 0.1:
        st.info('视频长度需要大于或等于0.1')
        st.stop()
    else:
        with st.spinner(('ai正在思考，请稍等...')):
            wiki, title, script = get_script(subject, duration, creativity, api_key, model_name, fetch_online=online)
            # 将生成的内容保存到会话状态
            st.session_state.generated_data = {
                'title': title,
                'script': script,
                'wiki': wiki
            }
        st.success('视频脚本已生成！')
# 显示之前生成的内容（如果有）
if st.session_state.generated_data['title']:
    st.divider()
    st.subheader('标题：')
    st.write(st.session_state.generated_data['title'])
    st.subheader('视频脚本：')
    st.write(st.session_state.generated_data['script'])
    with st.expander('搜索结果'):
        st.info(st.session_state.generated_data['wiki'])
    