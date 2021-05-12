# 1n6

## 개발환경
- Django
- mysql

## 사용 IDE
> pycharm에 js코드에 색이나 도움 안 주길래,,, html css js는 VS Code로 작업합니다,, pycharm에도 되는데 저만 모르는 거라면 알려주세요...
- pycharm
- VS Code

4/28 이미지 이름 변경해서 올리게 했으면서 commit 안 함.ㅋ

요상한 점
- static file을 snsP 아래에 넣어두면 찾질 못함. 다른 곳에 두면 찾음.

현위치 불러오기
- google geocoring api
- [역지오코딩](https://developers.google.com/maps/documentation/geocoding/overview#ReverseGeocoding)


~~행정구역 DB에 넣기~~
- ~~세종시 데이터 insert 잘 확인하기~~
- ~~test1.py ~~
- ~~addData1.xls~~
- ~~[코드 참고](https://woonizzooni.tistory.com/entry/Python-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD-%ED%96%89%EC%A0%95%EB%8F%99-%EB%8D%B0%EC%9D%B4%ED%84%B0-MySQL-DB-%ED%85%8C%EC%9D%B4%EB%B8%94-%EC%83%9D%EC%84%B1-%EC%98%88%EC%8B%9C)~~
- ~~[데이터 참고](http://kssc.kostat.go.kr/ksscNew_web/kssc/common/CommonBoardList.do?gubun=1&strCategoryNameCode=019&strBbsId=kascrr&categoryMenu=014)
- 현위치 불러오는 정확도가 좀 떨어진다,,.
 ==> 변경
 도로명주소 DB 사용
 - test1.py 
 - address_data/개선_도로명코드_전체분.txt
 - [데이터참고](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=match)
