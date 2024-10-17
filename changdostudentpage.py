# 5학년 5반
# 채점 결과와 피드백을 함께 제공함.

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

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 0
if 'settingname' not in st.session_state:
    st.session_state['settingname'] = ''
if 'question1' not in st.session_state:
    st.session_state['question1'] = ''
if 'question2' not in st.session_state:
    st.session_state['question2'] = ''
if 'question3' not in st.session_state:
    st.session_state['question3'] = ''
if 'correctanswer1' not in st.session_state:
    st.session_state['correctanswer1'] = ''
if 'correctanswer2' not in st.session_state:
    st.session_state['correctanswer2'] = ''
if 'correctanswer3' not in st.session_state:
    st.session_state['correctanswer3'] = ''
if 'feedbackinstruction' not in st.session_state:
    st.session_state['feedbackinstruction'] = ''
if 'studentclass' not in st.session_state:
    st.session_state['studentclass'] = ''
if 'studentnumber' not in st.session_state:
    st.session_state['studentnumber'] = ''
if 'studentname' not in st.session_state:
    st.session_state['studentname'] = ''
if 'answer1' not in st.session_state:
    st.session_state['answer1'] = ''
if 'answer2' not in st.session_state:
    st.session_state['answer2'] = ''
if 'answer3' not in st.session_state:
    st.session_state['answer3'] = ''
if 'feedback1' not in st.session_state:
    st.session_state['feedback1'] = ''
if 'feedback2' not in st.session_state:
    st.session_state['feedback2'] = ''
if 'feedback3' not in st.session_state:
    st.session_state['feedback3'] = ''
if 'studentopinion1' not in st.session_state:
    st.session_state['studentopinion1'] = ''
if 'studentopinion2' not in st.session_state:
    st.session_state['studentopinion2'] = ''
if 'score1' not in st.session_state:
    st.session_state['score1'] = ''
if 'score2' not in st.session_state:
    st.session_state['score2'] = ''
if 'score3' not in st.session_state:
    st.session_state['score3'] = ''
if 'openclose' not in st.session_state:
    st.session_state['openclose'] = 'open'

# 페이지 전환 함수 정의
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_home():
    st.session_state.page = 0

# 홈페이지 구성 
st.header(':100: 사회 5학년 2학기 서술형 평가 연습(5반)')

# 사용 방법 소개
def home():
    with st.container(border=True):
        st.write("""
        학생 페이지 사용 방법
                    
        총 3단계로 이루어져 있습니다. 차례대로 다음 단계로 넘어가주세요.""")

        st.info("""1. [평가 코드 입력하기]:           
- 선생님이 알려주신 평가 코드를 입력한 뒤 '평가 코드 확인하기' 버튼을 눌러주세요.
- 평가 코드를 입력해야 다음 단계로 넘어갈 수 있습니다.""")
                    
        st.success("""2. [정보 입력하기]:           
- 반, 번호, 이름을 입력한 뒤 '학생 정보 등록하기' 버튼을 눌러주세요. 
- 정보를 입력해야 다음 단계로 넘어갈 수 있습니다.""")

        st.error("""3. [답안 작성 및 결과 확인하기]:            
- 서술형 문항을 잘 읽고 답안을 작성하세요.
- 답안을 작성한 뒤 '작성 답안 등록하기' 버튼을 눌러주세요.         
- '채점 결과 및 피드백 확인하기' 버튼을 누르면 내가 작성한 답안에 대한 채점 결과와 피드백을 확인할 수 있습니다.        
- 전체적인 서술형 평가 연습 과정과 채점 결과 및 피드백에 대한 소감과 느낀점을 남길 수 있습니다. 의견을 입력한 뒤 '소감 및 느낀점 등록하기' 버튼을 눌러주세요.          
- 마지막으로 '서술형 평가 연습 결과 저장하기' 버튼을 누르면 결과가 저장됩니다.""")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("다음 단계", on_click=next_page)
    
    with col2:
        st.write('')

    with col3: 
        st.write('')

def step1():
    st.subheader("1단계. 평가 코드 입력하기")
    st.info("선생님이 알려주신 평가 코드를 입력한 뒤 '평가 코드 확인하기' 버튼을 눌러주세요. 평가 코드를 입력해야 다음 단계로 넘어갈 수 있습니다.")

    with st.container(border=True):
        st.caption("평가코드")
# Google Sheets 인증 설정
        credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"])
        gc = gspread.authorize(credentials)

# 스프레드시트 열기
        spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
        worksheet = spreadsheet.sheet1

# 특정 설정 이름 입력
        setting_name = st.text_input("평가 코드를 입력하세요")

# 데이터 가져오기 버튼
        if st.button("평가 코드 확인하기"):

# 매번 rerun될 때마다 thread가 달라지는 것을 막기 위해 중간에 넣음.        
            st.session_state['usingthread'] = new_thread.id

# Google Sheets에서 모든 데이터 가져오기
            data = worksheet.get_all_records()

# '설정 이름'을 기준으로 해당 행 찾기
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
                + '3번 문항은 <' + st.session_state['question3'] + '> 입니다. 잘 기억하시길 바랍니다.')

                client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='모범답안을 입력하겠습니다.'
                + '1번 문항 모범답안은 <' + st.session_state['correctanswer1'] + '> 입니다.' 
                + '2번 문항 모범답안은 <' + st.session_state['correctanswer2'] + '> 입니다.' 
                + '3번 문항 모범답안은 <' + st.session_state['correctanswer3'] + '> 입니다. 잘 기억하시길 바랍니다.')

                client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 주의사항을 입력하겠습니다.'
                + '평가 주의사항은 <' + st.session_state['feedbackinstruction'] + '> 입니다. 잘 기억하시길 바랍니다.')

                st.success("평가를 성공적으로 불러왔습니다.")
                
            else:
                st.warning("평가 코드에 해당하는 데이터를 찾을 수 없습니다. 평가 코드를 확인해주세요.")

        st.write("---")
        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            st.button("이전 단계", on_click=prev_page)

        with col2:
            st.button("다음 단계", on_click=next_page, disabled=not bool(st.session_state['settingname']))
        
        with col3:
            st.button("처음 화면으로", on_click=go_home) 

def step2():
# 학생 정보 입력
    st.subheader("2단계. 정보 입력하기")
    st.success("반, 번호, 이름을 입력한 뒤 '학생 정보 등록하기' 버튼을 눌러주세요. 정보를 입력해야 다음 단계로 넘어갈 수 있습니다.")

    with st.container(border=True):
        st.caption("반, 번호, 이름 정보")
        studentclass = st.text_input("반")
        studentnumber = st.text_input("번호")
        studentname = st.text_input("이름")

        if st.button("학생 정보 등록하기"):
            st.session_state['studentclass'] = studentclass
            st.session_state['studentnumber'] = studentnumber
            st.session_state['studentname'] = studentname
            st.success("학생 정보가 성공적으로 등록되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page, disabled=not bool(st.session_state['studentname']))
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 답안 입력 및 결과 확인
def step3():
    st.subheader("3단계. 답안 작성 및 결과 확인하기")

    with st.container(border=True):
        st.caption("답안 작성")
        st.error("서술형 문항을 잘 읽고 답안을 작성하세요. 답안을 작성한 뒤 '작성 답안 등록하기' 버튼을 눌러주세요.")

        if 'question1' in st.session_state and st.session_state['question1']:
            answer1 = st.text_area("1번 문항: " + st.session_state['question1'], height=100)
        else:
            answer1 = None

        if 'question2' in st.session_state and st.session_state['question2']:
            answer2 = st.text_area("2번 문항: " + st.session_state['question2'], height=100)
        else:
            answer2 = None

        if 'question3' in st.session_state and st.session_state['question3']:
            answer3 = st.text_area("3번 문항: " + st.session_state['question3'], height=100)
        else:
            answer3 = None

# 답안 등록
        answer_input_button = st.button('작성 답안 등록하기', disabled=st.session_state['openclose'] == 'close')
        if answer1 is not None:
            st.session_state['answer1'] = answer1
        if answer2 is not None:
            st.session_state['answer2'] = answer2
        if answer3 is not None:
            st.session_state['answer3'] = answer3

        if answer_input_button:
            client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='학생이 작성한 답안을 입력하겠습니다.'
                    + '1번 문항에 대한 학생 답안은 <' + st.session_state['answer1'] + '> 입니다.' 
                    + '2번 문항에 대한 학생 답안은 <' + st.session_state['answer2'] + '> 입니다.'
                    + '3번 문항에 대한 학생 답안은 <' + st.session_state['answer3'] + '> 입니다. 잘 기억하시길 바랍니다.')
            
            st.success('작성한 답안이 성공적으로 등록되었습니다.')
            st.session_state['openclose'] = 'close'

# 채점 및 피드백 생성 
    with st.container(border=True):
        st.caption("채점 결과 및 피드백")
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
                content= '1번 문항은' + st.session_state['question1'] + '입니다.' + '학생 답안은' + st.session_state['answer1'] + '입니다.' + '1번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

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
                content='2번 문항은' + st.session_state['question2'] + '입니다.' + '학생 답안은' + st.session_state['answer2'] + '입니다.' + '2번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

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
                content='3번 문항은' + st.session_state['question3'] + '입니다.' + '학생 답안은' + st.session_state['answer3'] + '입니다.' + '3번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. **instructions에 나와 있는 대로 생성합니다. **instructions에 따르면 채점 결과에 따라 생성하는 피드백의 내용이 달라지므로 꼭 확인하세요. 학생이 입력한 답안, 채점 결과, 피드백 내용을 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. 【5:12†source】처럼 생긴 참조는 아예 보이지 않게 해주세요.')

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

# 채점 결과 보이기
            st.write(st.session_state['feedback1'])
            st.divider()
            st.write(st.session_state['feedback2'])
            st.divider()
            st.write(st.session_state['feedback3'])

# 학생 의견 작성 
    with st.container(border=True):
        st.caption("소감 및 느낀점")
        st.error("채점 결과 및 피드백을 확인하고 새롭게 알게된 점이나 궁금한 점, 채점 결과 및 피드백에 대해 이해가 가지 않는 점 등 생각을 적어주세요.")
        studentopinion1 = st.text_area("", label_visibility="collapsed", key="textarea1")

        st.error("서술형 평가 연습에 대해 선생님께 하고 싶은 말이나 좋았던 점, 아쉬웠던 점 등 전반적인 소감이나 느낀점을 적어주세요. 의견을 작성한 뒤 '소감 및 느낀점 등록하기' 버튼을 눌러주세요. ")
        studentopinion2 = st.text_area("", label_visibility="collapsed", key="textarea2")
        studentopinionbutton = st.button("소감 및 느낀점 등록하기")

        if studentopinionbutton:
            st.session_state['studentopinion1'] = studentopinion1
            st.session_state['studentopinion2'] = studentopinion2

            st.success('소감 및 느낀점이 성공적으로 등록되었습니다.')

# 자동 저장 기능
    with st.container(border=True):
        st.caption("저장")
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
            worksheet = spreadsheet.get_worksheet(1)

# 저장하기
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([current_time, st.session_state['settingname'], st.session_state['studentclass'], st.session_state['studentnumber'], st.session_state['studentname'], st.session_state['answer1'], st.session_state['score1'], st.session_state['feedback1'], st.session_state['answer2'], st.session_state['score2'], st.session_state['feedback2'], st.session_state['answer3'], st.session_state['score3'], st.session_state['feedback3'], st.session_state['studentopinion1'], st.session_state['studentopinion2']])
            st.success('서술형 평가 연습 결과가 성공적으로 저장되었습니다.')
            st.session_state['openclose'] = 'open'

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        st.button("이전 단계", on_click=prev_page)
    
    with col2:
        st.button("처음 화면으로", on_click=go_home) 

    with col3: 
        st.write('')

# 현재 페이지 상태에 따라 적절한 페이지 표시
current_page = st.session_state['page']

if current_page == 0:
    home()
elif current_page == 1:
    step1()
elif current_page == 2:
    step2()
elif current_page == 3:
    step3()