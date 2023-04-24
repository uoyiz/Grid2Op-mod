# Copyright (c) 2019-2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of Grid2Op, Grid2Op a testbed platform to model sequential decision making in power systems.

import numpy as np

from grid2op.dtypes import dt_float

_case_14_layout = [
    (-280, -81),
    (-100, -270),
    (366, -270),
    (366, -54),
    (-64, -54),
    (-64, 54),
    (450, 0),
    (550, 0),
    (326, 54),
    (222, 108),
    (79, 162),
    (-170, 270),
    (-64, 270),
    (222, 216),
]

_case_5_layout = [(0, 0), (0, 400), (200, 400), (400, 400), (400, 0)]

case14_test_layout = _case_14_layout
case14_test_TH_LIM = np.array(
    [
        352.8251645,
        352.8251645,
        183197.68156979,
        183197.68156979,
        183197.68156979,
        12213.17877132,
        183197.68156979,
        352.8251645,
        352.8251645,
        352.8251645,
        352.8251645,
        352.8251645,
        183197.68156979,
        183197.68156979,
        183197.68156979,
        352.8251645,
        352.8251645,
        352.8251645,
        2721.79412618,
        2721.79412618,
    ]
).astype(dt_float)

case14_redisp_layout = _case_14_layout
case14_redisp_TH_LIM = np.array(
    [
        3.84900179e02,
        3.84900179e02,
        2.28997102e05,
        2.28997102e05,
        2.28997102e05,
        1.52664735e04,
        2.28997102e05,
        3.84900179e02,
        3.84900179e02,
        1.83285800e02,
        3.84900179e02,
        3.84900179e02,
        2.28997102e05,
        2.28997102e05,
        6.93930612e04,
        3.84900179e02,
        3.84900179e02,
        2.40562612e02,
        3.40224266e03,
        3.40224266e03,
    ]
).astype(dt_float)

case14_real_layout = _case_14_layout
case14_real_TH_LIM = np.array(
    [
        384.900179,
        384.900179,
        380.0,
        380.0,
        157.0,
        380.0,
        380.0,
        1077.7205012,
        461.8802148,
        769.80036,
        269.4301253,
        384.900179,
        760.0,
        380.0,
        760.0,
        384.900179,
        230.9401074,
        170.79945452,
        3402.24266,
        3402.24266,
    ]
).astype(dt_float)


L2RPN_2019_layout = _case_14_layout
L2RPN_2019_dict = {
    "loads": {
        "2_C-10.61": "load_1_0",
        "3_C151.15": "load_2_1",
        "14_C63.6": "load_13_10",
        "4_C-9.47": "load_3_2",
        "5_C201.84": "load_4_3",
        "6_C-6.27": "load_5_4",
        "9_C130.49": "load_8_5",
        "10_C228.66": "load_9_6",
        "11_C-138.89": "load_10_7",
        "12_C-27.88": "load_11_8",
        "13_C-13.33": "load_12_9",
    },
    "lines": {
        "1_2_1": "0_1_0",
        "1_5_2": "0_4_1",
        "9_10_16": "8_9_16",
        "9_14_17": "8_13_15",
        "10_11_18": "9_10_17",
        "12_13_19": "11_12_18",
        "13_14_20": "12_13_19",
        "2_3_3": "1_2_2",
        "2_4_4": "1_3_3",
        "2_5_5": "1_4_4",
        "3_4_6": "2_3_5",
        "4_5_7": "3_4_6",
        "6_11_11": "5_10_12",
        "6_12_12": "5_11_11",
        "6_13_13": "5_12_10",
        "4_7_8": "3_6_7",
        "4_9_9": "3_8_8",
        "5_6_10": "4_5_9",
        "7_8_14": "6_7_13",
        "7_9_15": "6_8_14",
    },
    "prods": {
        "1_G137.1": "gen_0_4",
        "3_G36.31": "gen_1_0",
        "6_G63.29": "gen_2_1",
        "2_G-56.47": "gen_5_2",
        "8_G40.43": "gen_7_3",
    },
}
