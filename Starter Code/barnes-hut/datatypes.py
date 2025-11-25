from dataclasses import dataclass
import math

G = 6.67408e-11  # gravitational constant (you can scale this for visualization)

@dataclass
class OrderedPair:
    """
    A simple 2-D point or vector with named coordinates.

    Used to represent positions, velocities, and accelerations of stars
    in the simulation. Supports access via `.x` and `.y` for readability.
    """
    x: float = 0.0
    y: float = 0.0

@dataclass
class Star:
    """
    A celestial body in the simulation.

    Each Star has a position, velocity, acceleration, mass, and radius,
    along with optional RGB color values for visualization.
    The position and motion are expressed as 2D vectors (x, y).
    """
    position: OrderedPair | None = None
    velocity: OrderedPair | None = None
    acceleration: OrderedPair | None = None
    mass: float = 0.0
    radius: float = 0.0
    red: int = 255
    green: int = 255
    blue: int = 255

@dataclass
class Universe:
    """
    A square universe of given width containing a list of stars.

    The universe defines the simulation space. Its width represents the
    side length of a square region with corners at (0, 0) and (width, width).
    """
    width: float = 0.0
    stars: list[Star] = None

    def in_field(self, p: OrderedPair) -> bool:
        """
        Check if a given point is within the bounds of the universe.
        """
        return 0 <= p.x <= self.width and 0 <= p.y <= self.width

@dataclass
class Quadrant:
    """
    A square subregion of the universe given by its lower-left corner (x, y) and width.
    """
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0

@dataclass
class Node:
    """
    A quadtree node. Internal nodes store a dummy 'star' for the center of mass and have children.
    Leaf nodes may store a real star (or be empty) and have no children.
    By convention, child quadrants are ordered [NW, NE, SW, SE].
    """
    sector: Quadrant | None = None
    children: list["Node"] | None = None
    star: Star | None = None

    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf (i.e., is child-free).
        """
        return self.children is None or len(self.children) == 0

    def insert(self, s: Star) -> None:
        """
        Insert a star into the quadtree rooted at this node.
    
        Parameters:
            s: Star to insert into the quadtree
        """
        # Empty leaf node, assign star
        if self.is_leaf() and self.star is None:
            self.star = s
            return None
        # Occupied node to subdivide
        if self.is_leaf() and self.star is not None:
            existing_star = self.star
            # Create four quadrants
            self.create_children()
            # Insert the existing star into appropriate child
            child_for_existing = self.find_child(existing_star)
            child_for_existing.insert(existing_star)
            # Create placeholder with combined mass
            cog_position = center_of_gravity(existing_star, s)
            combined_mass = existing_star.mass + s.mass
            self.star = Star(
                position=cog_position,
                mass=combined_mass
            )
            # Insert the new star into appropriate child
            child_for_new = self.find_child(s)
            child_for_new.insert(s)
            return None
        # Internal node, update center of mass and use recursion
        if not self.is_leaf():
            # Update with new center of mass
            cog_position = center_of_gravity(self.star, s)
            combined_mass = self.star.mass + s.mass
            self.star = Star(
                position=cog_position,
                mass=combined_mass
            )
            # Insert into appropriate child
            appropriate_child = self.find_child(s)
            appropriate_child.insert(s)
            return None

    def create_children(self) -> None:
        """
        Subdivide this node's sector into four child quadrants:
        0: NW, 1: NE, 2: SW, 3: SE.
        """
        # Define variables
        w2 = self.sector.width / 2
        x = self.sector.x
        y = self.sector.y
        # Divide into the different quadrants
        self.children = [
            # 0: Northwest (NW)
            Node(sector=Quadrant(x=x,         y=y + w2, width=w2)),
            # 1: Northeast (NE)
            Node(sector=Quadrant(x=x + w2,    y=y + w2, width=w2)),
            # 2: Southwest (SW)
            Node(sector=Quadrant(x=x,         y=y,      width=w2)),
            # 3: Southeast (SE)
            Node(sector=Quadrant(x=x + w2,    y=y,      width=w2)),
        ]

    # find_child determines the correct quadrant child a star belongs to
    # and returns that child node.
    def find_child(self, s: Star) -> "Node":
        """
        Return the child node whose sector should contain star s.
    
        Divides the current sector into four quadrants and determines
        which quadrant contains the star's position.
    
        Children are ordered: [NW, NE, SW, SE] = [0, 1, 2, 3]
    
        Parameters:
            s: Star to locate within child quadrants
    
        Returns:
            The child Node containing the star's position
        """
        # Get star position coordinates
        star_x = s.position.x
        star_y = s.position.y
        # Get current sector bounds
        sector_left = self.sector.x
        sector_bottom = self.sector.y
        half_width = self.sector.width / 2
        # Calculate midpoint of current sector
        mid_x = sector_left + half_width
        mid_y = sector_bottom + half_width
        # Figure out which half the star is in
        is_north = star_y >= mid_y
        is_east = star_x >= mid_x
        # Map index based on quadrant
        if is_north and not is_east:
            child_index = 0  # Northwest
        elif is_north and is_east:
            child_index = 1  # Northeast
        elif not is_north and not is_east:
            child_index = 2  # Southwest
        else:
            child_index = 3  # Southeast
        return self.children[child_index]

    def calculate_net_force(self, s: Star, theta: float) -> OrderedPair:
        """
        Compute the net gravitational force on star s using Barnes-Hut approximation.
    
        Parameters:
            s: The star we're calculating force on
            theta: Barnes-Hut approximation threshold
    
        Returns:
            OrderedPair representing the net force (fx, fy) acting on star s
        """
        # Base case: no star at this node
        if self.star is None:
            return OrderedPair(0.0, 0.0)
        # Base case: missing position data
        if s.position is None or self.star.position is None:
            return OrderedPair(0.0, 0.0)
        # Calculate distance between s and this node's star
        d = distance(s.position, self.star.position)
        # Leaf node case
        if self.is_leaf():
            # Same star case
            if d == 0:
                return OrderedPair(0.0, 0.0)
            # Different star, compute direct force
            return compute_force(self.star, s)
        # Internal node case
        # If distance is zero, use recursion
        if d == 0:
            net_force = OrderedPair(0.0, 0.0)
            if self.children is not None:
                for child in self.children:
                    if child is not None:
                        force = child.calculate_net_force(s, theta)
                        net_force.x += force.x
                        net_force.y += force.y
            return net_force
        # Calculate Barnes-Hut ratio
        ratio = self.sector.width / d
        # If small enough, use approximation
        if ratio < theta:
            return compute_force(self.star, s)
        # Otherwise use recursion
        net_force = OrderedPair(0.0, 0.0)
        if self.children is not None:
            for child in self.children:
                if child is not None:
                    force = child.calculate_net_force(s, theta)
                    net_force.x += force.x
                    net_force.y += force.y
        return net_force

@dataclass
class QuadTree:
    """
    A wrapper around the root node of a Barnes–Hut quadtree.

    Provides an interface for inserting stars, building the spatial tree,
    and calculating net gravitational forces using hierarchical aggregation.
    """
    root: Node | None = None

    def insert(self, s: Star) -> None:
        self.root.insert(s)

# To prevent circular import issues, we define these functions here.

def center_of_gravity(*stars: Star) -> OrderedPair:
    """
    Compute the center of gravity of an arbitrary number of Star objects.

    Parameters:
        *stars: Any number of Star objects.

    Returns:
        OrderedPair: The (x, y) coordinates of the center of gravity.
    """
    # Define variables
    total_mass = 0.0
    sum_x = 0.0
    sum_y = 0.0
    # Calculate weighted sums
    for s in stars:
        m = s.mass
        total_mass += m
        sum_x += s.position.x * m
        sum_y += s.position.y * m
    # Handle edge case
    if total_mass == 0:
        return OrderedPair(0.0, 0.0)
    # Compute the weighted average
    return OrderedPair(sum_x / total_mass, sum_y / total_mass)

def compute_force(s1: Star, s2: Star) -> OrderedPair:
    """
    Compute the gravitational force exerted by s1 on s2.
    Uses Newton's law of universal gravitation.
    𝐹 = G * (m1 * m2) / r²
    """
    d = distance(s1.position, s2.position)
    F = G * s1.mass * s2.mass / (d * d)  
    
    delta = (s1.position.x - s2.position.x, s1.position.y - s2.position.y)
    force = OrderedPair(F * (delta[0] / d), F * (delta[1] / d))
    return force

def distance(p1: OrderedPair, p2: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points.
    """
    dx, dy = (p1.x - p2.x, p1.y - p2.y)
    return math.sqrt(dx * dx + dy * dy)