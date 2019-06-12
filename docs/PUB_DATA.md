# 公开数据

## DSTC

http://camdial.org/~mh521/dstc/


```json
{
    "session-id": "voip-0f41c16f2f-20130402_004600", 
    "session-date": "2013-04-02", 
    "session-time": "00:46:00", 
    "caller-id": "0f41c16f2f", 
    "turns": [
        {
            "output": {
                "transcript": "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?", 
                "end-time": 9.65, 
                "start-time": 0.001132, 
                "dialog-acts": [
                    {
                        "slots": [], 
                        "act": "welcomemsg"
                    }
                ], 
                "aborted": false
            }, 
            "turn-index": 0, 
            "input": {
                "live": {
                    "asr-hyps": [
                        {
                            "asr-hyp": "expensive restaurant", 
                            "score": -0.309871
                        }, 
                        {
                            "asr-hyp": "expensive expensive restaurant", 
                            "score": -2.097412
                        }, 
                        {
                            "asr-hyp": "a restaurant", 
                            "score": -2.103754
                        }
                    ], 
                    "slu-hyps": [
                        {
                            "slu-hyp": [
                                {
                                    "slots": [
                                        [
                                            "pricerange", 
                                            "expensive"
                                        ]
                                    ], 
                                    "act": "inform"
                                }
                            ], 
                            "score": 0.9651970175568477
                        }, 
                        {
                            "slu-hyp": [
                                {
                                    "slots": [
                                        [
                                            "pricerange", 
                                            "expensive"
                                        ]
                                    ], 
                                    "act": "inform"
                                }, 
                                {
                                    "slots": [
                                        [
                                            "area", 
                                            "west"
                                        ]
                                    ], 
                                    "act": "inform"
                                }
                            ], 
                            "score": 0.022628902637937556
                        }, 
                        {
                            "slu-hyp": [
                                {
                                    "slots": [], 
                                    "act": "affirm"
                                }, 
                                {
                                    "slots": [
                                        [
                                            "pricerange", 
                                            "expensive"
                                        ]
                                    ], 
                                    "act": "inform"
                                }
                            ], 
                            "score": 0.012174079805214724
                        }
                    ]
                }
            }
        }, 
        {
            "output": {
                "transcript": "There are 57 restaurants in the expensive price range . What type of food do you want?", 
                "end-time": 18.05, 
                "start-time": 11.8446, 
                "dialog-acts": [
                    {
                        "slots": [
                            [
                                "slot", 
                                "food"
                            ]
                        ], 
                        "act": "request"
                    }, 
                    {
                        "slots": [
                            [
                                "count", 
                                57
                            ]
                        ], 
                        "act": "inform"
                    }, 
                    {
                        "slots": [
                            [
                                "pricerange", 
                                "expensive"
                            ]
                        ], 
                        "act": "impl-conf"
                    }
                ], 
                "aborted": false
            }, 
            "turn-index": 1, 
            "input": {
                "live": {
                    "asr-hyps": [
                        {
                            "asr-hyp": "european", 
                            "score": -0.004296
                        }, 
                        {
                            "asr-hyp": "european food", 
                            "score": -6.187344
                        }, 
                        {
                            "asr-hyp": "uh european", 
                            "score": -6.544938
                        }
                    ], 
                    "slu-hyps": [
                        {
                            "slu-hyp": [
                                {
                                    "slots": [
                                        [
                                            "food", 
                                            "european"
                                        ]
                                    ], 
                                    "act": "inform"
                                }
                            ], 
                            "score": 1.0
                        }
                    ]
                }
            }
        }, 
        {
            "output": {
                "transcript": "There are 3 restaurants serving european in the expensive price range . What area would you like?", 
                "end-time": 27.29, 
                "start-time": 20.1028, 
                "dialog-acts": [
                    {
                        "slots": [
                            [
                                "slot", 
                                "area"
                            ]
                        ], 
                        "act": "request"
                    }, 
                    {
                        "slots": [
                            [
                                "count", 
                                3
                            ]
                        ], 
                        "act": "inform"
                    }, 
                    {
                        "slots": [
                            [
                                "food", 
                                "european"
                            ]
                        ], 
                        "act": "impl-conf"
                    }, 
                    {
                        "slots": [
                            [
                                "pricerange", 
                                "expensive"
                            ]
                        ], 
                        "act": "impl-conf"
                    }
                ], 
                "aborted": false
            }, 
            "turn-index": 2, 
            "input": {
                "live": {
                    "asr-hyps": [
                        {
                            "asr-hyp": "north", 
                            "score": -0.169395
                        }, 
                        {
                            "asr-hyp": "what", 
                            "score": -2.457234
                        }, 
                        {
                            "asr-hyp": "north", 
                            "score": -3.645586
                        }, 
                        {
                            "asr-hyp": "north food", 
                            "score": -3.645587
                        }
                    ], 
                    "slu-hyps": [
                        {
                            "slu-hyp": [
                                {
                                    "slots": [
                                        [
                                            "area", 
                                            "north"
                                        ]
                                    ], 
                                    "act": "inform"
                                }
                            ], 
                            "score": 0.8716779044912734
                        }, 
                        {
                            "slu-hyp": [], 
                            "score": 0.10512846332050378
                        }, 
                        {
                            "slu-hyp": [
                                {
                                    "slots": [], 
                                    "act": "affirm"
                                }, 
                                {
                                    "slots": [
                                        [
                                            "area", 
                                            "north"
                                        ]
                                    ], 
                                    "act": "inform"
                                }
                            ], 
                            "score": 0.023193632188222874
                        }
                    ]
                }
            }
        }, 
        {
            "output": {
                "transcript": "I'm sorry but there is no european restaurant in the north of town", 
                "end-time": 36.38, 
                "start-time": 29.8, 
                "dialog-acts": [
                    {
                        "slots": [
                            [
                                "area", 
                                "north"
                            ], 
                            [
                                "food", 
                                "european"
                            ]
                        ], 
                        "act": "canthelp"
                    }
                ], 
                "aborted": true
            }, 
            "turn-index": 3, 
            "input": {
                "live": {
                    "asr-hyps": [
                        {
                            "asr-hyp": "thank you goodbye", 
                            "score": -0.322816
                        }, 
                        {
                            "asr-hyp": "thank you goodbye bye", 
                            "score": -2.069746
                        }, 
                        {
                            "asr-hyp": "thank you good", 
                            "score": -2.145897
                        }
                    ], 
                    "slu-hyps": [
                        {
                            "slu-hyp": [
                                {
                                    "slots": [], 
                                    "act": "bye"
                                }
                            ], 
                            "score": 1.0
                        }
                    ]
                }
            }
        }
    ], 
    "system-specific": {
        "dialog-manager": 2, 
        "acoustic-condition": 1
    }
}
```