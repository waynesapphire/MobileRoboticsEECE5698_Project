#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
import random as rand
import math as mat

class GoToPose():
    def __init__(self):

        self.goal_sent = False

	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)
	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(60)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)
    
def dist(p1, p2):
	return mat.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) 
    
def getwp():
	wps=[]
	new_wps=[]
	while len(wps) <5:
	  tem =(rand.uniform(0,6),rand.uniform(0,3))
	  x=0
	  for item in wps:
	    if dist(tem,item) <= 0.5:
		    x=1
	  if x==0:
		  wps.append(tem)
	for item in wps:
	  new_item =(mat.sqrt(item[0]**2+item[1]**2),item[0],item[1])
	  new_wps.append(new_item)
	new_wps.sort()
	return new_wps
		
	    

if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)
	wps=getwp()
        # Customize the following values so they are appropriate for your location
	# x_wp1 = float(raw_input("Please enter x value: "))
	# y_wp1 = float(raw_input("Please enter y value: "))
        # position = {'x': x_wp1, 'y' : y_wp1}
########################################################### 1
        navigator = GoToPose()
	position = {'x': wps[0][1], 'y' : wps[0][2]}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 1st waypoint")
        else:
            rospy.loginfo("Shucks, I can't reach the 1st waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 2
        position = {'x': wps[1][1], 'y' : wps[1][2]}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 2nd waypoint")
        else:
            rospy.loginfo("Shucks, I can't reach the 2nd waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 3
        position = {'x': wps[2][1], 'y' : wps[2][2]}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 3rd waypoint")
        else:
            rospy.loginfo("Shucks, I can't reach the 3rd waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 4
        position = {'x': wps[3][1], 'y' : wps[3][2]}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 4th waypoint")
        else:
	    rospy.loginfo("Shucks, I can't reach the 4th waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

########################################################### 5
	position = {'x': wps[4][1], 'y' : wps[4][2]}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I reached the 5th waypoint")
        else:
		rospy.loginfo("Shucks, I can't reach the 5th waypoint")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)


########################################################### Home
	position = {'x': 0, 'y' : 0}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, I went home")
        else:
            rospy.loginfo("Shucks, I can't go home")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")