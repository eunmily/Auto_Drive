import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from std_msgs.msg import String


finding = 0
TB_LIN_SPD = 0.1
TB_ANG_SPD = 1


tw = Twist()

#=======================================================================================

def go():
    tw.angular.z = 0.0
    tw.linear.x = 0.05
    
def stop():
    tw.angular.z = 0.0
    tw.linear.x = 0.0

def turn_left():
    tw.angular.z = 0.4
    tw.linear.x = 0.0

def turn_right():
    tw.angular.z = -0.4
    tw.linear.x = 0.0



#========================================================================================

def GetGreen(frame):
    global finding
    crop_img =frame[60:170, 255:320]
    cv2.imshow('findgreen', crop_img)
    #bgr -> hsv
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    #색범위 지정
    lower_green = np.array([30,85,120])   
    upper_green = np.array([90,255,255])
    
    #hsv에서 녹색 검출(mask)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    cv2.imshow('mask(find green)', mask)
    green_extracted = cv2.bitwise_and(crop_img, crop_img, mask=mask)
    gray_light = cv2.cvtColor(green_extracted, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_light, (5,5) , 0)
    _, bin = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(crop_img, contour, -1, (255,0,255),1)
    #윤곽선 개수
    num_contours = len(contours)
    print(f"초록색 객체 개수: {num_contours}")

        #초록색 검출 결과
    if len(contours)>0:
        return 1
    else:
        return 0
#=======================================================================================

class Servo_Control(Node):

    def __init__(self):
        super().__init__('servo_control')
        self.pub_pt = self.create_publisher(String, 'pt_msg', 10)
        self.pt_msg = String()
        
    def up(self):
        msg = String()
        msg.data = 'up'
        self.pub_pt.publish(msg)
        
    def down(self):
        msg = String()
        msg.data = 'down'
        self.pub_pt.publish(msg)
        
#=======================================================================================

class Timer(Node):
    def __init__(self):
        super().__init__('Timer')
        timer_period = 1  # seconds
        self.timer    = self.create_timer(1.0, self.count_sec)
        self.cnt_sec = 0

    
    def count_sec(self):
        self.cnt_sec += 1
        duration = self.cnt_sec + 11
        if self.cnt_sec <= duration:
            go()
        else:
            pass
    
#=======================================================================================


class LineDetector(Node):

    def __init__(self):
        super().__init__('img_convert')
        qos_profile = QoSProfile(depth=10)

        self.subscription = self.create_subscription(CompressedImage, 
                'camera/image/compressed', 
                self.get_compressed, 
                10)
        self.bridge = CvBridge()
        self.cv_img = cv2.imread("empty1.png", cv2.IMREAD_COLOR)
        print("type(cv_img)", type(self.cv_img))

    def get_compressed(self, msg):
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

#=======================================================================================


def main(args=None):
    global finding
    rclpy.init(args=args)
    node = LineDetector()
    servo = Servo_Control()
    timer = Timer()
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    try:   
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=1.0)
            img = node.cv_img
            if img is not None and not img.size == 0:
                frame = img
                frame = cv2.flip(frame,-1)#상하반전
                frame = cv2.flip(frame, 1)#좌우반전
                cv2.imshow( 'normal' , frame)
                
                crop_img =frame[0:110, 0:320] # 세로 0~110픽셀 가로 0~320픽셀만 자름
                cv2.imshow('crop_img', crop_img)
                copy_img = crop_img.copy()
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) #bgr->gray
                blur = cv2.GaussianBlur(gray, (5,5) , 0)  #가우시안 블러 (노이즈 줄임)
                ret,thresh1 = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY_INV) #명암 90 이하 255, 이상 0으로 이진화
                mask = cv2.erode(thresh1, None, iterations=2)  
                mask = cv2.dilate(mask, None, iterations=2)
                
                mask_1 = mask.copy()
                contours,hierarchy = cv2.findContours(mask_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                #contour들의 면적 기준으로 오름차순
                contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
                   #윤곽선 개수 확인
                num_contours = len(contours)
                print(f"검출된 윤곽선 객체 개수: {num_contours}")
                if finding == 0:
                    if len(contours) > 0:
                        
                        c0 = contours[0]
                        M0 = cv2.moments(c0)
                        cx0 = int(M0['m10']/M0['m00'])
                        cy0 = int(M0['m01']/M0['m00'])
                        
                        c1 = 0
                        M1 = 0
                        cx1 = 0
                        cy1 = 0
#------------------------------------------------------------------------------------
     #contour가 2개면
                        if len(contours) == 2:
                            c1 = contours[1]
                            M1 = cv2.moments(c1)
                            cx1 = int(M1['m10']/M1['m00'])
                            cy1 = int(M1['m01']/M1['m00'])
                            #cy1 = cy0
                        # 무게중심 위치 표시
                        
                     #contour[0] 파란색 크로스
                            cv2.line(copy_img,(cx0,0),(cx0,240),(0,0,200),1)
                            cv2.line(copy_img,(0,cy0),(320,cy0),(0,0,200),1)
                     #contour[1] 노란색 크로스
                            cv2.line(copy_img,(cx1,0),(cx1,240),(0,255,255),1)
                            cv2.line(copy_img,(0,cy1),(320,cy1),(0,255,255),1)
                     #contour 표시 [0] 초록색, [1] 파란색
                            cv2.drawContours(copy_img, contours[0], -1, (0,255,0),1)
                            cv2.drawContours(copy_img, contours[1], -1, (255,255,0),1)
                       
                            #cv2.imshow('copy_img(2)', copy_img)
                            
                            #[0]의 무게중심 원으로 표시
                            cv2.circle(mask_1, (cx0, cy0), 3, (0,0,0), -1)
                            #[1]의 무게중심 사각형으로 표시
                            cv2.rectangle(mask_1, (cx1-3, cy1-3), (cx1+3, cy1+3), (0,0,0), -1)

                            #무게중심의 평균값 계산
                            cx_m = round((cx0 + cx1) / 2)
                            cy_m = round((cy0 + cy1) / 2)

                            #무게중심의 평균값(기준값) 위치에 회색 사각형 표시    
                            cv2.rectangle(mask_1, (cx_m -3, cy0 - 3), (cx_m + 3, cy0 + 3), (123,123,123), -1)
                            cv2.imshow('contour_2(2)', mask_1)
                            cv2.moveWindow('contour_2', 660, 0)

                            print("cx0 : ", cx0) 
                            print("cx1 : ", cx1) 
                            print("cx_m : ", cx_m)
                            print("cy_m : ", cy_m)
                            print("cy0 : ", cy0) 
                            print("cy1 : ", cy1) 
                            print("cx 차이 : ", cx1 -cx0)
                            print("cy 차이 : ", cy1 -cy0)
                            #기준값이 왼쪽일때
                            if 0<cx_m and cx_m <140:              
                                print("Turn Left!")
                                turn_left()
                            #기준값이 오른쪽일때        
                            elif 180<cx_m and cx_m<320:
                                print("Turn Right")
                                turn_right()
                            #기준값이 중앙일때
                            else:
                                print("go")
                                go()
                                
                            pub.publish(tw)
#------------------------------------------------------------------------------------
    #contour가 2개가 아니면                    
                        else:
    #contour 2개이상
                            if len(contours)>2:   
                                    #모든 contour 분홍색으로 표시
                                for contour in contours:
                                    cv2.drawContours(copy_img, contour, -1, (255,0,255),3)
                                cv2.imshow('copy_img(2<)', copy_img)
                                stop()
                                pub.publish(tw)
                                print("=========")
                                print("장애물 감지")
                                print("=========")
    #contour 1개   
                            elif len(contours) == 1:    #일시정지선 발견
                                cv2.drawContours(copy_img, contours, -1, (255,0,255), 1)
                                stop()
                                finding = 1
                                pub.publish(tw)
                                print("일시정지선 발견")   
                                     #서보모터 위로 올리고 
                                servo.up()
                                print("고개 든다") 
                                   
      
                            else:
                                pass
                    #print("finding == ", finding)                
                elif finding == 1:
                    isGreen = GetGreen(frame)
                                
                    if isGreen == 1:
                        print("===================")
                        print("녹색등화 주행하세요")
                        print("===================")
                        duration = timer.cnt_sec + 11
                       
                        #3초 카운트
                        while timer.cnt_sec < duration: 
                            rclpy.spin_once(timer, timeout_sec = 1.0)
                            print("wait .................  : ", duration - timer.cnt_sec + 1)
                            pub.publish(tw)
                        
                        servo.down()  
                        finding = 0
                        
                    else:
                        print("===================")
                        print("적색등화 정지하세요")
                        print("===================")
                        stop()
                        pub.publish(tw)
#-------------------------------------------------------------------------------------
                if cv2.waitKey(1) == ord('q'):
                    stop()
                    pub.publish(tw)
                    break
    
        cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        stop()
        pub.publish(tw)
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()
