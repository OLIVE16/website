# Final Challenge: Fast Obstacle Avoidance

Slides for this lab are also accessible [here](https://drive.google.com/open?id=1kieycNzAH1OnR04PcUReGHFV1kBajHFnhcm2qmBWEOQ).

## **Description of Problem: Fast Obstacle Avoidance**

## **Technical Approach**

#####__**Mapping and Path Planning**__

Note: When we refer to localization in this map, we are referring to the particle filter implemented in Lab 5, and when we refer to path planning, we are referring to the search-based A* algorithm implemented in Lab 6.

One of the most important challenges in implementing fast obstacle avoidance was maintaining an accurate map with which to localize, as well as one with which to plan paths. We chose to maintain two different representations of this map, each representing the same Stata basement, but each optimized to the needs of the two purposes. We also had to consider when to dilate these maps and when to leave them undilated, the rationale for which will be discussed below.

For localization, we used the original stata basement map, undilated and free of obstacles. This map needed to be undilated because dilation alters the ground truth of objects on the map in order to be able to treat the car as a point mass when it traverses the occupancy grid. In the case of localization, we needed to maintain the ground truth of the walls around the car so that it could accurately pinpoint its location on the map. We also did not want to add obstacles to the map used by the particle filter, because we did not want to compound any error in detecting and drawing these obstacles, which would quickly make our map unusable for localizing the car. To account for the presence of these unmapped obstacles, we instead tuned the parameters of the particle filter to expect short lidar scans (e.g. the lidar hitting nearby cardboard boxes) at a higher probability, thus effectively telling the particle filter to ignore small disturbances in the hallway and prioritize using further obstacles, like the hallway walls, to orient itself.

For path planning, we chose to keep an internal representation of the map (published only for visualization purposes), that was dilated and continually updated with new obstacles based on incoming lidar scan information. This map needed to be dilated because it planned paths assuming the car was a point mass, so obstacles were inflated to create a configuration space in which the point mass could move freely without implying collisions of the physical car as a rigid body.

In order to update the map used for planning paths, we used incoming lidar scans to calculate the indices of cells in an occupancy grid that should be marked as unpermissible. This was done using the distance and angle of each lidar scan to calculate the changes in the x and y directions, applying a rotation matrix to transform these changes into the world frame. In addition to each detected obstacle cell, all of the cells in a surrounding square with side lengths based on the width of the car were also marked as occupied, effectively providing real time dilation.

In using this map updating process, we discovered that we needed a measure to prevent error from compounding over time and adding to many unpermissible regions where there were not actually obstacles. To counteract this compounding of error, we implemented a preventative clearing of the area around the car on the map every time we added new obstacles. We cleared a square with sides about as long as the hallway width, so as to correct for any mistakenly blocked out cells in the grid that would artificially trap the car such that it could not plan a path to the goal.

This processing of lidar scans did not occur on every incoming lidar message, but was rather tuned to about 10 Hz. Any faster and the planned trajectories would often flicker between two conflicting but similarly optimal options, confusing the pure pursuit controller, any slower and the path planning would not be responsive enough to “see” new obstacles coming into range quickly enough to prevent a collision. When a lidar scan was processed, we called our A* search algorithm to plan a path between the current location of the car according to the particle filter and the fixed goal point in the world frame. We found we had to adapt our A* implementation by decreasing the step size; larger step sizes are quick and can be accurate enough in long-range situations like Stata basement loop race, but will miss small obstacles entirely in the obstacle course environment, planning paths that go right through the obstacles.

#####__**Pure Pursuit Trajectory Following**__

## **Experimental Evaluation**
TBD  

## **Lessons Learned**
TBD  

## **Future Work**
TBD  
