
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/163712073-7d2dcd09-4c1f-4bab-935f-42de292300bb.png" /></p>

<div align="center">
05 TEAM 알잘딱깔센 <br/>
  
## 산타 백준 - 개인화 코딩 문제 추천 웹서비스
  
</div>

# 🏆️ 프로젝트 소개

<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233157-8f7d9220-0fc3-46ef-803d-07226ca10742.png" /></p>

<div align="center">

### 코딩 테스트를 준비하는 사람들을 위한 실시간 백준 문제 추천 웹서비스
  
</div>

* [![GoogleDrive Badge](https://img.shields.io/badge/REPORT-405263?style=flat-square&logo=Quip&link=https://drive.google.com/file/d/1VnYsB8k4Fxu6UFhAxuTi4m01BjoH2uwS/view?usp=sharing)](https://github.com/boostcampaitech3/final-project-level3-recsys-05/blob/main/RecSys_5%EC%A1%B0_%EC%82%B0%ED%83%80%EB%B0%B1%EC%A4%80_%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C.pdf)
* [![Youtube Badge](https://img.shields.io/badge/Youtube-ff0000?style=flat-square&logo=youtube&link=https://youtu.be/KPS1sD_lcMc)](https://www.youtube.com/watch?v=9IH-vjs3syI)
* [웹사이트](http://34.64.132.163:8888/)

# 💻 활용 장비
- **Ubuntu** 18.04.5 LTS
- **GPU** Tesla V100-PCIE-32GB
- **Google Cloud Platform VM Instance** (Ubuntu, 18.04 LTS)

# 🙋🏻‍♂️🙋🏻‍♀️ 팀 소개
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233642-70776e4b-a8e2-4e1e-8c55-c6f020f738d3.png" /></p>

# 전체 서비스
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233367-f1406c60-0728-4e55-9abe-fcfb9977d45e.png" /></p>

# 사용 데이터
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173243242-dc1b776a-1e5f-4eac-9885-df1d777c8ce8.png" /></p>

# 사용 모델
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233404-0ec09518-daea-4983-872d-d386c1bc1d92.png" /></p>

# 모델 학습 파이프라인
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233413-1682d0d3-17eb-4b34-9df5-61301aabed18.png" /></p>

- 모델 별로 학습 파이프라인을 구축하여, Airflow와 MLflow를 사용해 주기적으로 모델을 학습 및 업데이트

# 모델 API 서버
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233420-59c10b85-f733-414d-9821-68907f299697.png" /></p>

- 백엔드에서 user-id, feedback에 대한 데이터를 받음
- 모델 학습에 필요한 데이터를 실시간으로 수집
- 전처리를 거쳐서 각 모델 별로 후보 추천 리스트를 생성
- 해당 후보 집단 내에서 유저의 전체 풀이 내역을 이용해 한번의 필터링을 거침
- 각 모델에 따른 유저 피드백 정보를 MAB 알고리즘의 일종인 Thompson Sampling의 파라미터로 사용하여 개인화된 추천 결과를 생성

# 데이터 파이프 라인
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233425-8c8be488-e0f2-4811-809b-d4febb7f5f36.png" /></p>

- Airlflow를 이용한 데이터 수집 및 병렬화, Bigquery를 이용한 데이터 관리

# 웹 서비스
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233433-8381b22a-d735-4131-b2bf-c93c786d31ad.png" /></p>

- Spring을 이용하여 웹 구현, 유저 회원 관리 및 유저 피드백 수집

# CI/CD
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233439-a139d874-05b3-4d06-b8dc-545525e8ca93.png" /></p>

- Jenkins를 이용한 CI/CD, Docker를 이용한 원격 배포, 빌드 결과를 Slack으로 알림

# 사용자 요청 흐름도
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173233456-aac88eee-8bc2-41a1-b639-d96a72a7b466.png" /></p>

