import json

config_nuts3 = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [
                {
                    "id": "bwbla5i",
                    "type": "geojson",
                    "config": {
                        "dataId": "rs1hiroye",
                        "label": "demographic_2020_2030_2040_regions",
                        "color": [255, 203, 153],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {"geojson": "geometry"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "strokeOpacity": 0.8,
                            "thickness": 0.5,
                            "strokeColor": [248, 149, 112],
                            "colorRange": {
                                "name": "ColorBrewer PiYG-6",
                                "type": "diverging",
                                "category": "ColorBrewer",
                                "colors": [
                                    "#c51b7d",
                                    "#e9a3c9",
                                    "#fde0ef",
                                    "#e6f5d0",
                                    "#a1d76a",
                                    "#4d9221",
                                ],
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846",
                                    "#900C3F",
                                    "#C70039",
                                    "#E3611C",
                                    "#F1920E",
                                    "#FFC300",
                                ],
                            },
                            "radius": 10,
                            "sizeRange": [0, 10],
                            "radiusRange": [0, 50],
                            "heightRange": [0, 500],
                            "elevationScale": 25,
                            "enableElevationZoomFactor": True,
                            "stroked": False,
                            "filled": True,
                            "enable3d": True,
                            "wireframe": False,
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center",
                            }
                        ],
                    },
                    "visualChannels": {
                        "colorField": {"name": "ratio_2040", "type": "real"},
                        "colorScale": "quantile",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "heightField": {
                            "name": "Total_Fechada_2040",
                            "type": "integer",
                        },
                        "heightScale": "linear",
                        "radiusField": None,
                        "radiusScale": "linear",
                    },
                }
            ],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "rs1hiroye": [
                            {"name": "NUTSIII_DSG", "format": None},
                            {"name": "PopAbertH_2020", "format": None},
                            {"name": "PopAbertM_2020", "format": None},
                            {"name": "PopFechH_2020", "format": None},
                            {"name": "PopFechM_2020", "format": None},
                        ]
                    },
                    "compareMode": False,
                    "compareType": "absolute",
                    "enabled": True,
                },
                "brush": {"size": 0.5, "enabled": False},
                "geocoder": {"enabled": False},
                "coordinate": {"enabled": False},
            },
            "layerBlending": "normal",
            "splitMaps": [],
            "animationConfig": {"currentTime": None, "speed": 1},
        },
        "mapState": {
            "bearing": 24,
            "dragRotate": True,
            "latitude": 38.94404299394514,
            "longitude": -9.277581664279134,
            "pitch": 50,
            "zoom": 6.9,
            "isSplit": False,
        },
        "mapStyle": {
            "styleType": "dark",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False,
            },
            "threeDBuildingColor": [
                9.665468314072013,
                17.18305478057247,
                31.1442867897876,
            ],
            "mapStyles": {},
        },
    },
}
