#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tree_sitter import Language, Parser
import os
import pandas as pd


lib = "build/languages.so"


if not os.path.exists(lib):
    Language.build_library(
        lib,
        [
            'tree-sitter/tree-sitter-javascript'
        ]
    )

JS_LANG = Language('build/languages.so', 'javascript')


parser = Parser()
parser.set_language(JS_LANG)



# In[2]:


# Функция для нахождения длинных переменных
def long_identifier(parent, df):

    if 'identifier' in parent.type and len(parent.text.decode()) > 31:
        # print(parent.text.decode())
        df = df.append(pd.DataFrame({'type': ['warning'],
                  'name': ['long_identifier'],
                  'start_point': [parent.start_point],
                  'end_point': [parent.end_point]}), ignore_index=True)
    for children in parent.children:
        df = long_identifier(children, df)
    return df


# In[3]:


# Функция для нахождения слишком больших блоков кода
def big_code(parent, df):

    for children in parent.children:
        for new_children in children.children:
            if new_children.type == 'identifier' and (children.end_point[0] - children.start_point[0] - 1) >= 120:
                df = df.append(pd.DataFrame({'type': ['warning'],
                  'name': ['big_code'],
                  'start_point': [new_children.start_point],
                  'end_point': [new_children.end_point]}), ignore_index=True)
    return df


# In[4]:


# Функция для нахождения синтаксических ошибок
def syntactic_error(parent, df):

    for children in parent.children:
        for new_children in children.children:
            for new_new_children in new_children.children:
                if new_new_children.has_error:
                    if new_new_children.text.find(b'\n') != -1:
                        df = df.append(pd.DataFrame({'type': ['error'],
                                        'name': ['syntax_error'],
                                        'start_point': [new_new_children.start_point],
                                        'end_point': [tuple([new_new_children.start_point[0], new_new_children.text.find(b'\n')])]}),
                                            ignore_index=True)
                    else:
                        df = df.append(pd.DataFrame({'type': ['error'],
                                            'name': ['syntax_error'],
                                            'start_point': [new_new_children.start_point],
                                            'end_point': [new_new_children.end_point]}),
                                            ignore_index=True)
    return df


# In[5]:


# Функция для нахождения слишком длинной строки
def long_row(parent, df):

    if 'identifier' in parent.type and (parent.end_point[1]) > 80:
        df = df.append(pd.DataFrame({'type': ['warning'],
                  'name': ['long_row'],
                  'start_point': [tuple([parent.start_point[0], 0])],
                  'end_point': [tuple([parent.end_point[0], 1])]}), ignore_index=True)
    for children in parent.children:
        df = long_row(children, df)
    return df


# In[6]:


# Основная функция
def find_mistakes(code):
    tree = parser.parse(bytes(code, "utf8"))
    cursor = tree.walk()

    # DataFrame with all information
    df_common = pd.DataFrame({'type': [],
                  'name': [],
                  'start_point': [],
                  'end_point': []})

    df_common = long_identifier(cursor.node, df_common)
    df_common = big_code(cursor.node, df_common)
    df_common = long_row(cursor.node, df_common)
    df_common = syntactic_error(cursor.node, df_common)

    # В некоторых случаях ошибки могут задваиваться, убираем такие строки
    df_common = df_common.drop_duplicates()

    return(df_common)


# In[7]:


find_mistakes(open('data/poor-js-code.js').read())


# In[8]:


# find_mistakes(open('data/poor-js-code.js').read()).to_json('data/first_try.json', orient='records')

