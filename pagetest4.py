# 라이브러리
import streamlit as st
from openai import OpenAI
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random
import json

# API KEY, THREAD, client 생성
api_keys = st.secrets["api"]["keys"]
selected_api_key = random.choice(api_keys)
client = OpenAI(api_key=selected_api_key)
assistant_id = 'asst_t0CtEvNce3uo8pMqY4BjLY78'
new_thread = client.beta.threads.create()

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 0
if 'settingname' not in st.session_state:
    st.session_state['settingname'] = ''
if 'selectquestion1' not in st.session_state:
    st.session_state['selectquestion1'] = ''
if 'selectquestion2' not in st.session_state:
    st.session_state['selectquestion2'] = ''
if 'selectquestion3' not in st.session_state:
    st.session_state['selectquestion3'] = ''
if 'selectquestion4' not in st.session_state:
    st.session_state['selectquestion4'] = ''
if 'selectquestion5' not in st.session_state:
    st.session_state['selectquestion5'] = ''
if 'question1_option1' not in st.session_state:
    st.session_state['question1_option1'] = ''
if 'question1_option2' not in st.session_state:
    st.session_state['question1_option2'] = ''
if 'question1_option3' not in st.session_state:
    st.session_state['question1_option3'] = ''
if 'question1_option4' not in st.session_state:
    st.session_state['question1_option4'] = ''
if 'question1_option5' not in st.session_state:
    st.session_state['question1_option5'] = ''
if 'question2_option1' not in st.session_state:
    st.session_state['question2_option1'] = ''
if 'question2_option2' not in st.session_state:
    st.session_state['question2_option2'] = ''
if 'question2_option3' not in st.session_state:
    st.session_state['question2_option3'] = ''
if 'question2_option4' not in st.session_state:
    st.session_state['question2_option4'] = ''
if 'question2_option5' not in st.session_state:
    st.session_state['question2_option5'] = ''
if 'question3_option1' not in st.session_state:
    st.session_state['question3_option1'] = ''
if 'question3_option2' not in st.session_state:
    st.session_state['question3_option2'] = ''
if 'question3_option3' not in st.session_state:
    st.session_state['question3_option3'] = ''
if 'question3_option4' not in st.session_state:
    st.session_state['question3_option4'] = ''
if 'question3_option5' not in st.session_state:
    st.session_state['question3_option5'] = ''
if 'question4_option1' not in st.session_state:
    st.session_state['question4_option1'] = ''
if 'question4_option2' not in st.session_state:
    st.session_state['question4_option2'] = ''
if 'question4_option3' not in st.session_state:
    st.session_state['question4_option3'] = ''
if 'question4_option4' not in st.session_state:
    st.session_state['question4_option4'] = ''
if 'question4_option5' not in st.session_state:
    st.session_state['question4_option5'] = ''
if 'question5_option1' not in st.session_state:
    st.session_state['question5_option1'] = ''
if 'question5_option2' not in st.session_state:
    st.session_state['question5_option2'] = ''
if 'question5_option3' not in st.session_state:
    st.session_state['question5_option3'] = ''
if 'question5_option4' not in st.session_state:
    st.session_state['question5_option4'] = ''
if 'question5_option5' not in st.session_state:
    st.session_state['question5_option5'] = ''
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
if 'studentclass' not in st.session_state:
    st.session_state['studentclass'] = ''
if 'studentnumber' not in st.session_state:
    st.session_state['studentnumber'] = ''
if 'studentname' not in st.session_state:
    st.session_state['studentname'] = ''
if 'selectanswer1' not in st.session_state:
    st.session_state['selectanswer1'] = ''
if 'selectanswer2' not in st.session_state:
    st.session_state['selectanswer2'] = ''
if 'selectanswer3' not in st.session_state:
    st.session_state['selectanswer3'] = ''
if 'selectanswer4' not in st.session_state:
    st.session_state['selectanswer4'] = ''
if 'selectanswer5' not in st.session_state:
    st.session_state['selectanswer5'] = ''
if 'score' not in st.session_state:
    st.session_state['score'] = 0 

# 페이지 전환 함수 정의
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_home():
    st.session_state.page = 0

# 홈페이지 구성 
st.header(':100: 사회 5학년 2학기 정리활동')

# 사용 방법 소개
def home():
    with st.container(border=True):
        st.write("""
        학생 페이지 사용 방법
                    
        총 3단계로 이루어져 있습니다. 차례대로 다음 단계로 넘어가주세요.""")

        st.info("""1. [평가 코드 입력하기]:           
- 선생님이 알려주신 평가 코드를 입력한 뒤 등록 버튼을 눌러주세요.
- 평가 코드를 입력해야 다음 단계로 넘어갈 수 있습니다.""")
                    
        st.success("""2. [정보 입력하기]:           
- 반, 번호, 이름을 입력한 뒤 등록 버튼을 눌러주세요. 
- 정보를 입력해야 다음 단계로 넘어갈 수 있습니다.""")

        st.warning("""3. [답안 입력 및 결과 확인하기]:
- 문제를 잘 읽고 보기 중 하나를 골라주세요. 
- 답안을 입력한 다음에는 입력 답안 등록하기 버튼을 누르고, 결과 확인하기 버튼을 눌러주세요.
- 마지막으로 결과 저장하기 버튼을 누르면 결과가 저장됩니다.""")

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
    st.info("선생님이 알려주신 평가 코드를 입력한 뒤 확인 버튼을 눌러주세요. 평가 코드를 입력해야 다음 단계로 넘어갈 수 있습니다.")

    with st.container(border=True):
        st.caption("평가코드")
# Google Sheets 인증 설정
        credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"
        ])
        gc = gspread.authorize(credentials)

# 스프레드시트 열기
        spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
        worksheet = spreadsheet.get_worksheet(2)

# 특정 설정 이름 입력
        setting_name = st.text_input("평가 코드를 입력하세요")

# 데이터 가져오기 버튼
        if st.button("평가 코드 확인하기"):

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
                
                st.success("평가를 성공적으로 불러왔습니다.")
                
# st.session_state 확인용 출력 나중에 지울 수 있음.
                st.write(st.session_state)
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
    st.success("반, 번호, 이름을 입력한 뒤 등록 버튼을 눌러주세요. 정보를 입력해야 다음 단계로 넘어갈 수 있습니다.")

    with st.container(border=True):
        st.caption("반, 번호, 이름 정보")
        studentclass = st.text_input("반")
        studentnumber = st.text_input("번호")
        studentname = st.text_input("이름")

        if st.button("정보 등록하기"):
            st.session_state['studentclass'] = studentclass
            st.session_state['studentnumber'] = studentnumber
            st.session_state['studentname'] = studentname
            st.success("정보가 성공적으로 등록되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page, disabled=not bool(st.session_state['studentname']))
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 답안 입력하기
def step3():
    st.subheader("3단계. 답안 입력 및 결과 확인하기")

    with st.container(border=True):
        st.caption("답안 작성")
        st.warning("문제를 잘 읽고 답안을 입력하세요. 답안을 입력한 뒤 정답 확인하기 버튼을 눌러주세요.")
        st.session_state['score'] = 0 

        if 'selectquestion1'in st.session_state and st.session_state['selectquestion1']:
            selectquestion1 = st.radio(st.session_state['selectquestion1'], [
                st.session_state['question1_option1'], 
                st.session_state['question1_option2'], 
                st.session_state['question1_option3'], 
                st.session_state['question1_option4'], 
                st.session_state['question1_option5']],
                key='selectquestion1_radio')

        if 'selectquestion2'in st.session_state and st.session_state['selectquestion2']:
            selectquestion2 = st.radio(st.session_state['selectquestion2'], [
                st.session_state['question2_option1'], 
                st.session_state['question2_option2'], 
                st.session_state['question2_option3'], 
                st.session_state['question2_option4'], 
                st.session_state['question2_option5']],
                key='selectquestion2_radio')

        if 'selectquestion3'in st.session_state and st.session_state['selectquestion3']:
            selectquestion3 = st.radio(st.session_state['selectquestion3'], [
                st.session_state['question3_option1'], 
                st.session_state['question3_option2'], 
                st.session_state['question3_option3'], 
                st.session_state['question3_option4'], 
                st.session_state['question3_option5']],
                key='selectquestion3_radio')

        if 'selectquestion4'in st.session_state and st.session_state['selectquestion4']:
            selectquestion4 = st.radio(st.session_state['selectquestion4'], [
                st.session_state['question4_option1'], 
                st.session_state['question4_option2'], 
                st.session_state['question4_option3'], 
                st.session_state['question4_option4'], 
                st.session_state['question4_option5']],
                key='selectquestion4_radio')

        if 'selectquestion5'in st.session_state and st.session_state['selectquestion5']:
            selectquestion5 = st.radio(st.session_state['selectquestion5'], [
                st.session_state['question5_option1'], 
                st.session_state['question5_option2'], 
                st.session_state['question5_option3'], 
                st.session_state['question5_option4'], 
                st.session_state['question5_option5']],
                key='selectquestion5_radio')

# 결과 확인하기
            selectquestionanswer_input_button = st.button('작성 답안 등록하기')
            if selectquestionanswer_input_button:
                st.session_state['selectanswer1'] = selectquestion1
                st.session_state['selectanswer2'] = selectquestion2 
                st.session_state['selectanswer3'] = selectquestion3
                st.session_state['selectanswer4'] = selectquestion4
                st.session_state['selectanswer5'] = selectquestion5

            selectquestionanswer_check_button = st.button('결과 확인하기')
            if selectquestionanswer_check_button:
                if selectquestion1 == st.session_state['correctanswer1']:
                    st.session_state['score'] += 1
                    st.success('1번 문항은 정답입니다.')
                else:
                    st.error('1번 문항은 오답입니다.')

                if selectquestion2 == st.session_state['correctanswer2']:
                    st.session_state['score'] += 1
                    st.success('2번 문항은 정답입니다.')
                else:
                    st.error('2번 문항은 오답입니다.')

                if selectquestion3 == st.session_state['correctanswer3']:
                    st.session_state['score'] += 1
                    st.success('3번 문항은 정답입니다.')
                else:
                    st.error('3번 문항은 오답입니다.')

                if selectquestion4 == st.session_state['correctanswer4']:
                    st.session_state['score'] += 1
                    st.success('4번 문항은 정답입니다.')
                else:
                    st.error('4번 문항은 오답입니다.')

                if selectquestion5 == st.session_state['correctanswer5']:
                    st.session_state['score'] += 1
                    st.success('5번 문항은 정답입니다.')
                else:
                    st.error('5번 문항은 오답입니다.')

                st.warning('총 점수는 ' + str(st.session_state['score']) + '입니다.')

# 자동 저장 기능
    with st.container(border=True):
        st.caption("저장")
        st.warning("마지막으로 저장 버튼을 누르면 정리활동 결과가 저장됩니다.")

        saveresult = st.button("정리활동 결과 저장하기")
        if saveresult:

# 구글 시트 열기
# Google Sheets 인증 설정
            credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/spreadsheets"
            ])
            gc = gspread.authorize(credentials)

# 스프레드시트 열기
            spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
            worksheet = spreadsheet.get_worksheet(3)

# 저장하기
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([
            current_time, 
            st.session_state['settingname'], 
            st.session_state['studentclass'], 
            st.session_state['studentnumber'], 
            st.session_state['studentname'], 
            st.session_state['selectanswer1'], 
            st.session_state['selectanswer2'], 
            st.session_state['selectanswer3'], 
            st.session_state['selectanswer4'], 
            st.session_state['selectanswer5'], 
            st.session_state['score']])
            st.success('서술형 평가 결과가 성공적으로 저장되었습니다.')

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