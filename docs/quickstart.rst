==========
Quickstart
==========

The most common use of Chi-Pet is scanning over a configuration parameter of simulation. Let's say you have the following ``.yaml`` configuration file.

::

    # config.yaml
    run_time: 100
    dt: .01
    viscosity: 1
    interaction_energy: .5
    box_dimensions: [100., 100., 100.]
    periodic_boundarys: True
    sphere_radius: 1.
    temperature: 1.
    sphere_number: 1000

Now we want to scan over different ``interaction_energies``.


