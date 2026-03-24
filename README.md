# awsps

AWS Identity Center(SSO) Permission Set CLI

브라우저로 SSO 로그인 후, Account와 Permission Set을 인터랙티브하게 선택하면 임시 자격증명이 현재 쉘에 설정됩니다.

## 설치

### pip / pipx (추천)

```bash
pip install awsps

# 또는 pipx (격리된 환경에 설치)
pipx install awsps
```

### Homebrew

```bash
brew tap boseung-code/tap
brew install awsps
```

### 소스에서 설치

```bash
git clone https://github.com/boseung-code/awsps.git
cd awsps
pip install -e .
```

## 초기 설정

```bash
awsps configure --start-url https://your-org.awsapps.com/start --region ap-northeast-2
```

## 사용법

### 방법 1: Shell 함수 등록 (추천)

`.bashrc` 또는 `.zshrc`에 아래 한 줄을 추가합니다:

```bash
eval "$(awsps init)"
```

이후 쉘을 새로 열거나 `source ~/.bashrc`를 실행하면, 다음 명령어를 바로 사용할 수 있습니다:

```bash
# SSO 로그인 + Account/Permission Set 선택
awsps login

# Account/Permission Set 재선택 (재로그인 없이)
awsps sw
```

### 방법 2: eval 직접 사용

Shell 함수를 등록하지 않고도 사용할 수 있습니다:

```bash
# SSO 로그인 + Account/Permission Set 선택
eval $(awsps _login)

# Account/Permission Set 재선택
eval $(awsps _sw)
```

## 사용 후

자격증명이 설정된 상태에서 AWS CLI, Terraform 등을 바로 사용할 수 있습니다:

```bash
aws s3 ls
aws sts get-caller-identity
terraform plan
```

## 명령어 요약

| 명령어 | 설명 |
|---|---|
| `awsps configure` | SSO 시작 URL, 리전 설정 저장 |
| `awsps login` | SSO 로그인 + 자격증명 선택 (Shell 함수 필요) |
| `awsps sw` | Account/Permission Set 재선택 (Shell 함수 필요) |
| `awsps init` | Shell 함수 출력 |
| `awsps _login` | login 내부 명령 (eval과 함께 사용) |
| `awsps _sw` | sw 내부 명령 (eval과 함께 사용) |
