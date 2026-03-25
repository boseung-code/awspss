# awspss

AWS Identity Center Permission Sets Switcher

[English](../README.md)

브라우저로 SSO 로그인 후, Account와 Permission Set을 인터랙티브하게 선택하면 임시 자격증명이 현재 쉘에 설정됩니다.

<p align="center">
  <img src="demo.svg" alt="awspss demo" width="620">
</p>

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

`awspss login`과 `awspss sw`가 현재 쉘에 자격증명을 직접 설정하려면 shell 함수 등록이 필요합니다. Tab 자동완성도 함께 활성화됩니다.

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

항상 브라우저에서 SSO 재인증을 수행합니다. 인증 후 Account → Permission Set을 선택하면 자격증명이 현재 쉘에 설정됩니다. 자격증명 만료 시간이 함께 표시됩니다.

### 자격증명 전환

```bash
awspss sw
```

캐시된 토큰을 사용하여 재로그인 없이 다른 Account/Permission Set으로 전환합니다. 토큰이 만료된 경우 자동으로 재로그인합니다.

### 빠른 전환 (Permission Set만)

```bash
awspss sw AdministratorAccess
```

동일 계정 내에서 다른 Permission Set으로 인터랙티브 선택 없이 바로 전환합니다. `awspss sw ` 뒤에 Tab을 누르면 사용 가능한 Permission Set 목록이 자동완성됩니다.

### 현재 자격증명 확인

```bash
awspss whoami
```

현재 AWS 자격증명 정보(Account, ARN, UserId)를 표시합니다.

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
awspss unset
```

### 로그아웃 (캐시 토큰 삭제)

```bash
awspss logout
```

캐시된 SSO 토큰을 삭제합니다. 다음 사용 시 새로 로그인하게 됩니다.

## 명령어

| 명령어 | 설명 |
|---|---|
| `awspss init` | Shell 함수 등록 (rc 파일 자동 추가 + 즉시 적용) |
| `awspss init --print` | Shell 함수 출력만 (수동 등록용) |
| `awspss configure` | SSO 접속 정보 설정 |
| `awspss login` | SSO 로그인 (항상 재인증) |
| `awspss sw` | 계정/Permission Set 전환 (캐시된 토큰 사용) |
| `awspss sw [ROLE]` | Permission Set 빠른 전환 (Tab 자동완성 지원) |
| `awspss whoami` | 현재 AWS 자격증명 정보 표시 |
| `awspss unset` | 현재 쉘의 AWS 자격증명 해제 |
| `awspss logout` | 캐시된 SSO 토큰 삭제 |
