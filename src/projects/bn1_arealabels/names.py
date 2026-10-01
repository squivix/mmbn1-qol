"""(area, subarea) -> label shown in the pause menu.

IDs from vgperson/MMBNSaveEditor (BN1Definitions.getSubareaName); Net/comp names follow the
Rockman EXE Zone wiki ("Category:Areas in MMBN1"). Long names are shortened to fit the box
(prebuild.py fails the build if any label is too wide). Unlisted areas show no label.
"""

AREAS = {
    0x00: {  # ACDC School
        0x00: 'Class 5-A', 0x01: 'Class 5-B', 0x02: 'Library', 0x03: '5th Grade Hall',
        0x05: 'Class 1-A', 0x06: 'Class 1-B', 0x07: 'AV Room', 0x08: 'Infirmary',
        0x09: '1st Grade Hall', 0x0B: 'Cross Hall', 0x0C: 'Storage Room', 0x0D: 'Staff Lounge',
        0x0E: 'Lounge Hall',
    },
    0x01: {  # ACDC Town
        0x00: 'ACDC Town', 0x01: 'School Entrance', 0x02: "Lan's House", 0x03: "Lan's Room",
        0x05: "Mayl's House", 0x06: "Mayl's Room", 0x07: "Dex's Room", 0x09: "Yai's Room",
        0x0B: "Higsby's", 0x0C: 'ACDC Metroline', 0x0D: 'Secret Metroline',
    },
    0x02: {  # Government Complex
        0x00: 'Gov. Complex', 0x01: 'Gov. Metroline', 0x02: 'Waterworks Lobby',
        0x03: 'SciLab Lobby', 0x04: 'Complex Hallway', 0x05: "Dad's Lab",
        0x06: 'Elevator Hall', 0x07: 'Control Room', 0x09: 'Pump Room', 0x0B: 'Filter Room',
    },
    0x03: {  # Dentown
        0x00: 'Dentown', 0x01: 'Dentown Metroline', 0x02: 'Northwest Block',
        0x03: 'Northeast Block', 0x04: 'Southeast Block', 0x05: 'Southwest Block',
        0x06: 'Antique Shop', 0x07: 'Summer School',
    },
    0x04: {  # Restaurant & Power Plant
        0x00: 'Restaurant Hall', 0x01: 'Restaurant', 0x02: 'Plant Elevator',
        0x03: 'Plant Entrance', 0x04: 'Power Plant Control', 0x05: 'Generator Room',
    },
    0x05: {  # WWW Base
        0x00: 'WWW Base', 0x01: 'Control Center', 0x02: 'Rocket Room',
        0x03: 'WWW Base 1F-2F', 0x04: 'WWW Base 2F-3F', 0x05: 'WWW Base 3F-4F',
    },
    0x80: {i: f'School Comp {i + 1}' for i in range(5)},
    0x81: {i: f'Oven Comp {i + 1}' for i in range(2)},
    0x82: {i: f'Waterworks Comp {i + 1}' for i in range(6)},
    0x83: {i: f'Traffic Comp {i + 1}' for i in range(5)},
    0x84: {i: f'Power Plant Comp {i + 1}' for i in range(4)},
    0x85: {**{i: f'WWW Comp {i + 1}' for i in range(5)}, 0x05: 'Rocket Comp'},
    0x88: {0x00: "Lan's PC", 0x01: "Mayl's Piano Comp", 0x02: "Yai's Portrait Comp", 0x03: "Dex's PC"},
    0x89: {0x00: "Dad's PC", 0x01: 'Lunch Stand Comp'},
    0x8B: {0x00: 'Fish Stand Comp'},
    0x8C: {
        0x00: 'Doghouse Comp', 0x01: 'Servbot Comp', 0x02: 'Game Machine Comp',
        0x03: 'Telephone Comp', 0x04: 'Car Comp', 0x05: 'Vending Comp',
        0x06: 'TV Comp', 0x07: 'Large Monitor Comp', 0x08: 'Control Equip. Comp',
        0x09: 'SciLab Vending', 0x0A: 'Recycled PET Comp', 0x0B: 'Big Vase Comp',
        0x0C: 'Blackboard Comp',
    },
    0x90: {**{i: f'Internet {i + 1}' for i in range(4)}, **{i: f'Undernet {i - 3}' for i in range(4, 16)}},
}
