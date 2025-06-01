import rclpy
from rclpy.node import Node

from std_srvs.srv import Trigger
from std_msgs.msg import Float64


class AlignmentMath(Node):

    def __init__(self):
        super().__init__('alignment_math')
        self.srv = self.create_service(Trigger, 'get_calibration_data', self.get_calibration_data_callback)
        self.boardSub = self.create_subscription(Float64, 'board_calibration_data', self.read_board_calibration_callback, 10)
        self.holderSub = self.create_subscription(Float64, 'holder_calibration_data', self.read_holder_calibration_callback, 10)
        self.boardOffsetSub = self.create_subscription(Float64, 'board_offset_changes', self.read_board_offset_callback, 10)
        self.holderOffsetSub = self.create_subscription(Float64, 'holder_offset_changes', self.read_holder_offset_callback, 10)

        self.boardCalibration = -1
        self.holderCalibration = -1
        self.board_offset = 0
        self.holder_offset = 0

    def get_calibration_data_callback(self, request, response):
        self.get_logger().info('Incoming calibration request')
        response.success = True
        response.message = f"{self.boardCalibration} {self.board_offset} {self.holderCalibration} {self.holder_offset}"
        return response

    def read_board_calibration_callback(self, message):
        self.get_logger().info(f"BOARD DATA: {message}.data")
        self.boardCalibration = message.data
        self.board_offset = 0
        return message

    def read_holder_calibration_callback(self, message):
        self.get_logger().info(f"HOLDER DATA: {message.data}")
        self.holderCalibration = message.data
        self.holder_offset = 0
        return message

    def read_board_offset_callback(self, message):
        self.get_logger().info(f"BOARD OFFSET DELTA RECEIVED: {message}")
        self.board_offset += message.data
        self.get_logger().info(f"NEW BOARD OFFSET: {self.board_offset}")
        return message

    def read_holder_offset_callback(self, message):
        self.get_logger().info(f"HOLDER OFFSET DELTA RECEIVED: {message}")
        self.holder_offset += message.data
        self.get_logger().info(f"NEW HOLDER OFFSET: {self.holder_offset}")
        return message

def main():
    rclpy.init()

    alignment_math = AlignmentMath()

    rclpy.spin(alignment_math)

    rclpy.shutdown()


if __name__ == '__main__':
    main()