# 부동산 경매 컨설팅 플랫폼 - Django 개발 단계별 프로세스

## 프로젝트 개요

- **프로젝트명**: 부동산 경매 컨설팅 플랫폼
- **기술 스택**: Django 5.x, PostgreSQL, HTML/CSS/JS, Bootstrap 5
- **개발 기간**: 10주 (Phase 1~5)

---

## Phase 1: 프로젝트 초기 설정 (1주차)

### 1.1 Django 프로젝트 구조 설정

```
realestate_auction_platform/
├── config/                     # 프로젝트 설정
│   ├── settings/
│   │   ├── base.py            # 공통 설정
│   │   ├── local.py           # 개발 환경
│   │   └── production.py      # 운영 환경
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/              # 회원 관리
│   ├── core/                  # 공통 기능 (메인페이지)
│   ├── company/               # 회사소개
│   ├── services/              # 서비스 안내
│   ├── properties/            # 추천 물건
│   ├── success_cases/         # 성공사례
│   ├── academy/               # 경매 아카데미
│   ├── info_center/           # 정보센터
│   └── consultation/          # 상담신청
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── sidebar.html
│   └── [app별 템플릿]/
├── media/                     # 업로드 파일
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
└── manage.py
```

### 1.2 필수 패키지 설치

```txt
# requirements/base.txt
Django>=5.0
psycopg2-binary          # PostgreSQL
Pillow                   # 이미지 처리
django-crispy-forms      # 폼 스타일링
crispy-bootstrap5
django-allauth           # 소셜 로그인
django-ckeditor          # 에디터
django-environ           # 환경변수
django-debug-toolbar     # 디버깅
celery                   # 비동기 작업
redis                    # 캐시/세션
```

### 1.3 데이터베이스 설계 (ERD)

```
[User] ──1:N── [Consultation]
   │
   └──1:N── [PropertyBookmark]
               │
[Property] ──1:N──┘
   │
   └──N:1── [PropertyCategory]

[SuccessCase] ──N:1── [ServiceCategory]

[Course] ──1:N── [Enrollment]
   │              │
   └──N:1── [User]

[Post] ──N:1── [PostCategory]
```

---

## Phase 2: 핵심 앱 개발 - 기본 구조 (2주차)

### 2.1 accounts 앱 (회원 관리)

#### Models
```python
# apps/accounts/models.py
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20)
    user_type = models.CharField(choices=USER_TYPE_CHOICES)  # 일반/기업
    marketing_agreed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)
    preferred_region = models.CharField()  # 관심 지역
    budget_range = models.CharField()      # 예산 범위
    interest_type = models.CharField()     # 관심 분야
```

#### Views/URLs
- 회원가입: `/accounts/signup/`
- 로그인: `/accounts/login/`
- 소셜 로그인: `/accounts/social/kakao/`, `/accounts/social/naver/`
- 마이페이지: `/accounts/mypage/`
- 프로필 수정: `/accounts/profile/edit/`

### 2.2 core 앱 (메인페이지)

#### 메인페이지 섹션 구성
```
[섹션 1] 히어로 배너 - 슬라이드 4개
[섹션 2] 서비스 하이라이트 - 5대 서비스 아이콘
[섹션 3] 핵심 수치 - 컨설팅 건수, 낙찰액, 고객수 (카운트업)
[섹션 4] 금주 추천물건 - 3~4개 카드 슬라이드
[섹션 5] 성공사례 프리뷰 - 2~3건 요약
[섹션 6] 고객 후기 - 슬라이드
[섹션 7] 왜 우리인가 - 차별화 포인트
[섹션 8] 아카데미 배너
[섹션 9] 최신 콘텐츠 - 블로그 최신글
[섹션 10] 상담 유도 CTA
```

#### Models
```python
# apps/core/models.py
class HeroBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    link_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

class SiteStatistics(models.Model):
    total_consultations = models.PositiveIntegerField()
    total_winning_amount = models.BigIntegerField()  # 누적 낙찰액
    total_customers = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
```

#### URL
- 메인페이지: `/`

---

## Phase 3: 서비스 및 물건 관리 (3~4주차)

### 3.1 company 앱 (회사소개)

#### 페이지 구성
| URL | 페이지명 | 설명 |
|-----|---------|------|
| `/company/` | 인사말 | 대표 인사말, 경영철학, 비전 |
| `/company/history/` | 회사 연혁 | 타임라인 형태 |
| `/company/experts/` | 전문가 소개 | 컨설턴트 프로필 카드 |
| `/company/achievements/` | 사업 실적 | 수치 + 인포그래픽 |
| `/company/location/` | 오시는 길 | 카카오맵 연동 |

#### Models
```python
# apps/company/models.py
class CompanyInfo(models.Model):
    ceo_greeting = models.TextField()        # 대표 인사말
    vision = models.TextField()
    mission = models.TextField()

class History(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

class Expert(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='experts/')
    specialty = models.CharField(max_length=200)  # 전문분야
    certifications = models.TextField()           # 자격증
    career = models.TextField()                   # 경력사항
    order = models.PositiveIntegerField(default=0)
```

### 3.2 services 앱 (서비스 안내)

#### 페이지 구성 - 5대 서비스
| URL | 서비스명 | 대상 고객 |
|-----|---------|----------|
| `/services/home-buying/` | 내집마련 컨설팅 | 신혼부부, 무주택자 |
| `/services/redevelopment/` | 재개발/재건축 투자 | 중장기 투자자 |
| `/services/rental-income/` | 임대수익형 투자 | 임대사업자, 은퇴자 |
| `/services/company-building/` | 사옥마련 컨설팅 | 중소기업, 스타트업 |
| `/services/senior-facility/` | 노유자시설 컨설팅 | 사회복지법인, 의료법인 |
| `/services/process/` | 컨설팅 프로세스 | 8단계 안내 |
| `/services/pricing/` | 서비스 요금안내 | 패키지별 요금표 |

#### Models
```python
# apps/services/models.py
class ServiceCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)       # 아이콘 클래스
    short_description = models.CharField(max_length=200)

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory)
    title = models.CharField(max_length=100)
    hero_image = models.ImageField()
    overview = models.TextField()                # 서비스 개요
    target_properties = models.TextField()       # 대상 부동산
    process_steps = models.JSONField()           # 8단계 프로세스
    checkpoints = models.TextField()             # 핵심 체크포인트

class PricingPlan(models.Model):
    name = models.CharField(max_length=50)       # Basic/Standard/Premium/Enterprise
    description = models.TextField()
    price_type = models.CharField()              # 정액/정률
    price = models.CharField(max_length=100)
    features = models.JSONField()                # 서비스 내용 리스트
```

### 3.3 properties 앱 (추천 물건)

#### 페이지 구성
| URL | 페이지명 | 기능 |
|-----|---------|------|
| `/properties/` | 물건 리스트 | 필터링, 페이지네이션 |
| `/properties/weekly/` | 금주의 추천물건 | 주간 추천 |
| `/properties/category/<slug>/` | 분야별 물건 | 카테고리 필터 |
| `/properties/region/<region>/` | 지역별 물건 | 지역 필터 |
| `/properties/<pk>/` | 물건 상세 | 권리분석, 시세, 지도 |

#### Models
```python
# apps/properties/models.py
class PropertyCategory(models.Model):
    name = models.CharField(max_length=50)  # 내집마련/투자/사업용
    slug = models.SlugField(unique=True)

class Property(models.Model):
    # 기본 정보
    case_number = models.CharField(max_length=50)    # 사건번호
    title = models.CharField(max_length=200)
    category = models.ForeignKey(PropertyCategory)
    property_type = models.CharField()               # 아파트/빌라/상가 등

    # 위치 정보
    address = models.CharField(max_length=300)
    sido = models.CharField(max_length=20)           # 시도
    sigungu = models.CharField(max_length=20)        # 시군구
    latitude = models.DecimalField()
    longitude = models.DecimalField()

    # 면적/층수
    area_land = models.DecimalField()                # 대지면적
    area_building = models.DecimalField()            # 건물면적
    floor = models.CharField(max_length=20)

    # 가격 정보
    appraisal_price = models.BigIntegerField()       # 감정가
    minimum_price = models.BigIntegerField()         # 최저가
    market_price = models.BigIntegerField(null=True) # 시세

    # 경매 정보
    auction_date = models.DateField()                # 입찰일
    auction_status = models.CharField()              # 입찰예정/진행중/완료
    bid_count = models.PositiveIntegerField(default=0)

    # 권리분석
    rights_analysis = models.TextField()             # 권리분석 요약
    risk_level = models.CharField()                  # 리스크 등급 A/B/C
    tenant_info = models.TextField(blank=True)       # 임차인 현황

    # 추천 정보
    is_recommended = models.BooleanField(default=False)
    recommendation_reason = models.TextField(blank=True)
    tags = models.CharField(max_length=200)          # 역세권, 학군우수 등

    # 이미지
    thumbnail = models.ImageField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

class PropertyBookmark(models.Model):
    user = models.ForeignKey(CustomUser)
    property = models.ForeignKey(Property)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'property']
```

#### 필터링 옵션
```python
# 필터 항목
FILTER_OPTIONS = {
    'region': ['서울', '경기', '인천', '충청', '영남', '호남', '강원', '제주'],
    'property_type': ['아파트', '빌라', '단독주택', '상가', '오피스', '공장', '토지'],
    'purpose': ['내집마련', '투자', '사업용'],
    'price_range': ['1억이하', '1~3억', '3~5억', '5~10억', '10억이상'],
    'auction_status': ['입찰예정', '진행중', '완료'],
}
```

---

## Phase 4: 성공사례 및 아카데미 (5~6주차)

### 4.1 success_cases 앱 (성공사례)

#### 페이지 구성
| URL | 페이지명 | 설명 |
|-----|---------|------|
| `/success/` | 낙찰 성공기 | 카테고리별 필터 |
| `/success/<pk>/` | 성공기 상세 | 스토리텔링 형태 |
| `/success/reviews/` | 고객 후기 | 영상/텍스트 후기 |
| `/success/before-after/` | Before & After | 수익률 공개 |

#### Models
```python
# apps/success_cases/models.py
class SuccessCase(models.Model):
    category = models.ForeignKey(ServiceCategory)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField()

    # 물건 정보
    property_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    winning_price = models.BigIntegerField()         # 낙찰가
    market_price = models.BigIntegerField()          # 시세
    profit_rate = models.DecimalField()              # 수익률

    # 스토리
    client_situation = models.TextField()            # 고객 상황
    selection_reason = models.TextField()            # 물건 선정 이유
    analysis_process = models.TextField()            # 권리분석 과정
    bidding_strategy = models.TextField()            # 입찰 전략
    result_summary = models.TextField()              # 결과 및 수익

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerReview(models.Model):
    author_name = models.CharField(max_length=20)    # 이니셜
    service_category = models.ForeignKey(ServiceCategory)
    rating = models.PositiveIntegerField()           # 1~5점
    content = models.TextField()
    video_url = models.URLField(blank=True)          # 영상 후기 (유튜브)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 4.2 academy 앱 (경매 아카데미)

#### 페이지 구성
| URL | 페이지명 | 기능 |
|-----|---------|------|
| `/academy/` | 교육과정 안내 | 입문/실전/전문가 |
| `/academy/courses/` | 전체 과정 | 과정 리스트 |
| `/academy/courses/<pk>/` | 과정 상세 | 커리큘럼, 일정 |
| `/academy/enroll/<pk>/` | 수강신청 | 신청폼 + 결제 |
| `/academy/instructors/` | 강사진 소개 | 강사 프로필 |
| `/academy/reviews/` | 수강생 후기 | 만족도 리뷰 |
| `/academy/free/` | 무료 강좌 | 입문자용 영상 |

#### Models
```python
# apps/academy/models.py
class CourseCategory(models.Model):
    name = models.CharField(max_length=50)           # 입문/실전/전문가/1:1
    slug = models.SlugField(unique=True)

class Course(models.Model):
    category = models.ForeignKey(CourseCategory)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    thumbnail = models.ImageField()

    # 과정 정보
    duration = models.CharField(max_length=50)       # 8주, 12주 등
    schedule = models.CharField(max_length=100)      # 매주 토요일 10시
    start_date = models.DateField()
    max_students = models.PositiveIntegerField()
    current_students = models.PositiveIntegerField(default=0)

    # 가격
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(null=True)

    # 상세 내용
    description = models.TextField()
    curriculum = models.JSONField()                  # 주차별 커리큘럼
    target_audience = models.TextField()             # 대상 수강생
    benefits = models.TextField()                    # 수강 혜택

    is_active = models.BooleanField(default=True)
    is_enrolling = models.BooleanField(default=True)

class Instructor(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField()
    title = models.CharField(max_length=100)         # 직함
    bio = models.TextField()
    specialties = models.CharField(max_length=200)
    teaching_history = models.TextField()            # 강의 이력

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser)
    course = models.ForeignKey(Course)

    # 신청 정보
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # 결제 정보
    payment_method = models.CharField()              # card/bank/installment
    payment_status = models.CharField()              # pending/completed/cancelled
    payment_amount = models.PositiveIntegerField()
    paid_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class FreeLecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField()                    # 유튜브 임베드
    thumbnail = models.ImageField()
    duration = models.CharField(max_length=20)       # 영상 길이
    order = models.PositiveIntegerField(default=0)
```

---

## Phase 5: 정보센터 및 상담 (7~8주차)

### 5.1 info_center 앱 (정보센터)

#### 페이지 구성
| URL | 페이지명 | 콘텐츠 유형 |
|-----|---------|-----------|
| `/info/basics/` | 경매 기초지식 | 용어사전, 절차 안내 |
| `/info/rights-guide/` | 권리분석 가이드 | 등기부 읽기 등 |
| `/info/market-report/` | 시장동향 리포트 | 월간 분석 |
| `/info/columns/` | 전문가 칼럼 | 투자 인사이트 |
| `/info/news/` | 뉴스/공지사항 | 회사 소식 |
| `/info/<category>/<pk>/` | 콘텐츠 상세 | 본문 + SNS 공유 |

#### Models
```python
# apps/info_center/models.py
class PostCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200)

class Post(models.Model):
    category = models.ForeignKey(PostCategory)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    thumbnail = models.ImageField(blank=True)

    content = models.TextField()                     # CKEditor
    summary = models.CharField(max_length=300)       # 요약 (SEO용)

    author = models.ForeignKey(CustomUser, null=True)
    author_name = models.CharField(max_length=50)    # 외부 기고 시

    tags = models.CharField(max_length=200, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

class GlossaryTerm(models.Model):
    """경매 용어사전"""
    term = models.CharField(max_length=100)
    definition = models.TextField()
    category = models.CharField(max_length=50)       # 권리/절차/세금 등
    related_terms = models.ManyToManyField('self', blank=True)
```

### 5.2 consultation 앱 (상담신청)

#### 페이지 구성
| URL | 페이지명 | 기능 |
|-----|---------|------|
| `/consultation/` | 무료 상담신청 | 신청 폼 |
| `/consultation/complete/` | 신청 완료 | 확인 안내 |
| `/consultation/kakao/` | 카카오톡 상담 | 카카오채널 연동 |
| `/consultation/faq/` | 자주 묻는 질문 | FAQ 아코디언 |

#### Models
```python
# apps/consultation/models.py
class Consultation(models.Model):
    # 신청자 정보
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    # 상담 내용
    service_type = models.CharField()                # 5개 서비스 중 선택
    budget_range = models.CharField(blank=True)      # 예산 범위
    preferred_region = models.CharField(blank=True)  # 희망 지역
    message = models.TextField(blank=True)           # 문의 내용

    # 동의
    privacy_agreed = models.BooleanField(default=True)
    marketing_agreed = models.BooleanField(default=False)

    # 처리 상태
    status = models.CharField(default='pending')     # pending/in_progress/completed/cancelled
    assigned_to = models.ForeignKey(CustomUser, null=True)  # 담당 컨설턴트
    admin_memo = models.TextField(blank=True)        # 관리자 메모

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FAQ(models.Model):
    category = models.CharField(max_length=50)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

#### 상담신청 폼 필드
```python
CONSULTATION_FORM_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'phone': {'type': 'tel', 'required': True},
    'email': {'type': 'email', 'required': False},
    'service_type': {
        'type': 'select',
        'required': True,
        'choices': [
            ('home_buying', '내집마련 컨설팅'),
            ('redevelopment', '재개발/재건축 투자'),
            ('rental_income', '임대수익형 투자'),
            ('company_building', '사옥마련 컨설팅'),
            ('senior_facility', '노유자시설 컨설팅'),
        ]
    },
    'budget_range': {
        'type': 'select',
        'required': False,
        'choices': ['1억 이하', '1~3억', '3~5억', '5~10억', '10억 이상']
    },
    'preferred_region': {'type': 'text', 'required': False},
    'message': {'type': 'textarea', 'required': False, 'max_length': 500},
    'privacy_agreed': {'type': 'checkbox', 'required': True},
    'marketing_agreed': {'type': 'checkbox', 'required': False},
}
```

---

## Phase 6: 프론트엔드 및 통합 (9주차)

### 6.1 템플릿 구조

```
templates/
├── base.html                    # 기본 레이아웃
├── includes/
│   ├── header.html              # GNB 네비게이션
│   ├── footer.html              # 푸터
│   ├── sidebar_cta.html         # 우측 고정 CTA
│   ├── kakao_chat.html          # 카카오 채팅 버튼
│   └── seo_meta.html            # SEO 메타태그
├── components/
│   ├── property_card.html       # 물건 카드
│   ├── success_card.html        # 성공사례 카드
│   ├── review_card.html         # 후기 카드
│   ├── pagination.html          # 페이지네이션
│   └── breadcrumb.html          # 브레드크럼
├── core/
│   └── index.html               # 메인페이지
├── accounts/
│   ├── login.html
│   ├── signup.html
│   └── mypage.html
├── company/
│   ├── greeting.html            # 인사말
│   ├── history.html             # 연혁
│   ├── experts.html             # 전문가
│   └── location.html            # 오시는 길
├── services/
│   ├── list.html                # 서비스 목록
│   ├── detail.html              # 서비스 상세
│   ├── process.html             # 프로세스
│   └── pricing.html             # 요금안내
├── properties/
│   ├── list.html                # 물건 리스트
│   └── detail.html              # 물건 상세
├── success_cases/
│   ├── list.html
│   ├── detail.html
│   └── reviews.html
├── academy/
│   ├── index.html               # 아카데미 메인
│   ├── course_list.html
│   ├── course_detail.html
│   ├── enroll.html              # 수강신청
│   └── instructors.html
├── info_center/
│   ├── list.html
│   └── detail.html
└── consultation/
    ├── form.html                # 상담신청
    ├── complete.html            # 완료
    └── faq.html                 # FAQ
```

### 6.2 디자인 시스템 (CSS Variables)

```css
/* static/css/variables.css */
:root {
    /* Primary Colors */
    --color-primary: #1F4E79;        /* 네이비 */
    --color-secondary: #2E75B6;      /* 블루 */
    --color-accent: #C9A227;         /* 골드 */

    /* Background */
    --color-bg: #F8F9FA;
    --color-white: #FFFFFF;

    /* Text */
    --color-text-dark: #212529;
    --color-text-gray: #6C757D;

    /* System Colors */
    --color-success: #28A745;
    --color-warning: #FFC107;
    --color-danger: #DC3545;
    --color-info: #17A2B8;

    /* Typography */
    --font-family: 'Pretendard', -apple-system, sans-serif;
    --font-size-h1: 42px;
    --font-size-h2: 32px;
    --font-size-h3: 24px;
    --font-size-body: 16px;
    --font-size-caption: 14px;

    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;

    /* Border Radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 16px;

    /* Shadows */
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
}
```

### 6.3 반응형 브레이크포인트

```css
/* Breakpoints */
@media (max-width: 575px) { /* Mobile Small */ }
@media (min-width: 576px) and (max-width: 767px) { /* Mobile */ }
@media (min-width: 768px) and (max-width: 991px) { /* Tablet */ }
@media (min-width: 992px) and (max-width: 1199px) { /* Laptop */ }
@media (min-width: 1200px) and (max-width: 1399px) { /* Desktop */ }
@media (min-width: 1400px) { /* Desktop Large */ }
```

---

## Phase 7: SEO, 보안 및 배포 (10주차)

### 7.1 SEO 설정

#### 메타 태그 템플릿
```html
<!-- templates/includes/seo_meta.html -->
<title>{% block title %}{% endblock %} | 부동산 경매 컨설팅</title>
<meta name="description" content="{% block meta_description %}{% endblock %}">
<meta name="keywords" content="{% block meta_keywords %}{% endblock %}">

<!-- Open Graph -->
<meta property="og:title" content="{% block og_title %}{% endblock %}">
<meta property="og:description" content="{% block og_description %}{% endblock %}">
<meta property="og:image" content="{% block og_image %}{% endblock %}">
<meta property="og:url" content="{{ request.build_absolute_uri }}">

<!-- Schema.org -->
<script type="application/ld+json">
{% block schema_json %}{% endblock %}
</script>
```

#### sitemap.xml 생성
```python
# config/sitemaps.py
from django.contrib.sitemaps import Sitemap

class PropertySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
```

### 7.2 보안 설정

```python
# config/settings/production.py

# HTTPS 강제
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 쿠키 보안
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# XSS 방지
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

### 7.3 외부 서비스 연동

```python
# 연동 서비스 목록
INTEGRATIONS = {
    'analytics': {
        'google_analytics_4': 'G-XXXXXXXXXX',
        'naver_analytics': 'XXXXXXXX',
    },
    'social_login': {
        'kakao': {'client_id': '', 'secret': ''},
        'naver': {'client_id': '', 'secret': ''},
    },
    'payment': {
        'provider': 'tosspayments',  # or 'inicis'
        'client_key': '',
        'secret_key': '',
    },
    'messaging': {
        'kakao_channel': '@auction-consulting',
        'alimtalk': {'sender_key': ''},
        'sms': {'api_key': '', 'sender': ''},
    },
    'maps': {
        'kakao_map': {'app_key': ''},
    },
    'email': {
        'provider': 'stibee',  # or 'mailchimp'
        'api_key': '',
    }
}
```

### 7.4 배포 체크리스트

```
[ ] DEBUG = False 설정
[ ] SECRET_KEY 환경변수 분리
[ ] ALLOWED_HOSTS 설정
[ ] Static 파일 수집 (collectstatic)
[ ] 데이터베이스 마이그레이션
[ ] SSL 인증서 설치
[ ] Nginx/Gunicorn 설정
[ ] 로그 설정
[ ] 백업 설정
[ ] 모니터링 설정 (Sentry)
```

---

## 관리자 페이지 (Django Admin) 커스터마이징

### 관리 기능 목록

```python
# 관리자 대시보드 구성
ADMIN_SECTIONS = {
    '콘텐츠 관리': ['배너', '물건', '성공사례', '게시물'],
    '고객 관리': ['상담신청', '회원', '수강신청'],
    '통계': ['방문자', '상담', '물건조회'],
    '설정': ['사이트정보', '메뉴', 'SEO'],
}
```

---

## 개발 일정 요약

| 주차 | Phase | 주요 작업 |
|-----|-------|----------|
| 1주 | Phase 1 | 프로젝트 설정, DB 설계 |
| 2주 | Phase 2 | accounts, core 앱 개발 |
| 3주 | Phase 3-1 | company, services 앱 개발 |
| 4주 | Phase 3-2 | properties 앱 개발 |
| 5주 | Phase 4-1 | success_cases 앱 개발 |
| 6주 | Phase 4-2 | academy 앱 개발 |
| 7주 | Phase 5 | info_center, consultation 앱 개발 |
| 8주 | Phase 6-1 | 프론트엔드 템플릿 개발 |
| 9주 | Phase 6-2 | 통합 및 외부 연동 |
| 10주 | Phase 7 | SEO, 보안, 테스트, 배포 |

---

## 다음 단계

이 문서를 기반으로 실제 개발을 진행합니다:

1. **Phase 1 시작**: Django 프로젝트 생성 및 초기 설정
2. **앱별 순차 개발**: 각 Phase에 따라 앱 개발
3. **코드 리뷰**: 각 Phase 완료 시 검토
4. **테스트**: 기능 테스트 및 버그 수정
5. **배포**: 운영 서버 배포

---

*문서 작성일: 2025년 11월*
*버전: 1.0*
