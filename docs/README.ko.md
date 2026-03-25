# awspss

AWS Identity Center Permission Sets Switcher

[English](../README.md)

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

## 초기 설정

### 1. Shell 함수 등록

`awspss login`과 `awspss sw`가 현재 쉘에 자격증명을 직접 설정하려면 shell 함수 등록이 필요합니다.

```bash
eval "$(awspss init)"
```

실행하면:
1. 현재 쉘에 맞는 rc 파일(`.bashrc` 또는 `.zshrc`)을 감지
2. 등록 여부를 물어봄
3. rc 파일에 자동 추가 + 현재 쉘에 즉시 적용

이미 등록된 경우 중복 추가하지 않습니다. 새 터미널에서도 자동으로 활성화됩니다.

수동으로 등록하려면 `.bashrc` 또는 `.zshrc`에 직접 추가:

```bash
eval "$(awspss init --print)"
```

### 2. SSO 접속 정보 설정

```bash
awspss configure
```

start-url과 region을 순서대로 물어봅니다. 직접 입력도 가능합니다:

```bash
awspss configure --start-url https://your-org.awsapps.com/start --region ap-northeast-2
```

## 사용법

### 로그인

```bash
awspss login
```

항상 브라우저에서 SSO 재인증을 수행합니다. 인증 후 Account → Permission Set을 선택하면 자격증명이 현재 쉘에 설정됩니다.

### 자격증명 전환

```bash
awspss sw
```

캐시된 토큰을 사용하여 재로그인 없이 다른 Account/Permission Set으로 전환합니다. 토큰이 만료된 경우 자동으로 재로그인합니다.

### Shell 함수 미등록 시 (eval 방식)

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

### 자격증명 해제

```bash
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
```

## 명령어

| 명령어 | 설명 |
|---|---|
| `awspss init` | Shell 함수 등록 (rc 파일 자동 추가 + 즉시 적용) |
| `awspss init --print` | Shell 함수 출력만 (수동 등록용) |
| `awspss configure` | SSO 접속 정보 설정 |
| `awspss login` | SSO 로그인 (항상 재인증) |
| `awspss sw` | 계정/Permission Set 전환 (캐시된 토큰 사용) |
