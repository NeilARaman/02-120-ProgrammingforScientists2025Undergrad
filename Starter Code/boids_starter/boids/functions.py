from datatypes import OrderedPair, Boid, Sky 
import math

def distance(p0: OrderedPair, p1: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points in 2D space.
    Input:
        p0 (OrderedPair): The first point, with x and y coordinates.
        p1 (OrderedPair): The second point, with x and y coordinates.
    Output:
        float: The Euclidean distance between p0 and p1.
    """
    dx = p0.x - p1.x
    dy = p0.y - p1.y
    return math.sqrt(dx * dx + dy * dy)

def sum_vectors(vectors: list[OrderedPair]) -> OrderedPair:
    """
    Sum all OrderedPair objects in the input list element-wise.

    Args:
        vectors (list[OrderedPair]): A list of OrderedPair objects containing x and y coordinates.

    Returns:
        OrderedPair: A new OrderedPair containing the summed x and y values.
    """
    # Defines base totals
    total_x = 0.0
    total_y = 0.0
    # Sums each vector
    for vector in vectors:
        total_x += vector.x
        total_y += vector.y
    return OrderedPair(total_x, total_y)

def limit_speed(vel: OrderedPair, max_speed: float) -> OrderedPair:
    """
    Limit the speed of a velocity vector if its magnitude exceeds max_speed.

    Args:
        vel (OrderedPair): The current velocity vector (vx, vy).
        max_speed (float): The maximum allowed speed.

    Returns:
        OrderedPair: A new velocity vector scaled down below max_speed.
    """
    # Defines origin and then computes speed from there
    origin = OrderedPair(0.0, 0.0)
    speed = distance(origin, vel)
    # Scale down if above max_speed
    if speed > max_speed:
        scale = max_speed / speed
        return OrderedPair(vel.x * scale, vel.y * scale)
    return OrderedPair(vel.x, vel.y)

def net_acceleration_due_to_cohesion(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the net acceleration acting on boid i due to cohesion.

    Args:
        current_sky (Sky): The current Sky state containing all boids and parameters.
        i (int): The index of the boid which cohesion acceleration is being calculated.

    Returns:
        OrderedPair: The averaged cohesion acceleration vector acting on boid i.
    """
    # Define variables
    target = current_sky.boids[i]
    total_x = 0.0
    total_y = 0.0
    count = 0
    # Loop over all boids
    for j, boid in enumerate(current_sky.boids):
        # If itself, skip
        if j == i:
            continue
        # Get distance
        d = distance(target.position, boid.position)
        # Look at neighbors greater than 0 and inside, apply formula
        if d > 0 and d < current_sky.proximity:
            total_x += current_sky.cohesion_factor * (boid.position.x - target.position.x) / d
            total_y += current_sky.cohesion_factor * (boid.position.y - target.position.y) / d
            count += 1  
    if count == 0:
        return OrderedPair(0.0, 0.0)
    return OrderedPair(total_x / count, total_y / count)

def net_acceleration_due_to_alignment(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the net acceleration acting on boid i due to alignment.

    Args:
        current_sky (Sky): The current Sky state containing all boids and parameters.
        i (int): The index of the boid which alignment acceleration is being computed.

    Returns:
        OrderedPair: The averaged alignment acceleration vector acting on boid i.
    """
    # Define variables
    target = current_sky.boids[i]
    total_x = 0.0
    total_y = 0.0
    count = 0
    # Loop over all boids
    for j, boid in enumerate(current_sky.boids):
        # If same, continue
        if j == i:
            continue
        # Calculate distance
        d = distance(target.position, boid.position)
        # Checks if close enough to influence alignment
        if d > 0 and d < current_sky.proximity:
            total_x += current_sky.alignment_factor * (boid.velocity.x) / d
            total_y += current_sky.alignment_factor * (boid.velocity.y) / d
            count += 1
    if count == 0:
        return OrderedPair(0.0, 0.0)
    return OrderedPair(total_x / count, total_y / count)

def net_acceleration_due_to_separation(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the net acceleration acting on boid i due to separation.

    Args:
        current_sky (Sky): The current Sky state containing all boids and parameters.
        i (int): The index of the boid which separation acceleration is being calculated.

    Returns:
        OrderedPair: The averaged separation acceleration vector acting on boid i.
    """
    # Define variables
    target = current_sky.boids[i]
    total_x = 0.0
    total_y = 0.0
    count = 0
    # Loop over all boids
    for j, other in enumerate(current_sky.boids):
        # If same, continue
        if j == i:
            continue
        # Calculate distance
        d = distance(target.position, other.position)
        # Seperates if close enough to be a threat
        if d > 0 and d < current_sky.proximity:
            total_x += current_sky.separation_factor * (target.position.x - other.position.x) / (d * d)
            total_y += current_sky.separation_factor * (target.position.y - other.position.y) / (d * d)
            count += 1
    if count == 0:
        return OrderedPair(0.0, 0.0)
    return OrderedPair(total_x / count, total_y / count)

def update_acceleration(current_sky: Sky, i: int) -> OrderedPair:
    """
    Compute the updated acceleration for boid i as the sum of
    separation, alignment, and cohesion accelerations.

    Args:
        current_sky (Sky): The current Sky state containing all boids and parameters.
        i (int): The index of the boid which acceleration is being updated.

    Returns:
        OrderedPair: The new acceleration vector acting on boid i.
    """
    seperation = net_acceleration_due_to_separation(current_sky, i)
    alignment = net_acceleration_due_to_alignment(current_sky, i)
    cohesion = net_acceleration_due_to_cohesion(current_sky, i)
    return sum_vectors([seperation, alignment, cohesion])

def update_velocity(b: Boid,
                    old_acceleration: OrderedPair,
                    max_boid_speed: float,
                    time_step: float) -> OrderedPair:
    """
    Update the velocity of boid b using the dynamic equations, then enforce the max speed limit.

    Args:
        b (Boid): The boid which velocity is being updated.
        old_acceleration (OrderedPair): The acceleration from the previous time step.
        max_boid_speed (float): The maximum allowed speed for the boid.
        time_step (float): The time interval between generations.

    Returns:
        OrderedPair: The updated and limited velocity vector.
    """
    # Compute calculations
    avg_accel = OrderedPair(
        0.5 * (old_acceleration.x + b.acceleration.x),
        0.5 * (old_acceleration.y + b.acceleration.y),
    )
    new_vel = sum_vectors(
        [b.velocity,
        OrderedPair(avg_accel.x * time_step, avg_accel.y * time_step)]
    )
    return limit_speed(new_vel, max_boid_speed)

def update_position(b: Boid,
                    old_acceleration: OrderedPair,
                    old_velocity: OrderedPair,
                    sky_width: float,
                    time_step: float) -> OrderedPair:
    """
    Update the position of boid b using the gravity/boids kinematics rule and wrapping.

    Args:
        b (Boid): The boid which position is being updated.
        old_acceleration (OrderedPair): Acceleration from the previous step.
        old_velocity (OrderedPair): Velocity from the previous step.
        sky_width (float): Width of the square sky.
        time_step (float): Time interval between generations.

    Returns:
        OrderedPair: The updated/wrapped position.
    """
    # Get base position
    new_x = b.position.x + old_velocity.x * time_step + 0.5 * old_acceleration.x * (time_step * time_step)
    new_y = b.position.y + old_velocity.y * time_step + 0.5 * old_acceleration.y * (time_step * time_step)
    # Torus wrap
    new_x = new_x % sky_width
    new_y = new_y % sky_width
    return OrderedPair(new_x, new_y)

def copy_sky(current_sky: Sky) -> Sky:
    """
    Create a deep copy of a Sky object, duplicating all its parameters and boids.
    Input:
        current_sky (Sky): The Sky instance to be copied, containing boids and 
                           simulation parameters (e.g., width, max speed, proximity).
    Output:
        Sky: A new Sky object with identical properties and boid data as the input, 
             but stored in separate memory so changes to one do not affect the other.
    """
    new_sky = Sky()
    new_sky.width = current_sky.width
    new_sky.max_boid_speed = current_sky.max_boid_speed
    new_sky.proximity = current_sky.proximity
    new_sky.separation_factor = current_sky.separation_factor
    new_sky.alignment_factor = current_sky.alignment_factor
    new_sky.cohesion_factor = current_sky.cohesion_factor

    new_boids = []
    for b in current_sky.boids:
        pos_copy = OrderedPair(b.position.x, b.position.y)
        vel_copy = OrderedPair(b.velocity.x, b.velocity.y)
        acc_copy = OrderedPair(b.acceleration.x, b.acceleration.y)
        new_boids.append(Boid(pos_copy, vel_copy, acc_copy))

    new_sky.boids = new_boids
    return new_sky

def update_sky(current_sky: Sky, time_step: float) -> Sky:
    """
    Iterate the boids system by one time step.

    Args:
        current_sky (Sky): The current system snapshot.
        time_step (float): The time interval for one simulation step.

    Returns:
        Sky: A new Sky snapshot after iterating one generation.
    """
    # Make a copy of the current sky, get number of boids for looping
    next_sky = copy_sky(current_sky)
    n = len(current_sky.boids)
    # Calculate new accelerations from the current sky
    for i in range(n):
        next_sky.boids[i].acceleration = update_acceleration(current_sky, i)
    # Loop through and update velocities
    for i in range(n):
        old_acc = current_sky.boids[i].acceleration
        next_sky.boids[i].velocity = update_velocity(
            next_sky.boids[i],
            old_acc,
            current_sky.max_boid_speed,
            time_step
        )
    # Loop through and update + wrap positions using previous velocity & acceleration
    for i in range(n):
        old_acc = current_sky.boids[i].acceleration
        old_vel = current_sky.boids[i].velocity
        next_sky.boids[i].position = update_position(
            next_sky.boids[i],
            old_acc,
            old_vel,
            current_sky.width,
            time_step
        )
    return next_sky

def simulate_boids(initial_sky: Sky, num_gens: int, time_step: float) -> list[Sky]:
    """
    Run the boids simulation starting from initial_sky.

    Args:
        initial_sky (Sky): The initial state of the system.
        num_gens (int): Number of simulation steps to run.
        time_step (float): Duration of each simulation step.

    Returns:
        list[Sky]: A list of Sky snapshots where index 0 is the initial state
        and each subsequent element is produced by one update step.
    """
    # Start the list with a copy of the initial sky
    time_points: list[Sky] = [copy_sky(initial_sky)]
    # Iterate the system num_gens times
    current = time_points[0]
    for _ in range(num_gens):
        current = update_sky(current, time_step)
        time_points.append(current)
    return time_points