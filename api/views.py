from django.shortcuts import render
import requests
from .models import FoodSafetyData
from .forms import SearchForm
from django.conf import settings
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

def fetch_data(request):
    # 비밀번호 확인
    if request.method == 'POST' and 'password' in request.POST:
        entered_password = request.POST['password']
        if entered_password == settings.AUTHORIZED_PASSWORD:
            request.session['authorized'] = True
            logger.info("비밀번호 인증 성공")
        else:
            request.session['authorized'] = False
            logger.warning("비밀번호 인증 실패")
    
    # 인증 여부 확인
    if not request.session.get('authorized', False):
        return render(request, 'api/index.html', {'authorized': False})
    
    # 폼 처리
    form = SearchForm(request.POST or None)

    # 기본값 설정
    startIdx = 1
    endIdx = 1000

    if form.is_valid():
        startIdx = form.cleaned_data['start_idx']
        endIdx = form.cleaned_data['end_idx']

    # API 호출
    keyId = settings.API_KEY  # API 키
    serviceId = 'I2861'  # 서비스 ID
    dataType = 'json'  # 응답 형식

    base_url = f"http://openapi.foodsafetykorea.go.kr/api/{keyId}/{serviceId}/{dataType}/{startIdx}/{endIdx}"

    try:
        # API 호출
        response = requests.get(base_url)
        response.raise_for_status()  # 요청 오류 시 예외 발생

        # API 응답 로그 출력
        logger.info(f"API 응답 상태 코드: {response.status_code}")
        logger.info(f"API 응답 내용: {response.text}")

        # JSON 데이터 처리
        data = response.json()

        if 'I2861' in data and 'row' in data['I2861']:
            items = data['I2861']['row']
            logger.info(f"API에서 반환된 데이터: {items}")
            
            # 데이터베이스에 저장
            for item in items:
                FoodSafetyData.objects.update_or_create(
                    LCNS_NO=item.get('LCNS_NO'),
                    defaults={
                        'BSSH_NM': item.get('BSSH_NM'),
                        'INDUTY_CD_NM': item.get('INDUTY_CD_NM'),
                        'TELNO': item.get('TELNO'),
                        'SITE_ADDR': item.get('SITE_ADDR'),
                        'CHNG_DT': item.get('CHNG_DT'),
                        'CHNG_BF_CN': item.get('CHNG_BF_CN'),
                        'CHNG_AF_CN': item.get('CHNG_AF_CN'),
                        'CHNG_PRVNS': item.get('CHNG_PRVNS'),
                    }
                )

        else:
            items = []
            logger.info("API에서 반환된 데이터가 없습니다.")

        # 템플릿에 데이터 전달
        return render(request, 'api/index.html', {'data': items, 'authorized': True, 'form': form})

    except requests.exceptions.RequestException as e:
        logger.error(f"API 요청 중 오류 발생: {str(e)}")
        return render(request, 'api/index.html', {'data': [], 'authorized': True, 'form': form})