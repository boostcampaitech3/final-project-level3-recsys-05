from typing import List
from pydantic import BaseModel, Field

title="SantaBOJ"

description = """
SantaBOJ 추천 결과 반환 API

## models

추천 결과를 요청 받을 수 있음

"""

docs_url="/"

redoc_url=None

class ModelOutput(BaseModel):
    model_type: str= Field(description='추천 모델 타입')
    output: str = Field(description='추천 결과(모델)')

class Input(BaseModel):
    key: int= Field(description='인증을 위한 key 값')
    username: str= Field(description='추천을 위한 유저아이디')

class Output(BaseModel):
    problems: List[ModelOutput] = Field(description='''
    추천 결과(종합) / 
    Not-Found-Key : key 값 오류 / 
    Not-Found-User : 맞지 않는 유저 / 
    Not-Found-User-Solved-Problem : 맞은 문제가 없는 유저 / 
    Not-Found-User-Lately-Solved-Problem : 최근에 푼 문제에 우리 문제 리스트에 속한 문제가 없는 유저
    ''')
    tag: List[str] = Field(description='추천 태그')
