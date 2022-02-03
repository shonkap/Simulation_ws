#! /usr/bin/env python

#This controller just goes straight to goal...
import rospy
from nav_msgs.msg import Odometry
from tf import transformations
from geometry_msgs.msg import Point, Twist, PoseStamped
import math

robpos = Point()
robpos.x = 0.0
robpos.y = 0.0 

goal = Point()
goal.x = 0.0
goal.y = 0.0

slinx = 0.0
slinz = 0.0

goal_met = True

yaw = 0.0

speed = None
pub = None

def newGoal(msg):
    global goal
    global goal_met

    goal_met = False
    goal.x = msg.pose.position.x
    goal.y = msg.pose.position.y
    return

def newOdom(msg):
    global robpos
    global yaw

    robpos.x = msg.pose.pose.position.x
    robpos.y = msg.pose.pose.position.y

    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw = euler[2]
    #print('yaw: ', yaw)

def moveToGoal():
    global speed
    global pub

    global goal
    global goal_met

    global robpos
    global yaw

    global slinx
    global slinz

    if goal_met == False:
        rposl = 3
        rposr = -3

        inc_x = goal.x - robpos.x
        inc_y = goal.y - robpos.y

        speed.linear.x = slinx
        speed.angular.z = slinz

        
        angle_to_goal = math.atan2(inc_y, inc_x)
        dist_to_goal = math.sqrt(((goal.x - robpos.x) ** 2) + ((goal.y - robpos.y) ** 2))

	#angle to goal from robot orientation
        #print('new goal: ', goal.x, ' ', goal.y, ' yaw ', yaw, ' goal', angle_to_goal)
        if abs(angle_to_goal - yaw) < 0.3:
		#print('straight')
		slinz = 0.0
	elif (angle_to_goal >= 0.0 and yaw >= 0.0) or (angle_to_goal <= 0.0 and yaw <= 0.0):
	    if (angle_to_goal > yaw):
		#print("left s")
                slinz = rposr
	    else:
                #print("right s")
		slinz = rposl
	elif (angle_to_goal >= 0.0 and yaw <= 0.0) or (angle_to_goal <= 0.0 and yaw >= 0.0):
	    if yaw < 0:
                if(3.14 + yaw + 3.14 - angle_to_goal) > (angle_to_goal - yaw): 
		    #print("right dl")
		    slinz = rposr
		else:
	            #print("left dl")
		    slinz = rposl
	    else:
                if(3.14 + angle_to_goal + 3.14 - yaw) > (yaw - angle_to_goal): 
		    #print("left dg")
		    slinz = rposl
		else:
		    #print("right dg")
		    slinz = rposr

        speed.angular.z = slinz

        #move in straight line to goal
        if abs(angle_to_goal - yaw) > 1:
	    slinx = 0.1
            speed.linear.x = slinx
        if dist_to_goal > .1:
            slinx = 1
            speed.linear.x = slinx
        else:
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            pub.publish(speed)
            slinz = 0.0
            slinx = 0.0
	    goal_met = True
            return

        pub.publish(speed)
    else:
        speed.linear.x = 0.0
        speed.angular.z = 0.0
        pub.publish(speed)
    
    return

def main():
    global speed
    global pub

    rospy.init_node("speed_controller")

    sub = rospy.Subscriber("/odom", Odometry, newOdom)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    speed = Twist()

    goal = rospy.Subscriber("/move_base_simple/goal", PoseStamped, newGoal)
    
    rate_hz = 10
    rate = rospy.Rate(rate_hz)
    while not rospy.is_shutdown():
        moveToGoal()
        rate.sleep()

if __name__ == "__main__":
    main()

