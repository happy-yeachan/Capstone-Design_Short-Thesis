from konlpy.tag import Okt
from collections import Counter

# Okt 형태소 분석기 로드
okt = Okt()

def extract_keywords(text, num_keywords=6, exclude_keywords=None):
    if exclude_keywords is None:
        exclude_keywords = ["논문", "오늘"]

    # 명사 추출
    nouns = okt.nouns(text)
    
    # 중복 제거 및 필터링
    filtered_nouns = [noun for noun in nouns if len(noun) > 1 and noun not in exclude_keywords]

    # 빈도 수 계산
    noun_counts = Counter(filtered_nouns)

    # 상위 N개 키워드 추출
    top_keywords = noun_counts.most_common(num_keywords)

    return [word for word, count in top_keywords]

# # 대본 예시
# script = "오늘은 컴퓨터 기술이 어떻게 발전해왔고, 앞으로 어떻게 발전할지 예측하는 방법을 알려주는 논문을 소개할게요! 지금까지 많은 연구들이 유행이나 핫이슈에 맞춰 주제를 정해왔대요. 그런데 이렇게 하면 깊이 있는 결과를 얻기 어렵다고 해요. 그래서 이 논문에서는 컴퓨터 기술을 연구할 때 기술의 큰 흐름을 따라가야 한다고 말하고 있어요. 그중에서도 프로그래밍 언어가 어떻게 발전해왔는지를 살펴보고, 그 흐름을 따라 미래를 예측하는 방법을 제안하고 있어요. 쉽게 말해, 과거의 기술 변화를 잘 이해하면, 미래의 기술이 어떻게 발전할지 미리 준비할 수 있다는 거예요! 컴퓨터와 프로그래밍에 관심 있는 친구들, 꼭 한 번 읽어보면 좋을 것 같아요!"

# # 키워드 추출 (논문 제거)
# keywords = extract_keywords(script, num_keywords=6, exclude_keywords=['논문'])
# print("추출된 키워드:", keywords)
