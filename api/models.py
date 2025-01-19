from django.db import models

class FoodSafetyData(models.Model):
    BSSH_NM = models.CharField(max_length=255)  # 업소명
    INDUTY_CD_NM = models.CharField(max_length=255)  # 업종명
    LCNS_NO = models.CharField(max_length=255)  # 인허가번호
    TELNO = models.CharField(max_length=255)  # 전화번호
    SITE_ADDR = models.CharField(max_length=255)  # 주소
    CHNG_DT = models.DateField()  # 변경일자
    CHNG_BF_CN = models.TextField()  # 변경전 내용
    CHNG_AF_CN = models.TextField()  # 변경후 내용
    CHNG_PRVNS = models.TextField()  # 변경사유

    def __str__(self):
        return self.BSSH_NM