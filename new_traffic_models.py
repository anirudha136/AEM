__author__ = 'anirudha'
from numpy import *


def departure_flows(queue_length,arrival_rate,green_times,saturation_flow):
    dep1 = queue_length + arrival_rate
    dep2 = queue_length + (arrival_rate/green_times)*(green_times-queue_length/saturation_flow)
    if dep1<dep2:
        return dep1
    else:
        return dep2

def arrival_rate(prev_departure_rate,theta,smoothing_factor,prev_arrival_rate):
    '''

    :param prev_departure_rate:
    :param theta:
    :param smoothing_factor:
    :param prev_arrival_rate:
    :return:
    '''
    arrival_rate_current = smoothing_factor*theta*prev_departure_rate + (1-smoothing_factor)*prev_arrival_rate
    return arrival_rate_current

def queue_length(prev_queue_length,prev_arrival_rate,prev_departure_rate):
    '''

    :param prev_queue_length:
    :param prev_arrival_rate:
    :param prev_departure_rate:
    :return:
    '''
    queue_length_current = prev_queue_length +prev_arrival_rate - prev_departure_rate
    return queue_length_current

def green_time():
    return

def offset():
    return phi
