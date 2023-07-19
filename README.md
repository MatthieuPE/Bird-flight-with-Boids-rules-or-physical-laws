# Bird flight with Boids rules or physical-laws

Understanding collective behavior presents a scientific challenge across biology, physics, and social sciences, often complicated by numerous system parameters. In 1987, Craig W Reynolds proposed three simple rules to simulate bird flight, leading to the creation of the Boids artificial life program, widely utilized in simulating crowds in cinema.

This project focuses on the simulation of 2D bird swarms in an infinite sky, employing these rules. Additionally, we developed a model based on physical laws, aiming to approximate the collective behavior of birds.

## *Order1_Boids-or-Physics.py*
This file offers the option to utilize Boids rules or physical laws for simulation. However, it should be noted that the resolution is limited to first order, which may affect precise conservation of energy for physics systems.

## *Order4_Physics.py*
This introduces an order 4 method utilizing Runge Kutta, enabling more precise conservation of energy in physics systems, along with the emergent collective behavior observed in bird groups.
