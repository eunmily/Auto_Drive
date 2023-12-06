import rclpy, sys, serial
from rclpy.node import Node
from rclpy.qos import QoSProfile

from std_msgs.msg import String



sp  = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
class SubPT_MSG(Node):

    def __init__(self):
        super().__init__('sub_pt_msg')
        qos_profile = QoSProfile(depth=10)
        #'/pt_msg라는 토픽 구독'
        self.subscription = self.create_subscription(
            String, '/pt_msg', self.get_pt_msg, qos_profile )
        self.pt_msg = String()
        

                    
    def get_pt_msg(self, msg):
        self.pt_msg = msg.data
        
        if self.pt_msg == "down":
            sp.write(b'1')
            print(self.pt_msg)
        elif self.pt_msg == "up":
            sp.write(b'2')
            print(self.pt_msg)
        else:
            pass
        
        print(self.pt_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SubPT_MSG()
    try:    
        #while rclpy.ok():
            #pass
        #sys.exit(1)
        rclpy.spin(node)
    except KeyboardInterrupt:
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
