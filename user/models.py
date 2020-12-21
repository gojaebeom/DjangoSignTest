from django.db import models

# 2. 사용할 회원 모델을 만들어줍니다.
class User(models.Model):
    # id 칼럼은 따로 생성하지 않아도 장고가 알아서 생성해줌
    #id = models.IntegerField(primary_key=True)

    # 이메일 : 문자열 길이는 50까지 , 중복 금지
    email = models.EmailField(max_length=50, unique=True)
    # 패스워드 : 문자열 길이는 100까지, null값은 허용하지 않음
    password = models.CharField(max_length=100, null=False)
    # 닉네임 또는 이름 : 문자열 길이는 20까지, null값은 허용하지 않음
    nickname = models.CharField(max_length=20, null=False)
    # 가입 날짜 : 따로 값을 입력받지 않아도 날짜 자동 생성
    join_date = models.DateTimeField(auto_now_add=True)