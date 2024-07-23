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

# 사이드바에 학생 페이지 콘텐츠 추가
st.sidebar.title("서술형 평가 답안 작성 페이지")

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
worksheet = spreadsheet.sheet1

# 홈페이지 구성 
st.subheader('초등학교 사회 5학년 2학기 서술형 평가 연습 도구')

# 사용 방법 소개
with st.container(border=True):
    st.write(
"""
[[서술형 평가 실시]] 페이지 사용 방법

1. 선생님께서 알려주신 서술형 평가 설정 이름을 입력합니다. 

2. [학생 정보 입력]: 반, 번호, 이름을 적은 뒤 등록 버튼을 눌러 등록합니다.

3. [답안 입력 및 결과 확인]: 

- 서술형 문항에 맞는 답안을 입력합니다. 답안을 입력한 뒤에는 등록 버튼을 눌러 등록합니다. 

- 이후 채점 및 피드백 생성 버튼을 눌러 내가 입력한 답안에 대한 점수와 피드백을 확인합니다. 

- 학생 의견을 입력할 수 있습니다. 서술형 평가 전반에 대한 생각이나 느낌, 피드백을 보고난 뒤 드는 생각이나 느낌 등을 적을 수 있습니다. 

- 서술평 평가 결과 저장 버튼을 눌러 저장합니다.
""")

with st.container(border=True):
# 특정 설정 이름 입력
    setting_name = st.text_input("설정 이름을 입력하세요")

# 데이터 가져오기 버튼
    if st.button("설정 불러오기"):

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
            
            st.success("평가 문항 설정 데이터를 성공적으로 가져왔습니다.")
            
# st.session_state 확인용 출력 나중에 지울 수 있음.
            st.write(st.session_state)
        else:
            st.warning("입력한 '설정 이름'에 해당하는 데이터를 찾을 수 없습니다.")

# 어시스턴트와 대화 생성
        if 'question1' in st.session_state and 'correctanswer1' in st.session_state:
            thread_message = client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 문항과 모범답안을 새롭게 등록합니다. 기존 평가 문항과 모범답안은 잊고 지금부터 입력한 것을 기억하세요. 1번 문항은 <' + st.session_state['question1'] + 
                '> 입니다. 사용자가 입력한 모범답안은 <' + st.session_state['correctanswer1'] + 
                ' 입니다. 2번 문항은 <' + st.session_state['question2'] + '> 입니다. 사용자가 입력한 모범답안은 <' + st.session_state['correctanswer2'] + 
                ' 입니다. 3번 문항은 <' + st.session_state['question3'] + '> 입니다. 사용자가 입력한 모범답안은 <' + st.session_state['correctanswer3'] + ' 입니다.'
            )

            thread_message = client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 주의사항은 <' + st.session_state['feedbackinstruction'] + '> 입니다. 피드백을 제공할 때 위 내용을 고려해서 작성해주시기 바랍니다.'
            )

            thread_message = client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='현재 업로드된 서술형 평가 문항과 모범답안을 모두 보여주세요. user(teacher)가 입력한 평가 문항을 그대로 보여주세요. 모범답안의 경우 user(teacher)가 입력한 것이 있으면 그것을 보여주고, 없으면 file search를 통해 모범답안을 만들어서 보여주세요. 어떤 파일 어떤 페이지를 보면 되는지 함께 보여주세요. 표 형태로 보여주세요. 반드시 서술형 평가 문항와 모범답안 외에 다른 문장을 넣지 마세요. 그리고 현재 업로드된 평가 주의사항을 모두 보여주세요. 반드시 평가 주의사항 외에 다른 문장을 넣지 마세요.'
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
            st.write(msg)
        else:
            st.warning("평가 문항 설정 데이터를 먼저 불러와야 합니다.")

# 탭설정
tab1, tab2 = st.tabs(["학생 정보 입력", "답안 입력 및 결과 확인"])

# 학생 정보 입력
with tab1:
    st.subheader("학생 정보 입력")
    studentclass = st.text_input("반")
    studentnumber = st.text_input("번호")
    studentname = st.text_input("이름")

    if st.button("학생 정보 등록"):
        st.session_state['studentclass'] = studentclass
        st.session_state['studentnumber'] = studentnumber
        st.session_state['studentname'] = studentname
        st.success("학생 정보가 성공적으로 등록되었습니다.")

# 답안 입력 및 결과 확인
with tab2:
    st.subheader("답안 입력 및 결과 확인")

    with st.container(border=True):
        st.caption("답안 입력")
        if 'question1' in st.session_state:
            answer1 = st.text_area("1번 문항: " + st.session_state['question1'], height=100)
            answer2 = st.text_area("2번 문항: " + st.session_state['question2'], height=100)
            answer3 = st.text_area("3번 문항: " + st.session_state['question3'], height=100)

# 답안 등록
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
                content='1번 문항에 대한 학생 답안은 <' + st.session_state['answer1'] + 
                '> 입니다. 2번 문항에 대한 학생 답안은 <' + st.session_state['answer2'] + 
                '> 입니다. 3번 문항에 대한 학생 답안은 <' + st.session_state['answer3'] +'> 입니다.'
                )

                st.success(f'학생 답안이 성공적으로 등록되었습니다.')

# 채점 및 피드백 생성 
    with st.container(border=True):
        st.caption("채점 및 피드백 결과 확인")
        feedback_output_button = st.button('채점 및 피드백 생성')
        if feedback_output_button:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일을 확인한 다음 채점 및 피드백을 진행합니다. 업로드된 파일에 근거하여 채점 및 피드백을 진행합니다. 1번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. 평가 문항, 학생 답안, 채점 결과 및 피드백이 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다. 평가 주의사항는 보여주지 않습니다.'
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
            content='2번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. 벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일을 확인한 다음 채점 및 피드백을 진행합니다. 업로드된 파일에 근거하여 채점 및 피드백을 진행합니다. 평가 문항, 학생 답안, 채점 결과 및 피드백이 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다.'
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
            content='3번 문항에 대한 학생 답안을 보고 채점 및 피드백을 생성해주세요. 벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일을 확인한 다음 채점 및 피드백을 진행합니다. 업로드된 파일에 근거하여 채점 및 피드백을 진행합니다. 평가 문항, 학생 답안, 채점 결과 및 피드백이 포함되도록 보여주세요. 평가 주의사항을 지키면서 진행합니다.'
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
    with st.container(border=True):
        saveresult = st.button("서술형 평가 결과 저장")
        if saveresult:

# 구글 시트 열기
# Google Sheets 인증 설정
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\streamlit/240509/m20223715-403a2aed16a4.json', scope)
            gc = gspread.authorize(credentials)

# 스프레드시트 열기
            spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
            worksheet = spreadsheet.get_worksheet(1)

# 저장하기
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([current_time, st.session_state['settingname'], st.session_state['studentclass'], st.session_state['studentnumber'], st.session_state['studentname'], st.session_state['answer1'], st.session_state['feedback1'], st.session_state['answer2'], st.session_state['feedback2'], st.session_state['answer3'], st.session_state['feedback3'], st.session_state['studentopinion']])
            st.success(f'서술형 평가 결과가 성공적으로 저장되었습니다.')