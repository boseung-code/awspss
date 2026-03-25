# awspss

AWS Identity Center Permission Sets Switcher

브라우저로 SSO 로그인 후, Account와 Permission Set을 인터랙티브하게 선택하면 임시 자격증명이 현재 쉘에 설정됩니다.

## 설치

### pip / pipx

```bash
pip install awspss

# 또는 pipx (격리 환경 설치)
pipx install awspss
```

### Homebrew

```bash
brew tap boseung-code/tap
brew install awspss
```

### 소스에서 설치

```bash
git clone https://github.com/boseung-code/awspss.git
cd awspss
pip install -e .
```

## 설정

### 방법 1: 인터랙티브

```bash
awspss configure
```

start-url과 region을 순서대로 물어봅니다.

### 방법 2: 직접 입력

```bash
awspss configure --start-url https://your-org.awsapps.com/start --region ap-northeast-2
```

## 사용법

### Shell 함수 등록 (추천)

`.bashrc` 또는 `.zshrc`에 아래 한 줄을 추가합니다:

```bash
eval "$(awspss init)"
```

쉘을 새로 열거나 `source ~/.bashrc` 후 사용:

```bash
# SSO 로그인 + Account/Permission Set 선택
awspss login

# 다른 Account/Permission Set으로 전환 (재로그인 없음)
awspss sw
```

### eval 방식

Shell 함수 등록 없이도 사용할 수 있습니다:

```bash
eval $(awspss login)
eval $(awspss sw)
```

### 자격증명 확인

```bash
aws sts get-caller-identity
aws s3 ls
terraform plan
```

## 명령어

| 명령어 | 설명 |
|---|---|
| `awspss configure` | SSO 접속 정보 설정 |
| `awspss login` | SSO 로그인 + 자격증명 발급 |
| `awspss sw` | 자격증명 전환 (재로그인 없음) |
| `awspss init` | Shell 함수 출력 |
