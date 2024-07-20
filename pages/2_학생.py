# 라이브러리
import streamlit as st
from openai import OpenAI
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# 사이드바에 학생 페이지 콘텐츠 추가
st.sidebar.title("학생 페이지")

# 환경 변수에서 Google Cloud Credentials 로드
google_cloud_credentials_json = os.getenv("GOOGLE_CLOUD_CREDENTIALS_JSON")

# 문자열로 변환 (이미 문자열인 경우에도 문제가 없음)
if google_cloud_credentials_json:
    google_cloud_credentials_dict = json.loads(str(google_cloud_credentials_json))
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_cloud_credentials_dict)

# API KEY, THREAD, client 생성
api_key = st.session_state['usingapikey']
thread_id = st.session_state['usingthread']
client = OpenAI(api_key=st.session_state['usingapikey'])
assistant_id = 'asst_eVdrs48UPW5pD4sh4XA8Qkto'

# 홈페이지 구성 
st.subheader('초등학교 사회 5학년 2학기 서술형 평가 연습 도구')

# 사용 방법 소개
with st.container(border=True):
    st.write(
"""
<사용 방법>

1. [학생 정보 입력]에서 반, 번호, 이름을 입력합니다.
    
2. [답안 입력 및 결과 확인]에서 학생 답안을 입력하고, 학생 답안에 대한 채점 및 피드백을 확인합니다. 마지막으로 학생 의견을 입력할 수 있습니다. 
- 학생 의견에는 채점 및 피드백 결과에 대한 생각, 전체적인 생각 또는 느낀 점을 자유롭게 서술할 수 있습니다.
""")
   


# 탭설정
tab1, tab2 = st.tabs(["1. 학생 정보 입력", "2. 답안 입력 및 결과 확인"])

# 탭1: 학생 정보 입력
# 단원에 따라 assistant ID 변경(미리 입력한 파일이 다름. 이유는 가볍게 만들기 위해, 아래 어시스턴트 아이디 다르게 해야함.)
with tab1:
    st.subheader("1. 학생 정보 입력")
    studentclass = st.text_input("반")
    studentnumber = st.text_input("번호")
    studentname = st.text_input("이름")

    st.session_state['studentclass'] = studentclass
    st.session_state['studentnumber'] = studentnumber
    st.session_state['studentname'] = studentname

# 탭2: 답안 입력 및 결과 확인
with tab2:
    st.subheader("2. 답안 입력 및 결과 확인")

    with st.container(border=True):
        st.caption("답안 입력")
        answer1 = st.text_area("1번 문항: " + st.session_state['question1'], height=100)
        answer2 = st.text_area("2번 문항: " + st.session_state['question2'], height=100)
        answer3 = st.text_area("3번 문항: " + st.session_state['question3'], height=100)

# 문항 등록
        answer_input_button = st.button('답안 등록')
        if answer1 is not None:
            st.session_state['answer1'] = answer1
        if answer2 is not None:
            st.session_state['answer2'] = answer2
        if answer3 is not None:
            st.session_state['answer3'] = answer3

        if answer_input_button:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='1번 문항에 대한 학생 답안은 <' + answer1 + 
            '> 입니다. 2번 문항에 대한 학생 답안은 <' + answer2 + 
            '> 입니다. 3번 문항에 대한 학생 답안은 <' + answer3 +'> 입니다.'
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id
                )

            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            st.success(f'학생 답안이 성공적으로 등록되었습니다.')

#채점 및 피드백 생성 
    with st.container(border=True):
        st.caption("채점 및 피드백 결과 확인")
        feedback_output_button = st.button('채점 및 피드백 생성')
        if feedback_output_button:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='1번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. 평가 문항, 학생 답안, 채점 결과 및 피드백이 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다.'
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id
            )

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback1'] = thread_messages.data[0].content[0].text.value

            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='2번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. 평가 문항, 학생 답안, 채점 결과 및 피드백이 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다.'
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id
            )

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback2'] = thread_messages.data[0].content[0].text.value

            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='3번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. 평가 문항, 학생 답안, 채점 결과 및 피드백이 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다.'
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id
            )

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback3'] = thread_messages.data[0].content[0].text.value

            st.write(st.session_state['feedback1'])
            st.write(st.session_state['feedback2'])
            st.write(st.session_state['feedback3'])



# 학생 의견 작성 
    with st.container(border=True):
        st.caption("학생 의견 입력")
        studentopinion = st.text_area("채점 및 피드백 결과에 대한 의견을 적어주세요. 결과에 대해 궁금한 점이나 이해가 가지 않는 부분, 혹은 단순한 소감이나 느낀점도 좋습니다.")
        studentopinionbutton = st.button("의견 등록")
        if studentopinionbutton:
            st.session_state['studentopinion'] = studentopinion
            st.success(f'학생 의견이 성공적으로 등록되었습니다.')

# 자동 저장 기능
    saveresult = st.button("결과 저장")
    if saveresult:

# 구글 시트 열기
# Google Sheets 인증 설정
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\streamlit/240509/m20223715-403a2aed16a4.json', scope)
        gc = gspread.authorize(credentials)

# 스프레드시트 열기
        spreadsheet = gc.open('서술형 평가 결과 기록')
        worksheet = spreadsheet.sheet1  # 첫 번째 시트 선택

# 저장하기
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([current_time, st.session_state['studentclass'], st.session_state['studentnumber'], st.session_state['studentname'], st.session_state['answer1'], st.session_state['feedback1'], st.session_state['answer2'], st.session_state['feedback2'], st.session_state['answer3'], st.session_state['feedback3'], st.session_state['studentopinion']])
        st.success(f'결과가 성공적으로 Google Sheets에 저장되었습니다.')
