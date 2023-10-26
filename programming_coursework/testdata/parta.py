from typing import Final

highest_price_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(start_date='01/01/2016', end_date='31/01/2016', expected_result=462.92),
    dict(start_date='01/02/2016', end_date='28/02/2016', expected_result=447.61),
    dict(start_date='01/12/2016', end_date='31/12/2016', expected_result=982.57),
)

lowest_price_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(start_date='01/01/2016', end_date='31/01/2016', expected_result=350.39),
    dict(start_date='01/02/2016', end_date='28/02/2016', expected_result=365.27),
    dict(start_date='01/12/2016', end_date='31/12/2016', expected_result=741.08),
)

max_volume_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(start_date='01/01/2016', end_date='31/01/2016', expected_result=268141.73),
    dict(start_date='01/02/2016', end_date='28/02/2016', expected_result=111626.76),
    dict(start_date='01/12/2016', end_date='31/12/2016', expected_result=102224.08),
)

best_avg_value_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(start_date='01/01/2016', end_date='31/01/2016', expected_result=455.5523025617217),
    dict(start_date='01/02/2016', end_date='28/02/2016', expected_result=439.0143960593451),
    dict(start_date='01/12/2016', end_date='31/12/2016', expected_result=968.9494656981099),
)

moving_average_test_data: Final[tuple[dict[str, ...], ...]] = (
    dict(start_date='01/01/2016', end_date='31/01/2016', expected_result=411.89),
    dict(start_date='01/02/2016', end_date='28/02/2016', expected_result=402.73),
    dict(start_date='01/12/2016', end_date='31/12/2016', expected_result=824.83),
)
