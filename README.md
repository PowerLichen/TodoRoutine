# ToDo Routine Service
## 소개
매 주마다 해야할 일정을 기록 및 관리하는 서비스.

## (Required) Project Settings
시작 전, `config` 폴더 내부에 `.env` 파일을 다음 양식과 같이 작성합니다.

docker compose를 통해 바로 백엔드 서버를 실행할 수 있도록 작성해두었습니다.

본 프로젝트는 데이터베이스로 `PostgreSQL`을 사용하였습니다.

```
SECRET_KEY=vq760%j^+-=xxj4jgozdyhq5vsl@wha&cr3$p@skw97i222pq
POSTGRES_USER=username
POSTGRES_PASSWORD=userpassword
POSTGRES_DB=database_name
TZ=Asia/Seoul
```

## Start Project
최상위 폴더에서 다음 명령어를 수행합니다.
```
docker compose --env-file ./config/.env up --build
```

API 문서 링크: http://127.0.0.1:8000/docs/swagger/#/

## Test
django 서버 컨테이너에 접속하여 다음과 같은 명령어를 수행합니다.

```
pipenv install --system --dev
python manage.py test
```