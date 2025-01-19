from django.conf import settings
import requests
import logging
from .models import FoodSafetyData
from django.shortcuts import render, redirect
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
        # 인증이 안된 상태에서 비밀번호 입력 폼만 보여줌
        return render(request, 'api/index.html', {'authorized': False})
    
    # 인증이 된 경우, 식품 안전 데이터 조회
    keyId = settings.API_KEY  # secrets.json에서 읽은 keyId 사용
    serviceId = 'I2861'  # 서비스 ID
    dataType = 'json'  # 응답 형식
    startIdx = '1'  # 시작 인덱스
    endIdx = '1000'  # 종료 인덱스

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

        # 응답에서 'row' 키를 확인하고, 해당 값이 있는 경우에만 데이터 처리
        if 'I2861' in data and 'row' in data['I2861']:
            items = data['I2861']['row']  # 데이터 항목
            logger.info(f"API에서 반환된 데이터: {items}")
            
            # 데이터베이스에 저장 (필요한 경우)
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
        return render(request, 'api/index.html', {'data': items, 'authorized': True})

    except requests.exceptions.RequestException as e:
        # 요청 중 오류가 발생한 경우
        logger.error(f"API 요청 중 오류 발생: {str(e)}")
        return render(request, 'api/index.html', {'data': [], 'authorized': True})