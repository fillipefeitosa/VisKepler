config_nuts4 = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [
                {
                    "dataId": "rowek3uu",
                    "name": "NUTSII_DSG",
                    "value": [],
                    "enlarged": False,
                    "plotType": "histogram",
                    "yAxis": None,
                }
            ],
            "layers": [
                {
                    "id": "hmb3o0s",
                    "type": "geojson",
                    "config": {
                        "dataId": "rowek3uu",
                        "label": "Demografia Portugal 2030-2040",
                        "color": [255, 203, 153],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {
                            "geojson": "geometry"
                        },  # REMEMBER THIS LINE. IT IS THE KEY TO THE PROBLEM
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
                                "reversed": False,
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
                            "elevationScale": 70.7,
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
                        "rowek3uu": [
                            {"name": "NUTSII_DSG", "format": None},
                            {"name": "NUTSIII_DSG", "format": None},
                            {"name": "CONCELHO_DSG", "format": None},
                            {"name": "Total_Fechada_2040", "format": None},
                            {"name": "ratio_2040", "format": None},
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
            "latitude": 39.05464932813073,
            "longitude": -8.96162241262812,
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
