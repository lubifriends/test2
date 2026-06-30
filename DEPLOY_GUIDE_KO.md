# GitHub + Streamlit Community Cloud 처음부터 배포하기

이 문서는 PowerShell을 사용하지 않습니다. 가장 실수하기 쉬운 Git 명령어 대신 GitHub 웹사이트에서 파일을 올리는 방법을 기준으로 설명합니다.

## 결론부터

현재 저장소의 브랜치와 파일 상태가 헷갈린다면 **새 GitHub 저장소와 새 Streamlit 앱을 만드는 방법이 가장 안전합니다.** 기존 저장소와 기존 사이트는 새 사이트가 정상 작동한 뒤에 삭제하세요.

## 1. GitHub에 올릴 파일 준비

다음 파일과 폴더만 올립니다.

```text
app.py
database.py
mock_data.py
scoring.py
requirements.txt
README.md
DEPLOY_GUIDE_KO.md
run_dashboard.bat
.gitignore
.env.example
collectors/
  __init__.py
  google_trending_now.py
  naver_datalab.py
  translator.py
```

다음 항목은 올리지 않습니다.

```text
.venv/
venv/
__pycache__/
trends.db
.env
.streamlit/secrets.toml
work/
outputs/
.agents/
.codex/
```

`NAVER_CLIENT_ID`와 `NAVER_CLIENT_SECRET`은 네이버 로그인 아이디와 비밀번호가 아닙니다. 네이버 개발자 센터에서 발급한 API 자격 증명이며, GitHub 파일 안에 적으면 안 됩니다.

## 2. 새 GitHub 저장소 만들기

1. [GitHub](https://github.com/)에 로그인합니다.
2. 오른쪽 위 `+`를 누르고 `New repository`를 선택합니다.
3. Repository name에 예를 들어 `asia-trend-dashboard`를 입력합니다.
4. 외부 공개 사이트라면 `Public`을 선택합니다.
5. `Add a README file`, `.gitignore`, `license`는 모두 선택하지 않습니다.
6. `Create repository`를 누릅니다.

빈 저장소로 만들면 첫 브랜치는 파일을 처음 업로드할 때 생성됩니다. 기본 브랜치가 `main`인지 업로드 후 저장소 왼쪽 위 브랜치 표시에서 확인합니다.

## 3. 파일 업로드

1. 새 저장소 화면에서 `uploading an existing file`을 누릅니다. 이미 파일이 있다면 `Add file` → `Upload files`를 누릅니다.
2. 준비한 루트 파일들과 `collectors` 폴더를 업로드 영역으로 끌어놓습니다.
3. 업로드 목록에 `collectors/translator.py`와 `collectors/__init__.py`가 있는지 반드시 확인합니다.
4. Commit message에 `Initial Streamlit dashboard`를 입력합니다.
5. `Commit directly to the main branch`를 선택하고 커밋합니다.

ZIP 파일 자체를 GitHub에 올리면 안 됩니다. ZIP을 컴퓨터에서 먼저 풀고, 풀린 파일들을 업로드해야 합니다.

## 4. Streamlit Community Cloud에서 새 사이트 만들기

1. [Streamlit Community Cloud](https://share.streamlit.io/)에 GitHub 계정으로 로그인합니다.
2. `Create app` → `Yup, I have an app`을 선택합니다.
3. 다음과 같이 지정합니다.

```text
Repository: 내아이디/asia-trend-dashboard
Branch: main
Main file path: app.py
```

4. `Advanced settings`를 엽니다.
5. Python version은 `3.12`를 선택합니다.
6. 네이버 API를 사용할 경우 Secrets 칸에 아래처럼 넣습니다.

```toml
NAVER_CLIENT_ID = "네이버에서_발급받은_ID"
NAVER_CLIENT_SECRET = "네이버에서_발급받은_SECRET"
```

네이버 API 키가 없어도 샘플 데이터로 사이트는 실행됩니다. 일본어 키워드 번역에도 별도 API 키가 필요하지 않습니다.

7. `Save` 후 `Deploy`를 누릅니다.

## 5. 사이트가 터졌을 때 확인하는 곳

사이트 오른쪽 아래 `Manage app`을 누르면 로그를 볼 수 있습니다. 오류별 조치는 다음과 같습니다.

- `No module named 'collectors.translator'`: `collectors/translator.py`가 빠졌습니다.
- `cannot import name 'get_translations'`: GitHub의 `database.py`가 구버전입니다.
- `No module named 'plotly'` 또는 `No module named 'streamlit_autorefresh'`: `requirements.txt`가 루트에 없거나 구버전입니다.
- `File does not exist: app.py`: Main file path가 잘못되었습니다. `app.py`로 수정합니다.
- 수정했는데 예전 오류가 계속됨: Streamlit 앱 설정에서 `Reboot app`을 실행합니다.

이 프로젝트는 번역 관련 파일이 누락돼도 일본어 원문으로 대체하도록 방어되어 있습니다. 그래도 모든 기능을 사용하려면 최신 `app.py`, `database.py`, `collectors/translator.py`를 함께 업로드해야 합니다.

## 6. 이후 수정하는 방법

기존 GitHub 파일을 먼저 삭제할 필요가 없습니다.

1. 저장소에서 `Add file` → `Upload files`를 누릅니다.
2. 수정한 파일을 같은 경로와 같은 이름으로 업로드합니다.
3. 새 파일은 추가되고, 같은 이름의 파일은 새 내용으로 반영됩니다.
4. `Commit directly to the main branch`로 커밋합니다.
5. Streamlit은 연결된 `main` 브랜치의 변경을 감지해 자동으로 다시 배포합니다.

폴더 구조를 바꾸거나 완전히 없어진 파일만 별도로 삭제하면 됩니다. 정상 동작하는 기존 파일을 전부 지웠다가 다시 올리는 방식은 파일 누락 가능성이 커서 권장하지 않습니다.

## 7. CMD에서 로컬 실행하기

명령 프롬프트(CMD)를 열고 다음을 순서대로 실행합니다. PowerShell 활성화 명령은 필요 없습니다.

```bat
cd /d "프로젝트_폴더_전체_경로"
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

이미 `.venv`가 있으면 두 번째 줄은 생략해도 됩니다. 또는 프로젝트 폴더의 `run_dashboard.bat`을 더블클릭해 실행할 수 있습니다.
