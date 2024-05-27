# MementoAI

## **1. 프로젝트에 대한 설명**

이 프로그램은 URL 단축 서비스를 제공하는 FastAPI 기반의 웹 애플리케이션입니다. 사용자가 원하는 URL을 입력하면 이를 단축하여 새로운 짧은 URL을 생성해주고, 이를 통해 기존 URL로 리디렉션하는 기능을 제공합니다.

1. **URL 입력**: 사용자는 URLShortenRequest 모델을 통해 원본 URL과 만료 시간(선택 사항)을 입력합니다.
2. **Short Key 생성**: 입력받은 원본 URL에 대해 무작위한 문자열을 생성하여 고유한 단축 키(short key)를 만듭니다. 이 단축 키는 중복되지 않도록 데이터베이스에 저장됩니다.
3. **Short URL 반환**: 단축 키가 생성되면 사용자에게 이를 포함한 Short URL을 반환합니다.
4. **리디렉션**: 사용자가 Short URL을 요청하면 해당 URL에 대한 원본 URL로의 리디렉션을 수행합니다.
5. **통계 제공**: 생성된 단축 URL에 대한 통계 정보를 제공합니다. 현재까지의 방문 횟수 등을 확인할 수 있습니다.

단축 키 생성은 다음과 같이 이루어집니다 :
- URL에 대한 단축 키는 알파벳 대소문자와 숫자로 이루어진 무작위 문자열입니다.
- 중복을 피하기 위해 생성된 단축 키가 이미 데이터베이스에 있는지 확인하고, 없을 경우에만 사용됩니다.

**SQLite를 사용한 이유** :
- 프로젝트 규모, 사용자 수 등.. 조건이 없어 개발 초기 단계나 작은 규모의 애플리케이션으로 가정하였습니다.
- 만약 프로젝트가 대규모 혹은 많은 사용자가 고려해야 될 상황이 온다면, ORM을 사용하기 때문에 기존 데이터를 Json 형태로 import/export로 백업이 가능하고 셋팅된 DB 정보를 변경이 가능하다고 생각했습니다.


## **2. 설치**

### Windows:

1. 먼저 Python 다운로드 페이지(https://www.python.org/downloads/)에서 Python 3.8 설치 프로그램을 다운로드합니다.
2. 다운로드한 설치 프로그램을 실행하여 Python 3.8을 설치합니다. 설치 중에 "Add Python 3.x to PATH" 옵션을 선택해야 합니다.
3. 설치가 완료되면 명령 프롬프트를 열고 `python --version` 명령어를 실행하여 Python 버전이 3.8.x로 나오는지 확인합니다.
4. `pip install -r requirements.txt` 명령어를 사용하여 패키지를 설치합니다.

### macOS:

1. macOS에는 기본적으로 Python이 설치되어 있지만, Python 3.8을 사용하려면 다음과 같이 설치합니다.
   ```
   brew install python@3.8
   ```
2. Python 3.8이 설치되면 터미널에서 `python3 --version` 명령어를 실행하여 버전이 3.8.x로 나오는지 확인합니다.
3. `pip install -r requirements.txt` 명령어를 사용하여 패키지를 설치합니다.

### Linux:

1. 대부분의 Linux 배포판에는 Python이 기본적으로 설치되어 있습니다. 그러나 Python 3.8을 사용하려면 다음과 같이 설치합니다.
   ```
   sudo apt update
   sudo apt install python3.8
   ```
2. Python 3.8이 설치되면 터미널에서 `python3 --version` 명령어를 실행하여 버전이 3.8.x로 나오는지 확인합니다.
3. `pip install -r requirements.txt` 명령어를 사용하여 패키지를 설치합니다.


## **3. 실행 방법**

1. FastAPI 서버 실행
  ```
    uvicorn main:app --reload
   ```
2. Swagger
  - http://127.0.0.1:8000/docs 로 접속하여 Swagger UI를 통해 API를 테스트할 수 있습니다.

3. 단위 테스트 및 통합 테스트
  ```
    pytest test.py
   ```