# 5학년 4반
# 피드백은 제공하지 않고 채점 결과만 제공함.

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
assistant_id = 'asst_R4ZpxD9c27ImT641ttLM7m0G'
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
if 'studentopinion' not in st.session_state:
    st.session_state['studentopinion'] = ''

# 페이지 전환 함수 정의
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_home():
    st.session_state.page = 0

# 홈페이지 구성 
st.header(':100: 사회 5학년 2학기 서술형 평가 연습')

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

        st.error("""3. [답안 작성 및 결과 확인하기]:            
- 서술형 문항을 잘 읽고 답안을 입력하세요. 문항이 보이지 않는 경우 문제가 3개보다 적은 경우입니다.
- 답안을 입력한 뒤 등록 버튼을 눌러주세요.         
- 채점 결과 확인하기 버튼을 누르면 내가 입력한 답안에 대한 채점 결과를 볼 수 있습니다.        
- 전체적인 서술형 평가 연습 과정과 채점 결과에 대한 소감과 느낀점을 남길 수 있습니다. 의견을 입력한 뒤 등록 버튼을 눌러주세요.          
- 마지막으로 저장 버튼을 누르면 서술형 평가 연습 결과가 저장됩니다.""")

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
                
                st.success("평가를 성공적으로 불러왔습니다.")
                
            else:
                st.warning("평가 코드에 해당하는 데이터를 찾을 수 없습니다. 평가 코드를 확인해주세요.")

# 어시스턴트와 대화 생성
            if 'question1' in st.session_state and 'correctanswer1' in st.session_state:
                thread_message = client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 문항과 모범답안을 새롭게 등록합니다. 기존 평가 문항과 모범답안은 지우고 지금부터 입력한 것을 기억하세요. 1번 문항은 <' + st.session_state['question1'] +
                '> 입니다. user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer1'] +
                ' 입니다. 2번 문항은 <' + st.session_state['question2'] + '> 입니다. user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer2'] +
                ' 입니다. 3번 문항은 <' + st.session_state['question3'] + '> 입니다. user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer3'] + ' 입니다.'
                )
                
                thread_message = client.beta.threads.messages.create(
                    thread_id=st.session_state['usingthread'],
                    role="user",
                    content='평가 주의사항은 <' + st.session_state['feedbackinstruction'] + '> 입니다. 채점 결과를 제공할 때 위 내용을 고려해서 작성해주시기 바랍니다.'
                )

                thread_message = client.beta.threads.messages.create(
                    thread_id=st.session_state['usingthread'],
                    role="user",
                    content='현재 업로드된 서술형 평가 문항과 모범답안을 모두 보여주세요. user(teacher)가 입력한 평가 문항을 그대로 보여주세요. 모범답안의 경우 user(teacher)가 입력한 것이 있으면 그것을 보여주고, 없으면 vector store vs_FtRt7SEalipabRPrOk0usxl8 file search를 통해 문항과 관련된 내용을 찾아 모범답안을 만들어서 보여주세요. 만약 문항과 관련된 내용을 찾을 수 없다면 모범답안을 작성하지 않습니다. 절대 vector store에 없는 내용이나 수준 높은 내용으로 모범답안을 작성하지 않습니다. 어떤 파일 어떤 페이지를 보면 되는지 함께 보여주세요. 표 형태로 보여주세요. 반드시 서술형 평가 문항와 모범답안 외에 다른 문장을 넣지 마세요. 그리고 현재 업로드된 평가 주의사항을 모두 보여주세요. 반드시 평가 주의사항 외에 다른 문장을 넣지 마세요.'
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

                thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
                msg = thread_messages.data[0].content[0].text.value

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
        st.error("서술형 문항을 잘 읽고 답안을 입력하세요. 답안을 입력한 뒤 등록 버튼을 눌러주세요.")

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
        answer_input_button = st.button('작성 답안 등록하기')
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
            content='1번 문항에 대한 학생 답안은 <' + st.session_state['answer1'] + 
            '> 입니다. 2번 문항에 대한 학생 답안은 <' + st.session_state['answer2'] + 
            '> 입니다. 3번 문항에 대한 학생 답안은 <' + st.session_state['answer3'] +'> 입니다.')

            st.success('작성한 답안이 성공적으로 등록되었습니다.')

# 채점 및 피드백 생성 
    with st.container(border=True):
        st.caption("채점 결과")
        st.error("채점 결과 버튼을 누르면 내가 입력한 답안에 대한 채점 결과를 확인할 수 있습니다.")

        feedback_output_button = st.button('채점 결과 확인하기')
        if feedback_output_button:
            if 'question1' in st.session_state and st.session_state['question1']:
                thread_message = client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='1번 문항에 대한 학생 답안을 보고 채점 결과를 생성해주세요. 벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일을 확인한 다음 채점을 진행합니다. 모범답안과 비교해 학생 답안을 채점합니다. 반드시 업로드된 파일에 근거하여 채점을 진행합니다. 평가 문항, 학생 답안, 채점 결과가 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다. 평가 주의사항은 보여주지 않습니다. 표 형식으로 보여주지 말고, 학생이 입력한 답안과 평가 결과를 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. ***평가 결과는 좀 더 큰 글씨로 빨간색으로 보여주세요. ***긍정적인 부분이나 개선 점은 보여주지 않고, 오직 채점 결과만 보여주세요.')

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

            if 'question2' in st.session_state and st.session_state['question2']:
                thread_message2 = client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='2번 문항에 대한 학생 답안을 보고 채점 결과를 생성해주세요. 벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일을 확인한 다음 채점을 진행합니다. 모범답안과 비교해 학생 답안을 채점합니다. 반드시 업로드된 파일에 근거하여 채점을 진행합니다. 평가 문항, 학생 답안, 채점 결과가 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다. 평가 주의사항은 보여주지 않습니다. 표 형식으로 보여주지 말고, 학생이 입력한 답안과 평가 결과를 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. ***평가 결과는 좀 더 큰 글씨로 빨간색으로 보여주세요. ***긍정적인 부분이나 개선 점은 보여주지 않고, 오직 채점 결과만 보여주세요.')

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

            if 'question3' in st.session_state and st.session_state['question3']:
                client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='3번 문항에 대한 학생 답안을 보고 채점 결과를 생성해주세요. 벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일을 확인한 다음 채점을 진행합니다. 모범답안과 비교해 학생 답안을 채점합니다. 반드시 업로드된 파일에 근거하여 채점을 진행합니다. 평가 문항, 학생 답안, 채점 결과가 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다. 평가 주의사항은 보여주지 않습니다. 표 형식으로 보여주지 말고, 학생이 입력한 답안과 평가 결과를 각각 서로 다른 문단으로 나눠서 읽기 쉽게 보여주세요. ***평가 결과는 좀 더 큰 글씨로 빨간색으로 보여주세요. ***긍정적인 부분이나 개선 점은 보여주지 않고, 오직 채점 결과만 보여주세요.')

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

# 예시: 채점 결과 부분만 빨간색으로 표시
            st.write(st.session_state['feedback1'])
            st.divider()
            st.write(st.session_state['feedback2'])
            st.divider()
            st.write(st.session_state['feedback3'])

# 학생 의견 작성 
    with st.container(border=True):
        st.caption("소감 및 느낀점")
        st.error("전체적인 평가 연습 과정과 채점 결과에 대한 의견을 적어주세요. 결과에 대해 궁금한 점이나 이해가 가지 않는 부분, 혹은 단순한 소감이나 느낀점도 좋습니다. 의견을 입력한 뒤 등록 버튼을 눌러주세요. ")

        studentopinion = st.text_area("", label_visibility="collapsed")
        studentopinionbutton = st.button("소감 및 느낀점 등록하기")
        if studentopinionbutton:
            st.session_state['studentopinion'] = studentopinion
            st.success('소감 및 느낀점이 성공적으로 등록되었습니다.')

# 자동 저장 기능
    with st.container(border=True):
        st.caption("저장")
        st.error("마지막으로 저장 버튼을 누르면 서술형 평가 연습 결과가 저장됩니다.")

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
            worksheet = spreadsheet.get_worksheet(2)

# 저장하기
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([current_time, st.session_state['settingname'], st.session_state['studentclass'], st.session_state['studentnumber'], st.session_state['studentname'], st.session_state['answer1'], st.session_state['feedback1'], st.session_state['answer2'], st.session_state['feedback2'], st.session_state['answer3'], st.session_state['feedback3'], st.session_state['studentopinion']])
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