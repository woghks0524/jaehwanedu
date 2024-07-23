# # 라이브러리
# import streamlit as st
# from openai import OpenAI
# import random

# # 사이드바에 메인 페이지 콘텐츠 추가
# st.sidebar.title("사전 설정")

# # API 키 리스트
# api_keys = st.secrets["api"]["keys"]

# # assistant_id 등록 
# assistant_id = 'asst_t0CtEvNce3uo8pMqY4BjLY78'

# # API KEY 생성 기본 세팅
# st.session_state['APIKEYon/off'] = False
# st.session_state['THREADon/off'] = False

# # [[사전 설정]] 페이지 사용 방법 소개
# with st.container(border=True):
#     st.write(
# """
# [[사전 설정]] 페이지 사용 방법

# 1. 'API KEY 생성하기' 버튼을 클릭합니다. 클릭했을 때 나타나는 'sk'로 시작하는 API KEY를 전부 복사하여 아래 빈칸에 붙여넣습니다.
    
# 2. 'THREAD 생성하기' 버튼을 클릭합니다. 클릭했을 때 나타나는 'thread'로 시작하는 THREAD를 전부 복사하여 아래 빈칸에 붙여넣습니다.

# 3. [[서술형 평가 문항 설정]] 페이지에 접근할 수 있는 비밀번호를 만듭니다. 비밀번호를 만든 후에는 '비밀번호 등록하기' 버튼을 클릭합니다.
# """)

# # API KEY 생성 버튼
# if st.button("API KEY 생성하기"):
#     st.session_state['APIKEYon/off'] = True

# # 조건에 따라 API KEY 생성
# if st.session_state['APIKEYon/off'] == True:

# # 임의의 API KEY 선택
#     selected_api_key = random.choice(api_keys)
#     st.write(selected_api_key)

# # 글로벌 함수로 API KEY 입력
# usingapikey = st.text_input("선택된 API KEY를 복사하여 넣어주세요.")
# st.session_state['usingapikey'] = usingapikey
# st.session_state['APIKEYon/off'] = False
# api_key = usingapikey

# if usingapikey:
#     # client 생성 
#     client = OpenAI(api_key=st.session_state['usingapikey'])

#     # thread 생성
#     new_thread = client.beta.threads.create()

# # THREAD 생성 버튼
# if st.button("THREAD 생성하기"):
#     st.session_state['THREADon/off'] = True
#     st.write(new_thread.id)

# usingthread = st.text_input("생성된 THREAD를 복사하여 넣어주세요.")

# # 글로벌 함수로 Thread 입력
# st.session_state['usingthread'] = usingthread
# thread_id = usingthread

# # 비밀번호 설정하기
# passwordsettingbutton = st.button("비밀번호 등록하기")
# passwordsetting = st.text_input("[[서술형 평가 문항 설정]] 페이지 접근을 위한 비밀번호를 만들어주세요.")
# if passwordsettingbutton:
#     st.session_state['passwordsetting'] = passwordsetting