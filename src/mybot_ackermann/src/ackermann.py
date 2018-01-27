#!/usr/bin/env python

class Ackermann():
    def __init__(self):
        #acceleration | speed
        self.speed = 0.0
        #value between -1.0 and 1.0 | straight 0.0
        self.steering = 0.0

        #init ros_node
        rospy.init_node('ackermann_control', anonymous=True)
        #init publisher
        self.pub_acc_left = rospy.Publisher("/mybot/left_rear_wheel_effort_controller/command", Float64, queue_size=10)
        self.pub_acc_right = rospy.Publisher("/mybot/right_rear_wheel_effort_controller/command", Float64, queue_size=10)
        self.pub_steering_left = rospy.Publisher("/mybot/left_steering_hinge_position_controller/command", Float64,
                                            queue_size=10)
        self.pub_steering_right = rospy.Publisher("/mybot/right_steering_hinge_position_controller/command", Float64,
                                             queue_size=10)

    def callback_steering(self, data):
        self.set_steering(data)

    def callback_speed(self, data):
        self.set_speed(data)

    def set_speed(self,new_speed):
        self.speed = new_speed

    def set_steering(self,new_steering):
        self.steering = new_steering

    def subscribe(self):
        # init subscriber
        self.sub_steering = rospy.Subscriber("/mybot/ackermann_steer/command", Float64, self.callback_steering)
        self.sub_speed = rospy.Subscriber("/mybot/ackermann_speed/command", Float64, self.callback_speed)

    def publish(self):
        self.pub_acc_left.publish(self.speed)
        self.pub_acc_right.publish(self.speed)
        self.pub_steering_left.publish(self.steering)
        self.pub_steering_right.publish(self.steering)


def main():
    ackerm = Ackermann()
    rate = rospy.Rate(100) # 100hz
    while not rospy.is_shutdown():
        ackerm.subscribe()
        ackerm.publish()
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
