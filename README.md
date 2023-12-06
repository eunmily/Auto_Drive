# Project

 프로젝트명 : Auto Driving
수행기간
 2023. 10. 23 ~ 2023. 11. 24 (33일)

담당역할
- Project Manger
- 소프트웨어 구현
- ppt 제작
수행목표
- 광학카메라로 차선 검출
- 검출된 차선의 평균(무게 중심값)으로 주행
- 검출된 카메라 객체의 물체감지 후 정지
사용 기술
- Open CV로 라인 검출, 신호등 인식
- 마이크로 컨트롤러 활용 카메라 제어
- Python으로 코드 작성
- ROS2 환경에서 Turtlebot3 구동
세부수행내용
구 성 도


상세 내용
1) 목 적 : turtlebot3를 활용한 자율주행 차량 구현
2) 개발환경 : 리눅스(우분투), python(OpenCV), C언어, arduino, turtlebot3(ROS2)
3) 주요기능 
   3 - 1 레인트래킹을 이용한 주행 
	OpenCV를 이용해 차선 검출, 차선 무게중심 계산, 무게중심 x값의 평균을 기준으로 조향 가능

   3 - 2 상황 변화에 따른 주행 
	횡단보도, 신호등화, 장애물 등에 따른 정지 및 주행 
 
   3 - 3 카메라 틸트 제어
	마이크로 컨트롤러를 활용해 일시정지선을 인식하면 신호등화 검지를 위해 카메라 UP
	일시정지선 통과후 차선검출 및 정상 주행을 위해 카메라 DOWN

# 구성도
<img src="https://github.com/Cshe97/Auto_driving/blob/main/%EC%9E%90%EC%9C%A8%EC%A3%BC%ED%96%89%20%EA%B5%AC%EC%84%B1%EB%8F%84.jpg?raw=true"  width="450" height="450">

# 결과화면
<img src="https://github.com/Cshe97/Auto_driving/blob/main/lane_trace.png?raw=true"  width="200" height="200">        <img src="https://github.com/Cshe97/Auto_driving/blob/main/detect_object.png?raw=true"  width="200" height="200">        <img src="https://github.com/Cshe97/Auto_driving/blob/main/detect_light.png?raw=true"  width="200" height="200">
