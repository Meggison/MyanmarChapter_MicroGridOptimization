appliance_usage = {
    "air conditioner (weekday)": {
        "number": 1,  # Assuming 1 air conditioner per household
        "power": 800,  # The power rating of the air conditioner as specified
        "num_windows": 1,  # The air conditioner is used during one main time window
        "func_time": 120,  # 2 hours of total usage per day as specified
        "func_cycle": 60,  # Minimum usage time after a switch-on event is 60 minutes
        "window_1": [1080, 1320],  # From 18:00 to 22:00 (evening usage period)
        "random_var_w": 0.2,  # 20% variability in the time window due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular usage patterns
        "fixed": "no",  # The air conditioner is not always on; usage varies according to need
        "occasional_use": 1,  # The air conditioner is used daily during the operation period
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 0,  # The air conditioner is used only on weekdays
    },
    "air conditioner (weekend)": {
        "number": 1,  # Assuming 1 air conditioner per household
        "power": 800,  # The power rating of the air conditioner as specified
        "num_windows": 1,  # The air conditioner is used during one main time window
        "func_time": 480,  # 8 hours of total usage per day as specified
        "func_cycle": 60,  # Minimum usage time after a switch-on event is 1 hour
        "window_1": [
            720,
            1320,
        ],  # From 12:00 to 22:00 (afternoon and evening usage period)
        "random_var_w": 0.2,  # 20% variability in the time window due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular usage patterns
        "fixed": "no",  # The air conditioner is not always on; usage varies according to need
        "occasional_use": 1,  # The air conditioner is used daily during the operation period
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 1,  # The air conditioner is used only on weekends
    },
    "cellphone charging": {
        "number": 1,  # Assuming 1 cellphone per household being charged
        "power": 5,  # The power rating for charging a cellphone as specified
        "num_windows": 1,  # The cellphone is typically charged during one main time window
        "func_time": 135,  # Charging time is approximately 2.25 hours (135 minutes) per day as specified
        "func_cycle": 60,  # Minimum usage time after a switch-on event is 60 minutes
        "window_1": [1080, 1215],  # From 18:00 to 20:15 (evening charging period)
        "random_var_w": 0.1,  # 10% variability in the time window due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular charging patterns
        "fixed": "no",  # The cellphone is not always charging; usage varies according to need
        "occasional_use": 1,  # The cellphone is charged daily, as it is a necessity
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 2,  # The cellphone is charged both on weekdays and weekends
    },
    "electric fan": {
        "number": 1,  # Assuming 1 fan per household
        "power": 100,  # Average power consumption of an electric fan in Myanmar
        "num_windows": 1,  # The fan is used during two main time windows, in the morning and evening
        "func_time": 300,  # Average daily usage is 5 hours (300 minutes) as specified
        "func_cycle": 60,  # Assuming the fan stays on for at least 1 hour after being switched on
        "window_1": [1080, 1380],  # From 18:00 to 23:00 (evening usage period)
        "random_var_w": 0.2,  # 20% variability in the time windows due to possible changes in the household schedule
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular usage patterns
        "fixed": "no",  # The fan is not always on; usage varies according to household needs
        "occasional_use": 1,  # The fan is used daily as it's a common appliance in Myanmar during the hot months
        "flat": "no",  # The appliance usage is subject to random variability, typical for an electric fan
        "wd_we_type": 2,  # The fan is used both on weekdays and weekends
    },
    "lighting": {
        "number": 1,  # Assuming 1 fluorescent lamp per household
        "power": 74.6,  # The power rating of a fluorescent lamp as specified
        "num_windows": 2,  # Two main usage windows: early morning and evening
        "func_time": 240,  # Assuming 4 hours of total usage per day (240 minutes)
        "func_cycle": 30,  # Minimum usage time after a switch-on event is 30 minutes
        "window_1": [300, 420],  # From 05:00 to 07:00 (morning usage period)
        "window_2": [1080, 1320],  # From 18:00 to 22:00 (evening usage period)
        "random_var_w": 0.3,  # 30% variability in the time windows due to possible changes in household activities
        "time_fraction_random_variability": 0.15,  # 15% random variability in the total usage time to account for irregular usage patterns
        "fixed": "no",  # Lighting is not always on; usage varies according to need
        "occasional_use": 1,  # The lights are used daily, especially in the morning and evening
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 2,  # The lights are used both on weekdays and weekends
    },
    "radio": {
        "number": 1,  # Assuming 1 radio per household
        "power": 2.4,  # The power rating of the radio as specified
        "num_windows": 2,  # The radio is used during two main time windows
        "func_time": 120,  # Assuming the radio is used for 2 hours per day (120 minutes)
        "func_cycle": 15,  # Minimum usage time after a switch-on event is 15 minutes
        "window_1": [360, 480],  # From 6:00 to 8:00 (morning usage period)
        "window_2": [1080, 1260],  # From 18:00 to 21:00 (evening usage period)
        "random_var_w": 0.2,  # 20% variability in the time windows due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular listening patterns
        "fixed": "no",  # The radio is not always on; usage varies according to need
        "occasional_use": 1,  # The radio is used daily, typically for news or entertainment
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 2,  # The radio is used both on weekdays and weekends
    },
    "refrigerator": {
        "number": 1,  # Assuming 1 refrigerator per household
        "power": 200,  # The power rating of the refrigerator as specified
        "num_windows": 1,  # The refrigerator operates continuously, but we'll define a single window for simplicity
        "func_time": 1440,  # The refrigerator runs 24 hours a day (1440 minutes)
        "func_cycle": 60,  # Minimum compressor cycle time is assumed to be 60 minutes
        "window_1": [
            0,
            1440,
        ],  # The refrigerator operates continuously throughout the day
        "random_var_w": 0.0,  # No variability in the operational window since it's always on
        "time_fraction_random_variability": 0.0,  # No random variability in total usage time
        "fixed": "yes",  # The refrigerator is always on when needed
        "occasional_use": 1,  # The refrigerator is used daily
        "flat": "yes",  # The usage is not subject to any random variability; it operates consistently
        "wd_we_type": 2,  # The refrigerator operates continuously, regardless of the day of the week
    },
    "television": {
        "number": 1,  # Assuming 1 television per household
        "power": 70,  # The power rating of the television as specified
        "num_windows": 1,  # The television is used during one main time window
        "func_time": 180,  # Assuming the television is used for 3 hours per day (180 minutes)
        "func_cycle": 30,  # Minimum usage time after a switch-on event is 30 minutes
        "window_1": [1080, 1260],  # From 18:00 to 21:00 (evening usage period)
        "random_var_w": 0.25,  # 25% variability in the time window due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular viewing patterns
        "fixed": "no",  # The television is not always on; usage varies according to need
        "occasional_use": 1,  # The television is used daily for entertainment or news
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 2,  # The television is used both on weekdays and weekends
    },
    "washing machine": {
        "number": 1,  # Assuming 1 washing machine per household
        "power": 400,  # The power rating of the washing machine as specified
        "num_windows": 1,  # The washing machine is typically used during one main time window
        "func_time": 60,  # Assuming the washing machine is used for 1 hour per day (60 minutes)
        "func_cycle": 30,  # Minimum usage time after a switch-on event is 30 minutes
        "window_1": [360, 420],  # From 6:00 to 7:00 (morning usage period)
        "random_var_w": 0.2,  # 20% variability in the time window due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular laundry patterns
        "fixed": "no",  # The washing machine is not always on; usage varies according to need
        "occasional_use": 0.5,  # Assuming the washing machine is used every second day on average
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 2,  # The washing machine is used both on weekdays and weekends
    },
    "water pump": {
        "number": 1,  # Assuming 1 water pump per household (for cooking, cleaning, washing, bathing)
        "power": 320,  # The power rating of the water pump as specified
        "num_windows": 1,  # The water pump is used during one main time window
        "func_time": 30,  # Assuming the water pump is used for 30 minutes per day
        "func_cycle": 30,  # Minimum usage time after a switch-on event is 30 minutes
        "window_1": [360, 480],  # From 6:00 to 8:00 (morning usage period)
        "random_var_w": 0.2,  # 20% variability in the time windows due to possible changes in household activities
        "time_fraction_random_variability": 0.1,  # 10% random variability in the total usage time to account for irregular water usage patterns
        "fixed": "no",  # The water pump is not always on; usage varies according to need
        "occasional_use": 1,  # The water pump is used daily, as water needs are constant
        "flat": "no",  # The appliance usage is subject to random variability
        "wd_we_type": 2,  # The water pump is used both on weekdays and weekends
    },
}


