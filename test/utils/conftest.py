DUMMY_PRED_1 = {
    "dt":1682938800,
    "temp":{
        "day":16.11,
        "min":8.94,
        "max":16.16,
        "night":8.94,
        "eve":14.35,
        "morn":11.52
    },
    "weather": [
        {
            "id":802,
            "main":"Clouds",
            "description":"scattered clouds",
            "icon":"03d"}
    ]
}

EXPECTED_FORECAST_1 = "Scattered clouds. Temperature up to 16 °C."

DUMMY_PRED_2 = {
    "dt":1683025200,
    "temp":{
        "day":13.09,
        "min":5.72,
        "max":13.93,
        "night":5.72,
        "eve":11,
        "morn":8.19,
    },
    "weather": [
        {
            "id":803,
            "main":"Clouds",
            "description":"broken clouds",
            "icon":"04n"}
        ]
}

DUMMY_PRED_3 = {
    "dt":1683111600,
    "temp":{
        "day":12.56,
        "min":2.55,
        "max":15.12,
        "night":9.96,
        "eve":14.12,
        "morn":2.72,
    },
    "weather": [
        {
            "id":804,
            "main":"Clouds",
            "description":"overcast clouds",
            "icon":"04n"}
    ]
}

