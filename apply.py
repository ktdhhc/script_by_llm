#!/usr/bin/python 3.10

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_community.utilities import WikipediaAPIWrapper

def get_script(subject, video_length, creativity, api_key, chat_model='Chat_GPT', fetch_online=False):
    if chat_model == 'DeepSeek':
        model = ChatDeepSeek(model='deepseek-chat',
                            api_key = api_key,
                            temperature = creativity)
    elif chat_model == 'Chat_GPT':
        model = ChatOpenAI(model="gpt-3.5-turbo", 
                            openai_api_key = api_key,
                            openai_api_base = "https://api.aigc369.com/v1",
                            temperature = creativity)

    title_template = ChatPromptTemplate.from_messages({
        ("human", "要求：请为'{subject}'这个主题的视频想一个吸引人的标题。请严格按照要求输出内容，不需要多余回复语")
    })

    script_template = ChatPromptTemplate.from_messages({
        ("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
                    视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
                    要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
                    整体内容的表达方式要尽量轻松有趣，吸引年轻人。
                    脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
                    ```{wikipedia_search}```""")
    })

    title_prompt = title_template.invoke({'subject': subject})
    title = model.invoke(title_prompt)

    if fetch_online:
        search = WikipediaAPIWrapper(lang="zh")
        wiki_result = search.run(subject)
        wiki = wiki_result
    else:
        wiki_result = '0'
        wiki = '暂无内容'

    script_prompt = script_template.invoke({'title': title,
                                            'duration': video_length,
                                            'wikipedia_search': wiki_result})
    script = model.invoke(script_prompt)


    return wiki, title.content, script.content


# title, script = get_script('灵笼', 1, 1, os.getenv("OPENAI_API_KEY"), chat_model='gpt')

# print(wiki_result, title, script)
