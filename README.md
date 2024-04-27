# 크롤링 구조

![아키텍처](./images/image.png)

1. 공용의 Redis 존재
2. 검색어에 따라 레스토랑 목록을 크롤링 해서 Redis에 저장
3. Redis의 데이터를 각자의 VM에서 하나씩 가져와서 처리 후 공용 Storage 혹은 DB에 저장
