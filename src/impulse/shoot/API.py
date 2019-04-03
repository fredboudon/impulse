# -*- coding: latin-1 -*-

import generic_functions


def main(g):
    CO2 = 400
    plant_carbon_acquisition = 0
    plant_respiration = 0
    plant_area = 0
    plant_carbon_remobilisation = 0
    plant_nitrogen_remobilisation = 0

    # Transpiration plant
    plant_transpiration = sum(g.property('transpiration'))

    # Iterate over plant structure
    for vid in g.vertices():
        vid_properties = g.get_vertex_property(vid)

        # Organ photosynthesis
        plant_carbon_acquisition += generic_functions.carbon_acquisition(vid_properties['PAR'], CO2, vid_properties['nitrogen'], vid_properties['area'], vid_properties['temperature'])

        # Organ respiration
        plant_respiration += generic_functions.respiration(vid_properties['area'], vid_properties['temperature'])

        # Organ senescence and remob CN
        senesc_model = generic_functions.senescence(vid_properties['nitrogen'], vid_properties['area'], vid_properties['PAR'], vid_properties['carbon'])
        plant_area += senesc_model[0]
        plant_carbon_remobilisation += senesc_model[1]
        plant_nitrogen_remobilisation += senesc_model[2]

    # Calculate plant net C acquisition
    plant_net_C = generic_functions.plant_net_C(plant_carbon_acquisition, plant_respiration, plant_carbon_remobilisation)

    # N influx from roots
    nitrogen_influx_from_roots = generic_functions.nitrogen_influx_from_roots(g.roots.get_vertex_properties['conc_nitrates_roots'], plant_transpiration)
    total_N_flux = nitrogen_influx_from_roots + plant_nitrogen_remobilisation
    plant_potential_demand = sum(g.property('carbon_demand'))

    for vid in g.vertices():
        vid_properties = g.get_vertex_property(vid)
        # Organ C allocation
        vid_properties['carbon'] += generic_functions.carbon_allocation(vid_properties['carbon_demand'], plant_potential_demand, plant_net_C)
        # Organ N allocation
        vid_properties['nitrogen'] += generic_functions.nitrogen_allocation(vid_properties['transpiration'], plant_transpiration, total_N_flux)
