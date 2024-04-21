#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image, CameraInfo, Imu
from cv_bridge import CvBridge
from geometry_msgs.msg import Pose, Twist, PoseStamped
from tf.transformations import quaternion_from_euler
import tf
import numpy as np
import cv2
from geometry_msgs.msg import PoseStamped
from scipy.spatial.transform import Rotation as R
from filterpy.kalman import KalmanFilter
from differential_drive_robot_control.msg import VisualOdometryData


class VisualOdometryNode:
    class VisualOdometry:
        def __init__(self):
            # Initialize variables
            self.prev_frame = None
            self.prev_keypoints = None
            self.prev_descriptors = None
            self.curr_frame = None
            self.curr_keypoints = None
            self.curr_descriptors = None
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            self.matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)  # Enable cross-check
            self.R = np.eye(3)
            self.t = np.zeros((3, 1))

        def extract_features(self, frame):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            orb = cv2.ORB_create(nfeatures=500)
            keypoints, descriptors = orb.detectAndCompute(gray, None)
            return keypoints, descriptors

        def match_features(self):
            # Match features using the Brute-Force matcher
            matches = self.matcher.match(self.prev_descriptors, self.curr_descriptors)
            matches = sorted(matches, key=lambda x: x.distance)

            # Check if there are enough matches for essential matrix estimation
            if len(matches) < 5:
                rospy.logerr("Error in matching features: Insufficient matches for essential matrix estimation")
                return None, None

            prev_pts = np.float32([self.prev_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            curr_pts = np.float32([self.curr_keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            # Estimate essential matrix using RANSAC
            E, mask = cv2.findEssentialMat(curr_pts, prev_pts, focal=1.0, pp=(0, 0), method=cv2.RANSAC, prob=0.999, threshold=1.0)
            
            # Recover pose from essential matrix
            _, R, t, _ = cv2.recoverPose(E, curr_pts, prev_pts)
            
            # Update current pose based on relative motion
            self.R = R.dot(self.R)  # Update rotation matrix
            self.t = self.t + self.R.dot(t)  # Update translation vector

            return self.R, self.t
            

        def process_frame(self, frame, camera_matrix, distortion_coefficients):
            # Process each frame to estimate motion using RANSAC
            self.prev_frame = self.curr_frame
            self.curr_frame = frame
            if self.prev_frame is None:
                self.prev_frame = frame
                self.prev_keypoints, self.prev_descriptors = self.extract_features(self.prev_frame)
                return None  # Return None for the first frame
            self.curr_keypoints, self.curr_descriptors = self.extract_features(self.curr_frame)
            prev_points, curr_points = self.match_features()

            # Check if matching features failed
            if prev_points is None or curr_points is None:
                return None

            R, t = self.estimate_motion_ransac(prev_points, curr_points, camera_matrix, distortion_coefficients)
            self.update_pose(R, t)
            # Return the current camera pose
            return self.pose_from_rotation_translation(self.R, self.t)

        def pose_from_rotation_translation(self, R, t):
            # Convert rotation matrix and translation vector to Pose message
            pose = Pose()
            pose.orientation.x, pose.orientation.y, pose.orientation.z = cv2.Rodrigues(R)[0].flatten()
            pose.position.x, pose.position.y, pose.position.z = t.flatten()
            return pose

    def __init__(self):
        rospy.init_node('visual_odometry_node', anonymous=True)
        self.bridge = CvBridge()

        # Initialize variables for camera matrices and poses
        self.camera_matrix1 = None
        self.camera_matrix2 = None
        self.camera_pose1 = None
        self.camera_pose2 = None
        self.linear_acceleration = np.zeros(3)
        self.angular_velocity = np.zeros(3)

        # Camera1 subscribers
        self.camera1_sub = rospy.Subscriber('/camera/image_raw', Image, self.camera1_callback)
        self.camera1_info_sub = rospy.Subscriber('/camera/camera_info', CameraInfo, self.camera1_info_callback)

        # Camera2 subscribers
        self.camera2_sub = rospy.Subscriber('/camera2/image_raw', Image, self.camera2_callback)
        self.camera2_info_sub = rospy.Subscriber('/camera2/camera_info', CameraInfo, self.camera2_info_callback)

        # Camera1 image publisher
        self.camera_image_pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

        # Camera2 image publisher
        self.camera2_image_pub = rospy.Publisher('/camera2/image_raw', Image, queue_size=10)

        # IMU sensor subscriber
        self.imu_sub = rospy.Subscriber('/imu', Imu, self.imu_callback)

        # Visual odometry publisher
        self.vo_pub = rospy.Publisher('/visual_odometry', VisualOdometryData, queue_size=10)

        # Odometry publisher
        self.odom_pub = rospy.Publisher('/odom', Twist, queue_size=10)

        # Position publisher
        self.position_pub = rospy.Publisher('/robot_position', PoseStamped, queue_size=10)

        # Camera info publisher
        self.camera_info_pub = rospy.Publisher('/camera/camera_info', CameraInfo, queue_size=10)
        self.camera2_info_pub = rospy.Publisher('/camera2/camera_info', CameraInfo, queue_size=10)

        # IMU data publisher
        self.imu_data_pub = rospy.Publisher('/imu', Imu, queue_size=10)

        # IMU sensor subscriber
        self.imu_data_sub = rospy.Subscriber('/imu', Imu, self.imu_callback)


        # Initialize the VisualOdometry object
        self.vo = self.VisualOdometry()

        # Initialize the odometry subscriber
        self.odom_sub = rospy.Subscriber('/odom', Twist, self.odom_callback)

        # Kalman filter initialization for IMU
        self.kf_imu = KalmanFilter(dim_x=6, dim_z=6)
        self.kf_imu.F = np.array([[1, 0, 0, 1, 0, 0],
                                   [0, 1, 0, 0, 1, 0],
                                   [0, 0, 1, 0, 0, 1],
                                   [0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 1, 0],
                                   [0, 0, 0, 0, 0, 1]])  # State transition matrix
        self.kf_imu.H = np.array([[1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 0],
                                   [0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 1, 0],
                                   [0, 0, 0, 0, 0, 1]])  # Measurement matrix
        self.kf_imu.P *= 1000  # Covariance matrix
        self.kf_imu.R = np.diag([1, 1, 1, 1, 1, 1])  # Measurement noise
        self.kf_imu.Q = np.eye(6)  # Process noise

        # Kalman filter initialization for Odometry
        self.kf_odom = KalmanFilter(dim_x=3, dim_z=3)
        self.kf_odom.F = np.array([[1, 1, 0],
                                   [0, 1, 1],
                                   [0, 0, 1]])  # State transition matrix
        self.kf_odom.H = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]])  # Measurement matrix
        self.kf_odom.P *= 1000  # Covariance matrix
        self.kf_odom.R = np.diag([1, 1, 1])  # Measurement noise
        self.kf_odom.Q = np.eye(3)  # Process noise

        # Initialize tf broadcaster for visual odometry
        self.tf_broadcaster = tf.TransformBroadcaster()

    def camera1_info_callback(self, msg):
        # Callback function for camera1 info message
        self.camera_matrix1 = np.reshape(msg.K, (3, 3))
        self.publish_camera_info(msg.width, msg.height, camera_id=1)

    def camera1_callback(self, data):
        # Callback function for camera1 image message
        cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        if self.camera_matrix1 is not None:
            self.camera_pose1 = self.process_camera_image(cv_image, self.camera_matrix1)
        self.camera_image_pub.publish(data)

    def camera2_info_callback(self, msg):
        # Callback function for camera2 info message
        self.camera_matrix2 = np.reshape(msg.K, (3, 3))
        self.publish_camera_info(msg.width, msg.height, camera_id=2)

    def camera2_callback(self, data):
        # Callback function for camera2 image message
        cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        if self.camera_matrix2 is not None:
            self.camera_pose2 = self.process_camera_image(cv_image, self.camera_matrix2)
        self.camera2_image_pub.publish(data)

    def publish_camera_info(self, width, height, camera_id):
        # Helper method to publish camera info messages
        camera_info_msg = CameraInfo()
        camera_info_msg.width = width
        camera_info_msg.height = height
        self.camera_info_pub.publish(camera_info_msg)  # Publish for camera1
        self.camera2_info_pub.publish(camera_info_msg)  # Publish for camera2

    
    def imu_callback(self, data):
        # Callback function for IMU sensor message
        self.linear_acceleration = np.array([data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z])
        self.angular_velocity = np.array([data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z])

        # Kalman filter predict and update steps for IMU
        self.kf_imu.predict()
        self.kf_imu.update(np.array([self.linear_acceleration[0], self.linear_acceleration[1], self.linear_acceleration[2], 
                                    self.angular_velocity[0], self.angular_velocity[1], self.angular_velocity[2]]))

        # Kalman filter predict and update steps for Odometry
        self.kf_odom.predict()
        self.kf_odom.update(np.array([self.linear_acceleration[0], self.linear_acceleration[1], self.linear_acceleration[2]]))


    def process_camera_image(self, image, camera_matrix):
        # Process the camera image to estimate camera pose using visual odometry
        if camera_matrix is None:
            rospy.logerr("Camera matrix is not set. Cannot process image.")
            return None
        camera_pose = self.vo.process_frame(image, camera_matrix, None)
        return camera_pose

    def publish_visual_odometry(self):
        # Publish visual odometry data
        rate = rospy.Rate(10)  # Publish rate of 10 Hz
        while not rospy.is_shutdown():
            # Combine camera1, camera2, and IMU data for localization
            visual_odom_msg = VisualOdometryData()
            visual_odom_msg.camera1_pose = self.camera_pose1
            visual_odom_msg.camera2_pose = self.camera_pose2
            visual_odom_msg.imu_linear_acceleration = self.linear_acceleration
            visual_odom_msg.imu_angular_velocity = self.angular_velocity

            # Publish the visual odometry data
            self.vo_pub.publish(visual_odom_msg)

            # Publish odometry data
            self.publish_odometry()

            # Publish the robot position
            self.publish_robot_position()

            # Broadcast visual odometry transform
            self.broadcast_visual_odometry_transform()

            rate.sleep()

    def publish_odometry(self):
        # Publish odometry data based on Kalman filter estimate
        if self.kf_odom.x is not None:
            odom_msg = Twist()
            odom_msg.linear.x = self.kf_odom.x[0]
            odom_msg.linear.y = self.kf_odom.x[1]
            odom_msg.linear.z = self.kf_odom.x[2]
            self.odom_pub.publish(odom_msg)

    def publish_robot_position(self):
        # Publish robot position based on Kalman filter estimate
        if self.kf_imu.x is not None:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = rospy.Time.now()
            pose_msg.header.frame_id = "odom"
            pose_msg.pose.position.x = self.kf_imu.x[0]
            pose_msg.pose.position.y = self.kf_imu.x[1]
            pose_msg.pose.position.z = self.kf_imu.x[2]
            self.position_pub.publish(pose_msg)

    def broadcast_visual_odometry_transform(self):
        # Broadcast the visual odometry transform for camera1
        if self.camera_pose1 is not None:
            quaternion_camera1 = (
                self.camera_pose1.orientation.x,
                self.camera_pose1.orientation.y,
                self.camera_pose1.orientation.z,
                self.camera_pose1.orientation.w
            )
            translation_camera1 = (
                self.camera_pose1.position.x,
                self.camera_pose1.position.y,
                self.camera_pose1.position.z
            )
            # Broadcast transform from chassis to camera1_frame
            self.tf_broadcaster.sendTransform(translation_camera1, quaternion_camera1, rospy.Time.now(), "chassis", "camera1_frame")

        # Broadcast the visual odometry transform for camera2
        if self.camera_pose2 is not None:
            quaternion_camera2 = (
                self.camera_pose2.orientation.x,
                self.camera_pose2.orientation.y,
                self.camera_pose2.orientation.z,
                self.camera_pose2.orientation.w
            )
            translation_camera2 = (
                self.camera_pose2.position.x,
                self.camera_pose2.position.y,
                self.camera_pose2.position.z
            )
            # Broadcast transform from chassis to camera2_frame
            self.tf_broadcaster.sendTransform(translation_camera2, quaternion_camera2, rospy.Time.now(), "chassis", "camera2_frame")



    def odom_callback(self, msg):
        # Callback function for odometry message
        linear_speed = msg.linear.x
        angular_speed = msg.angular.z
        # Do something with the odometry data
        rospy.loginfo("Received Odometry: Linear Speed = %f, Angular Speed = %f" % (linear_speed, angular_speed))


if __name__ == '__main__':
    try:
        vo_node = VisualOdometryNode()
        vo_node.publish_visual_odometry()
        rospy.spin()  # Keep the main thread spinning to handle callbacks

    except rospy.ROSInterruptException:
        pass
