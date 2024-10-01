import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__("image_subscriber")
        #self.declare_parameter('image_topic_name', '/camera/color/image_raw')
        self.declare_parameter('image_topic_name', '/image/compressed')
        image_topic_name = self.get_parameter('image_topic_name').get_parameter_value().string_value

        video_qos = rclpy.qos.QoSProfile(depth=10)
        video_qos.reliability = rclpy.qos.QoSReliabilityPolicy.BEST_EFFORT

        self.sub_img = self.create_subscription(
            CompressedImage,
            image_topic_name,
            self.on_image_subscribed,
            video_qos
        )
        self.cnt = 0
        print("init image subscriber")
    
    def on_image_subscribed(self, img):
        print("subscribed" + str(self.cnt))
        self.cnt += 1
        np_arr = np.fromstring(img.data.tobytes(), np.uint8)
        input_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        output_image = self.process_image(input_image)
        cv2.imshow("Image", output_image)
        cv2.waitKey(1)
        
    def process_image(self, frame):
        frame = cv2.resize(frame, (640, 480))
        return frame


def main(args=None):
    try:
        rclpy.init(args=args)
        rclpy.spin(ImageSubscriber())
    
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
        

if __name__ == "__main__":
    main()
