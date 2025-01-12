# Team Shorts_makers

## 팀 구성
- **오예찬 (back-end)** 
- **이영재 (back-end)** 

## 프로젝트 배경
#### 개요
한국은 SCI 논문 발표 수에서 세계 12위에 위치하고 있으나, 대중은 논문을 읽고 이해하는 데 어려움을 느끼고 있다. 이러한 문제를 해결하기 위해, 대중이 가장 쉽게 접할 수 있는 매체인 **숏폼 영상**을 활용하여 논문을 더 쉽고 빠르게 전달할 방법을 모색했다. 본 프로젝트는 논문의 초록을 숏폼 영상으로 변환하여, 학문적 정보의 접근성을 높이고 대중의 관심을 유도하려는 목적을 가지고 있다.

## 프로젝트 내용
### 프로그램 흐름
![image](https://github.com/user-attachments/assets/a40acf8f-ed4b-48df-a39c-f2c74ff94f36)


### 설계 흐름
![image](https://github.com/user-attachments/assets/5edfd56f-cfb3-4326-9699-8fe38e227577)

### 구현 내용
1. **KCI API 활용 논문 데이터 추출 및 저장**  
   - 한국 학술지 논문 데이터를 자동으로 추출하여 데이터베이스에 저장.
   
2. **OpenAI API와 초록 데이터를 통한 대본 생성**  
   - 논문 초록을 바탕으로 OpenAI API를 활용하여 숏폼 영상의 대본을 자동 생성.
   
3. **NAVER Cloud Platform TTS 활용 대본 보이스 생성**  
   - 생성된 대본을 NAVER Cloud Platform의 TTS(Text-to-Speech) 기능을 통해 음성으로 변환.
   
4. **형태소 분석을 통한 키워드 추출**  
   - 논문 초록에서 의미 있는 키워드를 추출하여, 영상 제작에 필요한 핵심 정보 도출.
   
5. **Pixabay API 활용 키워드에 맞는 영상 데이터 추출**  
   - 추출된 키워드를 기반으로 Pixabay API를 활용하여 관련 영상을 자동으로 검색.
   
6. **MoviePy 활용 영상 편집 및 자막 생성**  
   - 추출된 영상과 생성된 대본을 MoviePy 라이브러리로 편집하고, 자막을 추가.
   
7. **대본 보이스와 영상 병합**  
   - 최종적으로 생성된 음성과 영상을 병합하여 숏폼 영상을 완성.

### 기대 효과
본 프로젝트는 논문의 접근성을 높여 일반 대중이 논문을 보다 쉽게 이해하고 접할 수 있는 기회를 제공한다. 또한, 숏폼 콘텐츠의 대중화와 활용도를 반영하여, 사회 이슈나 도서 소개 등의 분야로도 확장할 수 있는 가능성을 지닌다. 자동화된 시스템을 통해 콘텐츠 제작 시간을 단축시키고, 대규모로 정보 전달을 가능하게 하여 현대적인 정보 소통 방식을 혁신할 수 있다.

## 결과물
[유튜브 링크](https://www.youtube.com/@짧은논문/shorts)

## 개발 환경
- **DBMS**: MySQL
- **개발 언어**: Python, Java
- **IDE**: Visual Studio Code, IntelliJ


## Server 아키텍처
[Spring Server](https://github.com/YeongJae0114/Short-thesis/blob/main/README.md)

