#!/usr/bin/env python
import serial
import rospy
from serial_ros_comm.msg import StringStamped

ser = serial.Serial()
pub = rospy.Publisher('read', StringStamped, queue_size=25) #10 is not enough
serial_msg = StringStamped()
serial_msg.header.frame_id = ''
sequence = 0


def read_serial():
    while ser.in_waiting > 0:
        serial_msg.data = ser.read()
        serial_msg.header.stamp = rospy.Time.now()
        pub.publish(serial_msg)

def write_serial(data):
    ser.write(data.data)
    global sequence
    if sequence != (data.header.seq - 1):
       rospy.loginfo("Lost msg - seq_prev: %u, seq: %u", sequence, data.header.seq)
    sequence = data.header.seq
    # rospy.loginfo("Write to Port %s: %s", ser.port, data.data)


def read_data_loop():
    rate = rospy.Rate(1000)  # Frequency for smallest delay not found yet
    try:
        while not rospy.is_shutdown():
            read_serial()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    rospy.init_node('serial_node', anonymous=True)
    rospy.Subscriber("write", StringStamped, write_serial)

    ser.baudrate = rospy.get_param('~baud', 19200)
    ser.port = rospy.get_param('~port', '/dev/ttyUSB0')
    ser.open()

    if ser.isOpen():
        rospy.loginfo("Port %s initalized", ser.port)
    else:
        rospy.loginfo("Initialization of Port %s failed", ser.port)

    read_data_loop()
