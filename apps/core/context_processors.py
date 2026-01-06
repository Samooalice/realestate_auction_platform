from django.conf import settings


def site_settings(request):
    """전역 사이트 설정을 템플릿에 전달"""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', '부동산 경매 컨설팅'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
        'CONTACT_PHONE': getattr(settings, 'CONTACT_PHONE', ''),
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', ''),
        'KAKAO_CHANNEL': getattr(settings, 'KAKAO_CHANNEL', ''),
    }
