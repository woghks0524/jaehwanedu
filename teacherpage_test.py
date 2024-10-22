import streamlit as st
from openai import OpenAI
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# API KEY, THREAD, client 생성
api_keys = st.secrets["api"]["keys"]
selected_api_key = random.choice(api_keys)
client = OpenAI(api_key=selected_api_key)
assistant_id = 'asst_2FrZmOonHQCPO6EhXzQ6u3nr'

# 화면 페이키 크기 설정
st.set_page_config(layout="wide")

# 제작자 이름 
st.caption("이 웹 어플리케이션은 정재환(서울특별시교육청 소속 초등교사)에 의해 만들어졌습니다. 문의사항은 woghks0524jjh@gmail.com 또는 010-3393-0283으로 연락주세요.")

# 전체 제목
st.header(':memo:서술형 평가 설정 페이지')

# CSS 스타일을 사용하여 상단바와 메뉴 숨기기
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             header {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
if 'vectorstoreid' not in st.session_state:
    st.session_state['vectorstoreid'] = ''
if 'assiapi' not in st.session_state:
    st.session_state['assiapi'] = ''
if 'vectorapi' not in st.session_state:
    st.session_state['vectorapi'] = ''
if 'q1_image_id' not in st.session_state:
    st.session_state['q1_image_id'] = ''
if 'q2_image_id' not in st.session_state:
    st.session_state['q2_image_id'] = ''
if 'q3_image_id' not in st.session_state:
    st.session_state['q3_image_id'] = ''

# 구글 드라이브 서비스 인증 설정
def authenticate_services():
    # 구글 드라이브 서비스 인증 설정
    scope = ['https://www.googleapis.com/auth/drive']
    
    # st.secrets에서 credentials 가져오기 (문자열로 불러온 후 JSON 파싱)
    credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
    
    # ServiceAccountCredentials로 변환
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    
    # 구글 드라이브 서비스 생성
    drive_service = build('drive', 'v3', credentials=credentials)
    
    return drive_service
# 구글 드라이브에 이미지 업로드 함수 정의
def upload_image_to_drive(service, file):

# 이미지 업로드 메타데이터 정의
    file_metadata = {
        'name': file.name,  # 파일 이름 설정
        'mimeType': 'image/jpeg'  # 이미지 MIME 타입 설정 (필요에 따라 변경 가능)
    }
    
# 이미지 업로드
    media = MediaFileUpload(file.name, mimetype=file.type)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    return uploaded_file.get('id')

# 인증 서비스 초기화
drive_service = authenticate_services()

# 페이지 전환 함수 정의
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_home():
    st.session_state.page = 0

# 홈 
def home():
    with st.container(border=True):
            st.write("""
            서술형 평가 설정 페이지 사용 방법
                     
            총 4단계로 이루어져 있습니다. 각 단계에 필요한 내용을 입력하고 다음 단계로 넘어가주세요.""")

            st.info("""1. [평가 코드 만들기]:
- 선생님이 만든 서술형 평가의 평가 코드를 만든 뒤 등록 버튼을 눌러주세요.
- 평가 코드는 학생 페이지에서 선생님이 만든 평가를 불러오는 데 사용됩니다.""")
                     
            st.success("""2. [자료 입력하기]: 
- 서술형 평가에 활용할 수 있는 자료를 입력해 주세요. 
- 교과서 pdf, 수업 자료 pdf 등을 입력할 수 있습니다. 
- 입력한 자료를 근거로 모범 답안을 생성하거나 학생 답안을 채점할 수 있습니다.""")

            st.error("""3. [평가 문항 및 주의사항 입력하기]: 
- 서술형 평가 문항과 모범답안(선택 사항)을 입력해 주세요. 
- 서술형 평가 문항은 최대 3개까지 입력 가능합니다. 
- 평가 주의사항을 입력할 수 있습니다.
- 입력한 평가 주의사항을 근거로 채점 및 피드백을 생성할 수 있습니다.""")

            st.warning("""4. [평가 확인 및 저장하기]: 
- 선생님이 만든 서술형 평가를 확인하고 저장합니다. 
- 수정이 필요하다면 수정이 필요한 부분으로 돌아가서 다시 입력한 다음 저장합니다.""")

    st.button("다음 단계", on_click=next_page)

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

# 평가 코드 중복 확인 함수 생성 
def is_code_duplicate(settingname):
    # 구글 시트에서 모든 평가 코드 가져오기
    codes = worksheet.col_values(2)  # 2번째 열에 평가 코드가 있다고 가정
    return settingname in codes

# 1단계
def step1():
    st.subheader("1단계. 과목, 학년, 단원, 교과서 선택하기")
    st.info("선생님께서 만드실 서술형 평가 문항의 과목, 학년, 단원, 교과서를 선택해주세요.")

# 선택박스를 통해 어시스턴트, 벡터스토어 API 선택하기
    option = st.selectbox("옵션을 선택하세요", ("사회 5-1 미래엔", "사회 5-1 천재", "과학 5-1 아이스크림"))

    if option == "사회 5-1 미래엔":
        assistant_id = 'asst_3g0xvrDZB8djLcHJnXM4NkqV'
        vectorstoreid = 'vs_VVI1NN44uq5xEDEDF5RvGiW4'
        st.session_state['assiapi'] = 'asst_3g0xvrDZB8djLcHJnXM4NkqV'
        st.session_state['vectorstoreid'] = 'vs_VVI1NN44uq5xEDEDF5RvGiW4'
 
    elif option == "사회 5-1 천재":
        assistant_id = 'asst_5ArcGNyTPsTZ0XKLfFepCvtU'
        vectorstoreid = 'vs_eFbWQhlau8UEG2i1cxUxdICP'
        st.session_state['assiapi'] = 'asst_5ArcGNyTPsTZ0XKLfFepCvtU'
        st.session_state['vectorstoreid'] = 'vs_eFbWQhlau8UEG2i1cxUxdICP'
 
    elif option == "과학 5-1 아이스크림":
        assistant_id = 'asst_nZr417YaP34BAjS7gbhfDQcS'
        vectorstoreid = 'vs_wjHLRvzAf7tyDfSUCeAm6NIc'
        st.session_state['assiapi'] = 'asst_nZr417YaP34BAjS7gbhfDQcS'
        st.session_state['vectorstoreid'] = 'vs_wjHLRvzAf7tyDfSUCeAm6NIc'

    else:
        assistant_id = 'asst_2FrZmOonHQCPO6EhXzQ6u3nr'
        vectorstoreid = 'vs_FtRt7SEalipabRPrOk0usxl8'
        st.session_state['assiapi'] = 'asst_2FrZmOonHQCPO6EhXzQ6u3nr'
        st.session_state['vectorstoreid'] = 'vs_FtRt7SEalipabRPrOk0usxl8'

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page)
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 2단계
def step2():
    st.subheader("2단계. 평가 코드 만들기")
    st.info("선생님이 만든 평가를 찾기 위한 평가 코드를 만들어주세요. 학생 페이지에서 선생님이 만든 평가를 불러오는 데 사용됩니다. 예를 들어 [고조선은 어떤 나라였을까요], [240907], [A-1] 처럼 다양하게 만들 수 있습니다. 단, 숫자로만 이루어진 평가 코드는 사용할 수 없습니다.")

# 평가 코드 입력
    with st.container(border=True):
        st.caption("평가 코드")
        settingname = st.text_input("평가 코드를 만들어주세요.")

# 평가 코드 등록        
        settingnameinput = st.button("평가 코드 등록하기")
        if settingnameinput:
            if is_code_duplicate(settingname):
                        st.error(f"'{settingname}'  은/는 이미 존재하는 평가 코드입니다. 다른 코드를 입력해 주세요.")
            else:
                st.session_state['settingname'] = settingname
                st.session_state['api_key'] = selected_api_key
                st.success(f"'{settingname}' 평가 코드가 성공적으로 등록되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page, disabled=not bool(st.session_state['settingname']))
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 3단계
def step3():
    st.subheader("3단계. 자료 입력하기")
    st.success("서술형 평가에 활용할 자료를 입력해 주세요. 교과서 pdf, 수업 자료 pdf 등을 입력할 수 있습니다. 입력한 자료를 근거로 모범 답안이나 피드백을 생성할 수 있습니다.")

# 자료 등록
    with st.container(border=True):
        st.caption("자료")

# 기존 벡터 스토어 ID (파일을 가져올 스토어)
        vectorstoreid = st.session_state['vectorstoreid']

# 새로운 벡터 스토어 생성
        if st.button("새로운 자료 저장소 생성"):
            newvectorstore = client.beta.vector_stores.create(name="새로운 벡터 스토어")
            newvectorstoreid = newvectorstore.id
            st.session_state['vectorapi'] = newvectorstoreid

# 새로운 벡터 스토어를 기존 어시스턴트에 업데이트
            client.beta.assistants.update(
                assistant_id=st.session_state['assiapi'],
                tool_resources={"file_search": {"vector_store_ids": [st.session_state['vectorapi']]}})

# 기존 벡터 스토어에서 파일 목록 가져오기
            source_files = client.beta.vector_stores.files.list(vector_store_id=vectorstoreid)

# 파일 목록이 리스트 형식으로 반환되었는지 확인 후 복사
            if hasattr(source_files, 'data'):
                for file in source_files.data:
                    
# 기존 벡터 스토어의 파일을 새 벡터 스토어에 추가
                    client.beta.vector_stores.files.create(
                        vector_store_id=newvectorstoreid,
                        file_id=file.id
                    )
                    time.sleep(1)  # 각 파일 복사 후 잠깐 대기

                st.success("모든 파일이 새로운 자료 저장소로 성공적으로 복사되었습니다.")
            else:
                st.error("파일 목록을 가져오지 못했습니다.")

# 새로운 자료 등록하기
        uploaded_file = st.file_uploader("자료를 입력하세요.", label_visibility="collapsed")
        run_file_button = st.button('자료 등록하기')

        if uploaded_file is not None and run_file_button:
            uploaded_file_response = client.files.create(
                file=uploaded_file,
                purpose="assistants")

            client.beta.vector_stores.files.create(
                vector_store_id=st.session_state['vectorstoreid'],
                file_id=uploaded_file_response.id)
            
            st.success("자료가 성공적으로 등록되었습니다.")

# # 등록된 자료 확인(현재 기능을 제공하지 않음.)
#         filelist = st.checkbox("등록된 자료 목록(확인 후에는 체크 박스를 해제 해주세요.)")
        
#         if filelist:
#             client.beta.threads.messages.create(
#                 thread_id=st.session_state['usingthread'],
#                 role="user",
#                 content="st.session_state['vectorstoreid']을 file search합니다. st.session_state['vectorstoreid']에 있는 파일 이름을 오름차순으로 정리합니다. 파일 이름은 파일 확장자 부분을 제거한 다음 한 줄에 하나씩 줄 바꿈해서 제시합니다. 다른 문장은 넣지 말고 파일 이름만 제시합니다. 5번 이상 반복적으로 file search한 다음 제시합니다. 분명히 있을 거니까 꼭 찾아보고 알려주세요.")
            
#             run = client.beta.threads.runs.create(
#                 thread_id=st.session_state['usingthread'],
#                 assistant_id=assistant_id)
            
#             run_id = run.id

#             while True:
#                 run = client.beta.threads.runs.retrieve(
#                     thread_id=st.session_state['usingthread'],
#                     run_id=run_id)
#                 if run.status == "completed":
#                     break
#                 else:
#                     time.sleep(2)
                    
#             thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
#             msg = thread_messages.data[0].content[0].text.value
#             st.text(msg)

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page)
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 4단계
def step4():
    st.subheader("4단계. 평가 문항 및 주의사항 입력하기")
    st.error("서술형 평가 문항과 모범답안(선택 사항)을 입력하세요. 최대 3개 문항까지 입력 가능합니다. 모범답안의 경우 선택 사항으로 모범답안을 입력하지 않으면 자동으로 모범답안을 생성합니다. 평가 주의사항을 입력하면 이를 근거로 채점 및 피드백을 생성할 수 있습니다.")
    new_thread = client.beta.threads.create()
    st.session_state['usingthread'] = new_thread.id
    
 # 문항 및 모범답안 입력
    with st.container(border=True):
        st.caption("평가 문항 및 모범답안")
        col1, col2 = st.columns(2)
        with col1:
            question1 = st.text_area("1번 문항")
            image1 = st.file_uploader("1번 문항 이미지 자료 첨부", type=["jpg", "jpeg", "png"], key="q1_image")
            st.divider()
            
            question2 = st.text_area("2번 문항")
            image2 = st.file_uploader("2번 문항 이미지 자료 첨부", type=["jpg", "jpeg", "png"], key="q2_image")
            st.divider()
            
            question3 = st.text_area("3번 문항")
            image3 = st.file_uploader("3번 문항 이미지 자료 첨부", type=["jpg", "jpeg", "png"], key="q3_image")
            st.divider()
            
        with col2:
            correctanswer1 = st.text_area("1번 모범답안")
            st.divider()
            correctanswer2 = st.text_area("2번 모범답안")
            st.divider()
            correctanswer3 = st.text_area("3번 모범답안")
            st.divider()

    # 문항 및 모범답안 등록
    question_input_button = st.button('평가 문항 및 모범답안 등록하기')

    if question_input_button:
        st.session_state['question1'] = question1
        st.session_state['question2'] = question2
        st.session_state['question3'] = question3
        st.session_state['correctanswer1'] = correctanswer1
        st.session_state['correctanswer2'] = correctanswer2
        st.session_state['correctanswer3'] = correctanswer3
        
        # 이미지가 업로드된 경우 구글 드라이브에 저장하고 ID를 세션 상태에 저장
        for idx, (img, q_key) in enumerate([(image1, "q1_image_id"), (image2, "q2_image_id"), (image3, "q3_image_id")], 1):
            if img:
                image_id = upload_image_to_drive(drive_service, img)  # 구글 드라이브에 이미지 업로드
                st.session_state[q_key] = image_id  # 세션 상태에 이미지 ID 저장
                st.success(f"{idx}번 문항의 이미지가 성공적으로 등록되었습니다. 파일 ID: {image_id}")

        st.success("문항 및 모범답안이 성공적으로 등록되었습니다.")

# 평가 주의사항 입력
    with st.container(border=True):
        st.caption("평가 주의사항")
        st.write("""
        평가 주의사항을 입력할 때 다음과 같은 점을 고려할 수 있습니다.

        1. 피드백 분위기: 피드백 말투, 긍정/부정 등
        2. 채점 방법: 모범답안을 생성하여 채점, 모범답안 생성 없이 채점, 개별적으로 기준 만들어서 채점, 절대평가로 채점 등
        3. 점수 구분: 3단계, 5단계 등
        4. 피드백 구성: 피드백 문단 구성
        5. 점수 구분별 주된 피드백 내용: 점수 구분에 따라 다른 피드백 내용 구성 
        6. 기타 사항
        """)

        feedbackinstruction = st.text_area("평가 주의사항")
        st.divider()

# 평가 주의사항 등록
        feedbackinstruction_input_button = st.button('평가 주의사항 등록하기')

        if feedbackinstruction_input_button:
            st.session_state['feedbackinstruction'] = feedbackinstruction
            st.success("평가 주의사항이 성공적으로 등록되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page)
    
    with col3:
        st.button("처음 화면으로", on_click=go_home)
# 5단계

def step5():
    st.subheader("5단계. 평가 확인 및 저장하기")
    st.warning("선생님이 만든 서술형 평가를 확인하고 저장합니다. 수정이 필요하다면 이전 단계로 돌아가서 다시 입력한 다음 저장합니다.")

# 설정 확인
    with st.container(border=True):
        st.caption("평가 확인")
        testcheck = st.button("평가 확인")

        if testcheck:
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 문항과 모범답안을 새롭게 등록합니다.' 
                        '기존 평가 문항과 모범답안은 지우고 지금부터 입력한 것을 기억합니다.'
                        '1번 문항은 <' + st.session_state['question1'] +'> 입니다.'
                        'user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer1'] + '> 입니다.'
                        '2번 문항은 <' + st.session_state['question2'] + '> 입니다.'
                        'user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer2'] + '> 입니다.' 
                        ' 3번 문항은 <' + st.session_state['question3'] + '> 입니다.' 
                        'user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer3'] + '> 입니다.')
                    
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 주의사항은 <' + st.session_state['feedbackinstruction'] + '> 입니다.' 
                        '피드백을 제공할 때 입력한 평가 주의사항을 고려해서 작성해주시기 바랍니다.'
                        '만약 특별히 입력한 평가 주의사항이 없다면 ** instructions에 있는 평가 주의사항을 고려해서 작성해주시기 바랍니다.')
            
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='현재 업로드된 서술형 평가 문항, 모범답안, 평가 주의사항을 모두 보여주세요. user(teacher)가 입력한 평가 문항을 있는 그대로 보여주세요. 만약 user(teacher)가 입력한 모범답안이 있으면 user(teacher)가 입력한 것을 있는 그대로 보여줍니다. 만약 user(teacher)가 입력한 모범답안이 없으면 벡터 스토어를 검색하여 문항과 관련된 내용을 찾아 모범답안을 만듭니다. *** 참조 링크 없이, 파일에 적혀 있는 페이지 번호를 있는 그대로 보여주세요. "쪽" 이라는 단어를 사용합니다. 벡터 스토어에서 서술형 문항과 관련된 입력한 파일에서 내용을 찾을 수 없다면 "관련된 내용을 찾을 수 없습니다."라고 보여주세요. ** 반드시 벡터 스토어를 검색하여 서술형 문항과 관련된 내용을 찾는 과정을 거쳐야 합니다. 반드시 벡터 스토어에 있는 파일 내용으로 모범답안을 작성해야 합니다. 반드시 벡터 스토어에 있는 파일 수준으로 모범답안을 작성해야 합니다. 벡터 스토어를 검색했을 때 여러 파일에서 관련된 내용을 찾을 수 있다면 여러 파일의 내용을 종합적으로 활용합니다. ** 어떤 파일에서 어떤 페이지를 보면 되는지 함께 보여주세요. 이때, 반드시 파일 이름과 함께 **그 파일 안에 적혀있는 페이지 숫자**를 보여주어야 합니다. **문단을 나눠서 서술형 평가 문항과 모범답안을 함께 보여줍니다. 서술형 평가 문항과 모범답안을 보여줄 때 **줄을 바꿔서** 구분하여 보기 쉽게 보여줍니다. 【6:7†1-1】처럼 출처를 표시하지 않고, 파일 이름과 페이지 수를 있는 그대로 보여주세요.')
            
            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id)
                
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            msg = thread_messages.data[0].content[0].text.value
            st.write(msg)


# 설정 저장
    with st.container(border=True):
        st.caption("설정 저장하기")
        savesetting = st.button("설정 저장하기")

        if savesetting:
            credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/spreadsheets"
            ])
            gc = gspread.authorize(credentials)
            spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
            worksheet = spreadsheet.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([
            current_time, 
            st.session_state['settingname'], 
            st.session_state['question1'], 
            st.session_state['question2'], 
            st.session_state['question3'], 
            st.session_state['correctanswer1'], 
            st.session_state['correctanswer2'], 
            st.session_state['correctanswer3'], 
            st.session_state['feedbackinstruction'],
            st.session_state['assiapi'],
            st.session_state['vectorapi']])
            st.success("설정이 성공적으로 저장되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 3 ])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("처음 화면으로", on_click=go_home) 

    with col3:
        st.write()

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
elif current_page == 4:
    step4()
elif current_page == 5:
    step5()