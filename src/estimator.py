'''
input is an object in the format of:
{
    region: {
        name: "Africa",
        avgAge: 19.7,
        avgDailyIncomeInUSD: 5,
        avgDailyIncomePopulation: 0.71
    },
    periodType: "days",
    timeToElapse: 58,
    reportedCases: 674,
    population: 66622705,
    totalHospitalBeds: 1380614
}

output should be an object in the format of:
{
    data: {}, // the input data you got
    impact: {}, // your best case estimation
    severeImpact: {} // your severe case estimation
}
'''

def estimator(data):
    return {
        'data': data,
        'impact': get_impact(data, False),
        'severeImpact': get_impact(data, True)
    }


def get_impact(data, severe):
    # get the value of impact
    cases = int(data.get('reportedCases'))
    period_type = data.get('periodType')
    expected_time = int(data.get('timeToElapse'))
    total_beds = int(data.get('totalHospitalBeds'))
    region_data = data.get('region')

    requested_time = get_requested_time_in_days(period_type, expected_time)
    currently_infected = get_currently_infected(cases, severe)
    infections_by_time = get_infections_by_requested_time(
        currently_infected,
        requested_time
    )
    severe_cases = get_severe_cases_by_requested_time(infections_by_time)
    available_beds = get_expected_available_beds_by_time(
        total_beds,
        severe_cases
    )
    return {
        'currentlyInfected': currently_infected,
        'infectionsByRequestedTime': infections_by_time,
        'severeCasesByRequestedTime': severe_cases,
        'hospitalBedsByRequestedTime': available_beds,
        'casesForICUByRequestedTime': get_special_cases(
            infections_by_time,
            0.05
        ),
        'casesForVentilatorsByRequestedTime': get_special_cases(
            infections_by_time,
            0.02
        ),
        'dollarsInFlight': get_dollars_in_flight(
            region_data,
            infections_by_time,
            requested_time
        ),
    }


def get_currently_infected(reported_cases, severe):
    if severe:
        return reported_cases * 50
    return reported_cases * 10


def get_infections_by_requested_time(currently_infected, requested_time):
    # the requested time should be a value in days
    factor = requested_time // 3
    multiplier = 2 ** factor
    return currently_infected * multiplier


def get_requested_time_in_days(period_type, time_to_elapse):
    # period time can either be months, weeks or days
    if period_type == 'months':
        # a month is assumed to have 30 days
        return time_to_elapse * 30
    elif period_type == 'weeks':
        # a week is assumed to have 7 days
        return time_to_elapse * 7
    else:
        return time_to_elapse


def get_severe_cases_by_requested_time(infections_by_time):
    # severity cases that will require hospitalization are 0.15 * infections_by_time
    return int(0.15 * infections_by_time)


def get_expected_available_beds_by_time(total_hospital_beds, severe_cases):
    # expected hospital beds for COVID-19 is 0.35 * totalHospitalBeds
    available_beds = 0.35 * total_hospital_beds
    return int(available_beds - severe_cases)


def get_special_cases(infections_by_time, percentage):
    return int(infections_by_time * percentage)


def get_dollars_in_flight(region_data, infections_by_time, requested_time):
    # get the estimate of how much the economy is likely to lose daily
    daily_avg_income = float(region_data.get('avgDailyIncomeInUSD'))
    daily_avg_income_pop = float(region_data.get('avgDailyIncomePopulation'))
    daily_infections = infections_by_time / requested_time
    return int(daily_infections * daily_avg_income * daily_avg_income_pop)
