# -*- coding: utf-8 -*-
from datetime import timedelta


def get_ipaddress(request):
    """Return IP Address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_mobile(request):
    """Return true if request from Android or iPhone"""
    user_agent = request.META['HTTP_USER_AGENT']
    if 'Android' in user_agent or 'iPhone' in user_agent:
        return True
    else:
        return False


def date_range(start_date, end_date):
    """Iterate with date"""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def month_range(startmonth, startyear, endmonth, endyear):
    """Iterate with month"""
    range_start = startyear * 12 + startmonth - 1
    range_end = endyear * 12 + endmonth - 1
    for i in range(range_start, range_end):
        y, m = divmod(i, 12)
        yield y, m + 1


def get_key_1(item):
    """Utility funtion to sort list with first item"""
    return item[1]


def get_key_2(item):
    """Utility funtion to sort list with second item"""
    return item[2]


def get_media_from_email(request, email):
    """Find media name from email"""
    if '@chosun.com' in email:
        return '조선일보'
    elif '@joongang.co.kr' in email:
        return '중앙일보'
    elif '@donga.com' in email:
        return '동아일보'
    elif '@hani.co.kr' in email:
        return '한겨레'
    elif '@kyunghyang.com' in email:
        return '경향신문'
    elif '@ohmynews.com' in email:
        return '오마이뉴스'
    elif '@mediatoday.co.kr' in email:
        return '미디어오늘'
    elif '@kbs.co.kr' in email:
        return 'KBS'
    elif '@mbc.co.kr' in email:
        return 'MBC'
    elif '@sbs.co.kr' in email:
        return 'SBS'
    elif '@jtbc.co.kr' in email:
        return 'JTBC'
    elif '@mbn.co.kr' in email:
        return 'MBN'
    elif '@ytn.co.kr' in email:
        return 'YTN'
    elif '@yna.co.kr' in email:
        return "연합뉴스"
    elif '@newsis.com' in email:
        return '뉴시스'
    elif '@news1.kr' in email:
        return '뉴스1'
    elif '@kmib.co.kr' in email:
        return '국민일보'
    elif '@cbs.co.kr' in email:
        return 'CBS노컷뉴스'
    elif '@dailian.co.kr' in email:
        return '데일리안'
    elif '@mk.co.kr' in email:
        return '매일경제'
    elif '@mt.co.kr' in email:
        return '머니투데이'
    elif '@munhwa.com' in email:
        return '문화일보'
    elif '@mhj21.com' in email:
        return '문화저널21'
    elif '@vop.co.kr' in email:
        return '민중의소리'
    elif '@seoul.co.kr' in email:
        return '서울신문'
    elif '@sedaily.com' in email:
        return '서울경제'
    elif '@segye.com' in email:
        return '세계일보'
    elif '@sisain.co.kr' in email:
        return '시사iN'
    elif '@sisajournal.com' in email:
        return '시사저널'
    elif '@asiae.co.kr' in email:
        return '아시아경제'
    elif '@asiatoday.co.kr' in email:
        return '아시아투데이'
    elif '@inews24.com' in email:
        return '아이뉴스'
    elif '@womennews.co.kr' in email:
        return '여성신문'
    elif '@edaily.co.kr' in email:
        return '이데일리'
    elif '@etnews.com' in email:
        return '전자신문'
    elif '@joseilbo.com' in email:
        return '조세일보'
    elif '@fnnews.com' in email:
        return '파이낸셜뉴스'
    elif '@pressian.com' in email:
        return '프레시안'
    elif '@hankyung.com' in email:
        return '한국경제'
    elif '@hankookilbo.com' in email:
        return '한국일보'
    elif '@heraldcorp.com' in email:
        return '헤럴드경제'
    elif '@journalist.or.kr' in email:
        return '기자협회보'
    else:
        return "기타"
