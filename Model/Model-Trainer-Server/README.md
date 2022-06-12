# Model-Trainer-Server
모델 학습을 위한 모델별 학습 템플릿이 저장된 폴더

### Usage
해당 폴더에서 Airflow 실행시 dags와 연동되어 모델을 주기적으로 학습할 수 있음
- `pip install pip --upgrade`
- `pip install apache-airflow==2.2.0`
- `export AIRFLOW_HOME=.`
- `airflow db init`
- `airflow user create`
- `airflow webserver`
- `airflow schedyler`

### 모델 학습 파이프라인
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173225437-fafc3349-b627-4437-b752-bd1ee736d1a4.png" /></p>
