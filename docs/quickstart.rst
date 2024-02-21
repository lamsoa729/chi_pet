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

Now we want to scan over different ``interaction_energies``. To do this we change the ``interaction_energy`` to a `ChiParam` string that tells *Chi* how to scan over the parameter.

::

    interaction_energy: ChiParam(name='ie', format_str='Ei{:.2f}', values=[.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.]) 

The values specify the values of the interaction_energy variable. In creating the directory structure, Chi will use the format string to create the directory names. In this case, the directories will be named ``Ei0.10``, ``Ei0.20``, ``Ei0.30``, etc.

.. TODO: Write what the directory structure looks like.

.. TODO: Write what the combinatorial structure looks like.

.. TODO: Write tiered scanning structure looks like.

