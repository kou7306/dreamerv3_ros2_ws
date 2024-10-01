import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped

class RobotPublisher(Node):
    def __init__(self):
        super().__init__('robot_publisher')
        self.publisher_ = self.create_publisher(TransformStamped, 'object_pose_topic', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = TransformStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_footprint'
        msg.child_frame_id = 'base_link'
        msg.transform.translation.x = 1.0  # 適切な座標を設定
        msg.transform.translation.y = 0.0
        msg.transform.translation.z = 0.0
        msg.transform.rotation.x = 0.0
        msg.transform.rotation.y = 0.0
        msg.transform.rotation.z = 0.0
        msg.transform.rotation.w = 1.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)

def main(args=None):
    rclpy.init(args=args)
    robot_publisher = RobotPublisher()
    rclpy.spin(robot_publisher)
    robot_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
