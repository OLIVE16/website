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

When an obstacle passes the warn distance, the distances to the object are recorded by the controller, until it reaches the stop distance where the vehicle would then slam on the brakes. The purpose of the warn distance is to eliminate noise in the obstacle detection scheme—there must be at least 10 readings between the warn and stop distances before the obstacle reading is considered to be valid. The distances are varied with the vehicle's velocity, calibrated to ensure that the stop distance is just over the braking distance of the vehicle at that speed. The warn distance was arbitrarily chosen to be 20% further than the stop distance.  

In addition, the readings from the lidar have to be limited to only include the front of the vehicle. The polar coordinates returned by the lidar were converted to cartesian coordinates using simple trigonometry, and the detection region was limited to the width of the vehicle.  

## **Experimental Evaluation**  

### Wall Follower  
#### *Jordan Gamble*  

### Safety Controller  
#### *Mohammed Nasir*  

*Friction testing:*  
The first step in designing our safety controller was to experimentally determine the stopping distance of the vehicle in the Stata basement. We applied a strip of tape to one of the wheels and took a slow-motion video (at 125 frames per second) of the vehicle accelerating as fast as possible. Braking at the exact moment the vehicle passes the camera is a rather difficult task, so we instead launched from a standstill and intuitively knew it would yield the same results.  

We knew the wheelbase of the vehicle to be 25cm, so we were able to determine the scale of the video frame with respect to the real world. Analyzing the video frame-by-frame, we looked at the slip of the taped wheel: the displacement of the vehicle and instantaneous velocity at the point where the wheel makes a single turn told us the maximum acceleration possible by the car. Specifically, the wheel's circumference was 6.28cm in the video frame, but the car only moved forward 2cm when the wheel turned once (slipping over the remaining 4.28cm). Calculating the instantaneous velocity by looking at the displacement between individual frames yielded the maximum possible acceleration of the vehicle.  

*First iteration:*  
We developed the first version of the controller as per the proposed approach section. Barrier distances were calculated as a function of velocity and the experimentally-determined acceleration/deceleration limit. The vehicle's velocity was taken from the high_level_mux topic, the lidar data was taken from the scan topic, and the safety commands were published to its own safety topic that the low_level_mux gives precedence to. Upon testing this control scheme, we realized there were a couple of potential issues. We observed that the vehicle would sometimes stop rather far from the obstacle. It turns out that the velocity readings from the high_level_mux were the commanded velocities by the autonomous controller, not the actual velocity of the vehicle. In the instances where the car stopped far from the obstacle, it was traveling much slower than the commanded velocity, but considered the stopping distance of said velocity.  

We saw a potential bug in the system: in a situation where the commanded velocity has a step decrease and an obstacle appears right at that moment, the safety controller would have calculated the stop distance based on the lower velocity, despite the vehicle still traveling at or close to the higher initial velocity. To remediate this, we decided to break the rules a little bit with our second iteration of the controller.  

*Second iteration:*  
We figured it would make more sense to read the actual velocity of the vehicle rather than an arbitrary command. Thus, we subscribed directly to the vesc motor output topic. Since the safety controller published to the low_level_mux, and the low_level_mux publishes to the vesc, we effectively created a feedback loop with the safety controller.  

In this scheme, the friction coefficient that we had manually set in the code became our proportional term in what would eventually be a PD controller. The obstacle would breach the stop distance, the vehicle would slow down, which would reduce the stop distance, which in turn, slows the vehicle down further. It was slightly jittery at first, because the safety controller would publish a "zero speed" message to the motor. To remediate this, we designed a derivative controller that was technically unconventional. We did not use a change-in-error-over-timestep method. Instead, we used the natural dynamics of the system to smooth out the deceleration. Instead of publishing a "zero speed" message, we simply published the current speed, divided by a constant. This constant was effectively our D term, and it smoothed out the commanded velocity by making it proportional to the current velocity.  

## **Lessons Learned**  
#### *Tanya Smith*  

## **Future Work**  
#### *Tanya Smith*  

#### *This report was edited by Olivia Siegel.*  
