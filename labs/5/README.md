# Lab 5

You can find slides to this report [here](https://docs.google.com/presentation/d/1NuDpnbKnr5Q-sfzRN80VtYCx-H2BmiSQMGYetTSKh0Y/edit?usp=sharing).

## **Overview and Motivations**
### *Mohammed Nasir*

## **Proposed Approach**
### *Tanya Smith*

In order to localize the robot on a known map of the MIT Stata building basement, we implemented the Monte Carlo Localization particle filter method. The word “particle” in this method refers to the fact that we maintained a cloud of particles representing possible locations and orientations for the car, and the word “filter” refers to the fact that certain particles were periodically filtered out based on having a low probability of accurately describing the car’s position. 

As subcomponents of this method, we implemented a motion model and a sensor model, and used the particle filter to put the two together. On each timestep, the motion model updated the locations and orientations of each particle based on the odometry of the robot. The details of this odometry calculation are explained in the motion model subsection below. Periodically, the sensor model calculated the probability for each particle that it accurately represented the car’s current location; the particle filter would then resample a new particle cloud according to these probabilities. The details of how often the sensor model was called were chosen to optimize the speed and responsiveness of our code, and are explained in more detail in the sensor model subsection below.

__**Technical Approach: Motion Model**__

At every timestep, the motion model updated the locations and orientations of each particle based on the proprioceptive odometry data of the robot; this essentially means using the robot’s linear and angular velocities to calculate new positions based on the physical laws of motion. 

To understand the calculations necessary to make these updates, we will define the concept of the world frame and the body frame. The frame of reference means the axes with respect to which we are defining the positions and orientations of the particle. If the location of a particle is given in the world frame, it means the frame of reference of the global map. If it is given in the body frame, it means the frame of reference of the car, which changes depending on the movements of the car.

To update the position of each particle, we used the linear and angular velocities of the odometry data to calculate the changes in location and orientation. Because the odometry data we subscribed to was given in the body frame of the car, we then used a rotation matrix to transform these changes into the world frame. Finally, we added the changes to the old location and orientation to obtain the new ones. In simulation, we also added Gaussian noise to these changes, to account for the unavoidable noisiness of the real robot’s odometry data.

Due to this noise in the odometry data, whether real or simulated, using the motion model alone is not enough to perform accurate localization. The noise causes the locations of the particles to diverge over time until the particle cloud is far too large and inaccurate to be at all useful. This is demonstrated in Figure 1 below, in which the particle cloud diverges when the motion model is the only code affecting the locations of the particles. In order to combat this divergence, we used periodic sensor model updates based on exteroceptive measurements, which is explained in the next subsection.
