# 5학년 5반
# 채점 결과와 함께 피드백을 제공함.

# 라이브러리
import streamlit as st
from openai import OpenAI
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random
import json
import re

# API KEY, THREAD, client 생성
api_keys = st.secrets["api"]["keys"]
selected_api_key = random.choice(api_keys)
client = OpenAI(api_key=selected_api_key)
assistant_id = 'asst_2FrZmOonHQCPO6EhXzQ6u3nr'
new_thread = client.beta.threads.create()

# 화면 페이키 크기 설정
st.set_page_config(layout="wide")

# CSS 스타일을 사용하여 상단바와 메뉴 숨기기
hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 세션 상태 초기화
if 'settingname' not in st.session_state:
    st.session_state['settingname'] = ''
if 'question1' not in st.session_state:
    st.session_state['question1'] = ''
if 'question2' not in st.session_state:
    st.session_state['question2'] = ''
if 'question3' not in st.session_state:
    st.session_state['question3'] = ''
if 'question4' not in st.session_state:
    st.session_state['question4'] = ''
if 'question5' not in st.session_state:
    st.session_state['question5'] = ''
if 'correctanswer1' not in st.session_state:
    st.session_state['correctanswer1'] = ''
if 'correctanswer2' not in st.session_state:
    st.session_state['correctanswer2'] = ''
if 'correctanswer3' not in st.session_state:
    st.session_state['correctanswer3'] = ''
if 'correctanswer4' not in st.session_state:
    st.session_state['correctanswer4'] = ''
if 'correctanswer5' not in st.session_state:
    st.session_state['correctanswer5'] = ''
if 'feedbackinstruction' not in st.session_state:
    st.session_state['feedbackinstruction'] = ''
if 'sanswer1' not in st.session_state:
    st.session_state['sanswer1'] = ''
if 'sanswer2' not in st.session_state:
    st.session_state['sanswer2'] = ''
if 'sanswer3' not in st.session_state:
    st.session_state['sanswer3'] = ''
if 'sanswer4' not in st.session_state:
    st.session_state['sanswer4'] = ''
if 'sanswer5' not in st.session_state:
    st.session_state['sanswer5'] = ''
if 'feedback1' not in st.session_state:
    st.session_state['feedback1'] = ''
if 'feedback2' not in st.session_state:
    st.session_state['feedback2'] = ''
if 'feedback3' not in st.session_state:
    st.session_state['feedback3'] = ''
if 'feedback4' not in st.session_state:
    st.session_state['feedback4'] = ''
if 'feedback5' not in st.session_state:
    st.session_state['feedback5'] = ''
if 'score1' not in st.session_state:
    st.session_state['score1'] = ''
if 'score2' not in st.session_state:
    st.session_state['score2'] = ''
if 'score3' not in st.session_state:
    st.session_state['score3'] = ''
if 'score4' not in st.session_state:
    st.session_state['score4'] = ''
if 'score5' not in st.session_state:
    st.session_state['score5'] = ''
if 'name' not in st.session_state:
    st.session_state['name'] = ''

# 제작자 이름 
st.caption("이 웹 어플리케이션은 정재환(서울특별시교육청 소속 초등교사)에 의해 만들어졌습니다. 문의사항은 woghks0524jjh@gmail.com 또는 010-3393-0283으로 연락주세요.")

# 홈페이지 구성 
st.header(':100: 사람-인공지능간 채점 일치도 확인 페이지')

# 사용 방법 소개
st.subheader("1단계. 평가코드 입력하기")
st.info("평가 코드를 입력한 뒤 '평가코드 확인하기' 버튼을 눌러주세요.")

with st.container(border=True):

# Google Sheets 인증 설정
    credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"])
    gc = gspread.authorize(credentials)

# 스프레드시트 열기
    spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
    worksheet = spreadsheet.get_worksheet(7)

# 특정 설정 이름 입력
    setting_name = st.text_input("평가코드를 입력하세요.")

# 데이터 가져오기 버튼
    if st.button("평가 문항 불러오기"):

# 매번 rerun될 때마다 thread가 달라지는 것을 막기 위해 중간에 넣음.        
        st.session_state['usingthread'] = new_thread.id

# Google Sheets에서 모든 데이터 가져오기
        data = worksheet.get_all_records()

# '평가코드'를 기준으로 해당 행 찾기
        target_row = None
        for row in data:
            if row.get('settingname') == setting_name:
                target_row = row
                break

        if target_row:
        
# st.session_state에 데이터 저장
            for key, value in target_row.items():
                st.session_state[key] = value
            
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='서술형 문항을 입력하겠습니다. 서술형 문항을 정확히 이해하고, 문항에서 요구하는 내용이 무엇인지 잘 생각하기 바랍니다.'
            + '1번 문항은 <' + st.session_state['question1'] + '> 입니다.' 
            + '2번 문항은 <' + st.session_state['question2'] + '> 입니다.'
            + '3번 문항은 <' + st.session_state['question3'] + '> 입니다.'
            + '4번 문항은 <' + st.session_state['question4'] + '> 입니다.'
            + '5번 문항은 <' + st.session_state['question5'] + '> 입니다. 잘 기억하시길 바랍니다.')

            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='모범답안을 입력하겠습니다.'
            + '1번 문항 모범답안은 <' + st.session_state['correctanswer1'] + '> 입니다.' 
            + '2번 문항 모범답안은 <' + st.session_state['correctanswer2'] + '> 입니다.' 
            + '3번 문항 모범답안은 <' + st.session_state['correctanswer3'] + '> 입니다.' 
            + '4번 문항 모범답안은 <' + st.session_state['correctanswer4'] + '> 입니다.' 
            + '5번 문항 모범답안은 <' + st.session_state['correctanswer5'] + '> 입니다. 잘 기억하시길 바랍니다.')

            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='평가 주의사항을 입력하겠습니다.'
            + '평가 주의사항은 <' + st.session_state['feedbackinstruction'] + '> 입니다. 잘 기억하시길 바랍니다.')

            st.success("평가를 성공적으로 불러왔습니다.")
            
        else:
            st.warning("평가 코드에 해당하는 데이터를 찾을 수 없습니다. 평가 코드를 확인해주세요.")

# 학생 정보 입력
st.subheader("2단계. 학생 작성 답안 불러오기")
st.success("학생 작성 답안 불러오기")

with st.container(border=True):

# Google Sheets 인증 설정
    credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"])
    gc = gspread.authorize(credentials)

# 스프레드시트 열기
    spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
    worksheet = spreadsheet.get_worksheet(6)

# 특정 설정 이름 입력
    student_name = st.text_input("학생 이름을 입력하세요.")

# 데이터 가져오기 버튼
    if st.button("학생 작성 답안 불러오기"):

# Google Sheets에서 모든 데이터 가져오기
        data = worksheet.get_all_records()

# '학생 이름'을 기준으로 해당 행 찾기
        target_row = None
        for row in data:
            if row.get('name') == student_name:
                target_row = row
                break

        if target_row:
# st.session_state에 데이터 저장
            for key, value in target_row.items():
                st.session_state[key] = value

        st.success('학생 답안을 성공적으로 불러왔습니다.')

# 답안 입력 및 결과 확인
st.subheader("3단계. 채점 결과 및 피드백 확인하기")

with st.container(border=True):
    st.error("'채점 결과 및 피드백 확인하기' 버튼을 누르면 내가 작성한 답안에 대한 채점 결과와 피드백을 확인할 수 있습니다.")

# 피드백에서 1~4점 범위의 점수를 추출하는 함수
    def extract_score(feedback_text):

# "1점", "2점", "3점", "4점" 형식으로 점수를 추출하는 정규 표현식
        score_pattern = r'([1-4])점'
        match = re.search(score_pattern, feedback_text)
        
        if match:
            return int(match.group(1))
        return None

    feedback_output_button = st.button('채점 결과 및 피드백 확인하기')
    if feedback_output_button:
        if 'question1' in st.session_state and st.session_state['question1']:
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content= '1번 문항은' + st.session_state['question1'] + '입니다.' + '학생 답안은' + st.session_state['sanswer1'] + '입니다.' + '1번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id)   
                
                if run.status == "completed":
                    break

                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback1'] = thread_messages.data[0].content[0].text.value
            st.session_state['score1'] = extract_score(st.session_state['feedback1'])

        if 'question2' in st.session_state and st.session_state['question2']:
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='2번 문항은' + st.session_state['question2'] + '입니다.' + '학생 답안은' + st.session_state['sanswer2'] + '입니다.' + '2번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id)
                
                if run.status == "completed":
                    break

                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback2'] = thread_messages.data[0].content[0].text.value
            st.session_state['score2'] = extract_score(st.session_state['feedback2'])

        if 'question3' in st.session_state and st.session_state['question3']:
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='3번 문항은' + st.session_state['question3'] + '입니다.' + '학생 답안은' + st.session_state['sanswer3'] + '입니다.' + '3번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id)   
                
                if run.status == "completed":
                    break

                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback3'] = thread_messages.data[0].content[0].text.value
            st.session_state['score3'] = extract_score(st.session_state['feedback3'])

        if 'question3' in st.session_state and st.session_state['question4']:
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='4번 문항은' + st.session_state['question4'] + '입니다.' + '학생 답안은' + st.session_state['sanswer4'] + '입니다.' + '3번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id)   
                
                if run.status == "completed":
                    break

                else:
                    time.sleep(2)    
           
            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback4'] = thread_messages.data[0].content[0].text.value
            st.session_state['score4'] = extract_score(st.session_state['feedback4'])

        if 'question3' in st.session_state and st.session_state['question5']:
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='5번 문항은' + st.session_state['question5'] + '입니다.' + '학생 답안은' + st.session_state['sanswer5'] + '입니다.' + '3번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id)   
                
                if run.status == "completed":
                    break

                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            st.session_state['feedback5'] = thread_messages.data[0].content[0].text.value
            st.session_state['score5'] = extract_score(st.session_state['feedback5'])

# 채점 결과 보이기
        st.write(st.session_state['feedback1'])
        st.divider()
        st.write(st.session_state['feedback2'])
        st.divider()
        st.write(st.session_state['feedback3'])
        st.divider()
        st.write(st.session_state['feedback4'])
        st.divider()
        st.write(st.session_state['feedback5'])

# 자동 저장 기능
with st.container(border=True):
    st.error("마지막으로 '서술형 평가 연습 결과 저장하기' 버튼을 누르면 결과가 저장됩니다.")

    saveresult = st.button("서술형 평가 연습 결과 저장하기")
    if saveresult:

# 구글 시트 열기
# Google Sheets 인증 설정
        credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"])
        gc = gspread.authorize(credentials)

# 스프레드시트 열기
        spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
        worksheet = spreadsheet.get_worksheet(6)

# 저장하기
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 6칸을 빈 칸으로 채우기
        empty_cells = [""] * 6

# 점수와 피드백을 st.session_state에서 가져오기
        score_feedback_data = [
            st.session_state['score1'], st.session_state['score2'], st.session_state['score3'],
            st.session_state['score4'], st.session_state['score5'],
            st.session_state['feedback1'], st.session_state['feedback2'], st.session_state['feedback3'],
            st.session_state['feedback4'], st.session_state['feedback5']]

# 데이터를 추가 (6칸 빈칸 + 점수 + 피드백)
        worksheet.append_row(empty_cells + score_feedback_data)

        st.success('서술형 평가 연습 결과가 성공적으로 저장되었습니다.')