import rclpy
from rclpy.node import Node
from math import degrees

from turtlesim.msg import Pose

class SubPose(Node): 

    def __init__(self):
        super().__init__('sub_turtle_pose')
        sub = self.create_subscription(Pose, '/turtle1/pose', self.get_pose,10)
    def get_pose(self, msg):
        pose_th = msg.theta
        print(round(degrees(pose_th)))
        
def main(args=None):
    rclpy.init(args=args)
    node= SubPose()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
