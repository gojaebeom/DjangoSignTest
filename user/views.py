from django.shortcuts import redirect, render


# 3. 유저모델을 views(컨트롤러에서 사용하기 위해 불러옵니다.)
from .models import User
# 4. 회원가입 때 입력한 비밀번호는 그대로 들어가게되면 보안에 큰 문제가 됩니다.
# 비밀번호를 단반향 암호화 시키는 bcrypt 라이브러리를 사용하기 위해 불러와줍니다.
import bcrypt

# 5. 이번 예제에서 사용할 view들을 작성해줍니다.
# 회원가입
def join(request):
    # POST로 요청이 왔다는 것은 생성하기 버튼을 클릭했다는 것
    # 즉 데이터를 받아 데이터베이스에 넣어주어야한다.
    if request.POST:
        user = User()
        user.email = request.POST['email']
        password = request.POST['password']
        encode_password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        user.password = encode_password
        user.nickname = request.POST['nickname']

        user.save()

        return redirect('/login')
    
    # POST로 온요청이 아니라면 (GET 방식이라면) 단순히 회원가입 페이지를 요청
    # 회원가입 페이지를 보여주는 코드를 작성
    return render(request, 'join.html')

# 로그인
def login(request):
    # POST로 요청이 왔다는 것은 로그인하기 버튼을 클릭했다는 것
    # 즉 데이터를 받아 데이터베이스에 넣어주어야한다.
    if request.POST:

        # email을 조회하여 존재하지 않는다면?
        if not User.objects.filter(email=request.POST['email']):
            print('존재하지 않는 계정입니다!')
            return render(request, 'login.html', context={'login_false':'존재하지 않는 계정입니다.'})
        
        # 위의 if 문에 걸러지지 않았다면 email이 존재
        # email에 해당하는 user의 암호화된 password를 가져와 입력받은 값이 암호화된 비밀번호와 일치하는지 확인
        find_user = User.objects.get(email=request.POST['email'])

        if not bcrypt.checkpw(request.POST['password'].encode('utf-8'), find_user.password.encode('utf-8')):
            print('비밀전호가 일치하지 않습니다!')
            return render(request, 'login.html', context={'login_false':'비밀번호가 일치하지 않습니다.'})
        
        # 위 if 필터들을 통과했다면 정상적인 로그인 
        # user라는 세션을 만들어주고 필요한 데이터들을 저장
        # session에 유저정보를 저장하면 어느 template 단에서든 user 세션을 사용할 수 있다. (세션이 만료되거나, 삭제되기 전까지)
        request.session['user'] = {'id':find_user.id,'nickname':find_user.nickname, 'email':find_user.email}
        return redirect('/')
    
    # POST로 온요청이 아니라면 (GET 방식이라면) 단순히 로그인 페이지를 요청
    # 로그인 페이지를 보여주는 코드를 작성 
    return render(request, 'login.html')

# 로그아웃
def logout(request):
    # 세션의 값을 비우고
    request.session['user']={}
    # 세션이 수정되었다는 것을 알림
    request.session.modified = True
    return redirect('/')

# 홈화면
def home(request):
    return render(request, 'home.html')



