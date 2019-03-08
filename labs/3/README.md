# Lab 3  

You can find slides to this report [here](https://docs.google.com/presentation/d/1XzfDtFtvkoT-H0BVW3P9kHhvvWo48XWTCSjpks8Dee4/edit?usp=sharing).  

## **Overview and Motivations**  
#### *Olivia Siegel*  

## **Proposed Approach**  

### Wall Follower  
#### *Olivia Siegel*  

### Safety Controller  
#### *Mohammed Nasir*  

The purpose of the safety controller is to stop the vehicle from colliding with obstacles at high speeds. At the same time, the controller must not be overly cautious as to stop the vehicle when a collision was not necessarily imminent. The objective of this task was to design a safety controller that would analyze the vehicle's current trajectory and bring it to a stop at the last possible moment. To accomplish this, we set two virtual barriers at the front of the vehicle: the "warn distance" to begin tracking the position of an obstacle, and the "stop distance" to stop as quickly as possible.  

When an obstacle passes the warn distance, the distances to the object are recorded by the controller, until it reaches the stop distance where the vehicle would then slam on the brakes. The purpose of the warn distance is to eliminate noise in the obstacle detection scheme - there must be at least 10 readings between the warn and stop distances before the obstacle reading is considered to be valid. The distances are varied with the vehicle's velocity, calibrated to ensure that the stop distance is just over the braking distance of the vehicle at that speed. The warn distance was arbitrarily chosen to be 20% further than the stop distance.  

In addition, the readings from the lidar have to be limited to only include the front of the vehicle. The polar coordinates returned by the lidar were converted to cartesian coordinates using simple trigonometry, and the detection region was limited to the width of the vehicle.  

## **Experimental Evaluation**  

### Wall Follower  
#### *Jordan Gamble*  

### Safety Controller  
#### *Mohammed Nasir*  

##### *Friction testing:*  
The first step in designing our safety controller was to experimentally determine the stopping distance of the vehicle in the Stata basement. We applied a strip of tape to one of the wheels and took a slow-motion video (at 125 frames per second) of the vehicle accelerating as fast as possible. Braking at the exact moment the vehicle passes the camera is a rather difficult task, so we instead launched from a standstill and intuitively knew it would yield the same results.  

We knew the wheelbase of the vehicle to be 25cm, so we were able to determine the scale of the video frame with respect to the real world. Analyzing the video frame-by-frame, we looked at the slip of the taped wheel: the displacement of the vehicle and instantaneous velocity at the point where the wheel makes a single turn told us the maximum acceleration possible by the car. Specifically, the wheel's circumference was 6.28cm in the video frame, but the car only moved forward 2cm when the wheel turned once (slipping over the remaining 4.28cm). Calculating the instantaneous velocity by looking at the displacement between individual frames yielded the maximum possible acceleration of the vehicle.  

##### *First iteration:*  
We developed the first version of the controller as per the proposed approach section. Barrier distances were calculated as a function of velocity and the experimentally-determined acceleration/deceleration limit. The vehicle's velocity was taken from the high_level_mux topic, the lidar data was taken from the scan topic, and the safety commands were published to its own safety topic that the low_level_mux gives precedence to. Upon testing this control scheme, we realized there were a couple of potential issues. We observed that the vehicle would sometimes stop rather far from the obstacle. It turns out that the velocity readings from the high_level_mux were the commanded velocities by the autonomous controller, not the actual velocity of the vehicle. In the instances where the car stopped far from the obstacle, it was traveling much slower than the commanded velocity, but considered the stopping distance of said velocity.  

We saw a potential bug in the system: in a situation where the commanded velocity has a step decrease and an obstacle appears right at that moment, the safety controller would have calculated the stop distance based on the lower velocity, despite the vehicle still traveling at or close to the higher initial velocity. To remediate this, we decided to break the rules a little bit with our second iteration of the controller.  

##### *Second iteration:*  
We figured it would make more sense to read the actual velocity of the vehicle rather than an arbitrary command. Thus, we subscribed directly to the vesc motor output topic. Since the safety controller published to the low_level_mux, and the low_level_mux publishes to the vesc, we effectively created a feedback loop with the safety controller.  

In this scheme, the friction coefficient that we had manually set in the code became our proportional term in what would eventually be a PD controller. The obstacle would breach the stop distance, the vehicle would slow down, which would reduce the stop distance, which in turn, slows the vehicle down further. It was slightly jittery at first, because the safety controller would publish a "zero speed" message to the motor. To remediate this, we designed a derivative controller that was technically unconventional. We did not use a change-in-error-over-timestep method. Instead, we used the natural dynamics of the system to smooth out the deceleration. Instead of publishing a "zero speed" message, we simply published the current speed, divided by a constant. This constant was effectively our D term, and it smoothed out the commanded velocity by making it proportional to the current velocity.  

## **Lessons Learned**  
#### *Tanya Smith*  
There are several important technical lessons we learned as we attempted to quantitatively evaluate our wall following and safety controller performance. To measure our quantitative accuracy, we used rospy logging functionality to log the distance error of our racecar relative to desired distance from the wall, as it ran the wall follower for approximately ten minutes. We then wrote a Python script to compute the average distance error based on the roslaunch log file generated by our wall follower node. This resulted in an average distance error of 0.12 meters, which at first glance implies an accurate wall follower, but is also not informative enough to be very meaningful. The technical lessons we learned from this were that we need more robust testing data and more rigorous testing strategies. The first lesson is that we need to use data that is more representative of reality than just ten minutes of wall following on the same surface and in the same room; for example, our measurements would be more meaningful if our average error included wall following in rooms with more reflective surfaces, different floor textures, and different wall shapes. The second is that we must plan our quantitative testing strategies from the very start of the lab so that we can show the evolution of our error over time or with respect to different parameters. In this vein, we would have benefitted from showing a graph of distance error as a function of the different PD controller gains we tried for our wall follower, or a graph of stopping distances at different car velocities to show how we chose the parameters of our safety controller.  

When it came to the teamwork and communication aspects of the lab, we ran into a couple of issues that we can learn from and use to improve the effectiveness of our team. The first was fair distribution of work - we were so excited to jump into the technical aspects of the lab that we did not stop to formulate a working plan of how we would ensure that everyone could make a meaningful contribution in each module. In the future, we plan to think more carefully about this balance before anyone begins coding, so that everyone has a chance to write some code and do some testing. The second was that we did not use the potential of our four team members to its fullest; there were times when our poor planning resulted in one or two team members being stuck waiting for the others to finish a task before they could get started on their own. Instead, we plan to start distributing work in a more parallel fashion, so that everyone has something to do at all times even if someone else's part is taking longer than expected.  

## **Future Work**  
#### *Tanya Smith*  

If we were to develop this work further in the future, we would make improvements to the tuning of our wall follower and safety controller such that they would be able to adapt to a wider variety of situations or unexpected conditions. We would improve our wall following precision when turning corners and following more complex-shaped walls at higher speeds. One strategy we could try for this would be to change the PD controller gains and lookahead distance to be more responsive to changes in the velocity of the car. Another would be add an integral term to make our PD controller into a PID controller, or even change our controller entirely to implement pure pursuit instead. As for our safety controller, we would improve its robustness by making its lookahead range dependent on steering angle as well, instead of just velocity. This would improve obstacle detection and collision avoidance in situations where the car is going to encounter a safety emergency immediately after turning a corner.  

#### *This report was edited by Olivia Siegel.*  
