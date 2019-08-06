# serial_ros_comm
Transport serial data via ROS


##### To check USB-ports on linux, run the following code:
```
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do     (         syspath="${sysdevpath%/dev}";         devname="$(udevadm info -q name -p $syspath)";         [[ "$devname" == "bus/"* ]] && continue;         eval "$(udevadm info -q property --export -p $syspath)";         [[ -z "$ID_SERIAL" ]] && continue;         echo "/dev/$devname - $ID_SERIAL";     ); done
```

##### For running a single node:
```
roslaunch serial_ros_comm serial_single.launch
```
Optional parameters: `port`, `baud`, `node_name`, `read_topic`, `write_topic`

##### For running two nodes communicating with each other:
```
roslaunch serial_ros_comm serial_communication.launch
```
Optional parameters: `port1`, `port2`, `baud`, `node_name1`, `node_name2`, `read_topic1`, `read_topic2`

