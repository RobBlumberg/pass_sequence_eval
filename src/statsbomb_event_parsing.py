import pandas as pd
def get_events_for_game(game_json):
    """
    Function which parses through a game JSON and return a data frame containing all shots, passes, ball receipts and carries
    performed in that game with the following features related to those events:
    - eventid
    - x start location
    - y start location
    - x end location (-1 if event is a shot)
    - y end location (-1 if event is a shot)
    - xg (-1 if event is not a shot)
    
    Arguments
    ---------
    game_json (list of dicts) 
        event level json for a game from Statsbomb
    
    Returns
    -------
    pandas.DataFrame
        containing all shots, passes, ball receipts and carries
        performed in the specified game with several features related to those events
    """

    ids = []
    names = []
    x_list = []
    y_list = []
    related = []
    x_end_list = []
    y_end_list = []
    xg_list = []

    for events in game_json:
        if events['type']['name'] in ["Pass", "Ball Receipt", "Carry", "Shot"]:
            name = events['type']['name'].lower()
            ids.append(events['id'])
            names.append(name)
            x_list.append(events['location'][0])
            y_list.append(events['location'][1])
            
            
            if name != "shot":
                x_end_list.append(events[name]["end_location"][0])
                y_end_list.append(events[name]["end_location"][1])
                xg_list.append(-1)
            else:
                x_end_list.append(-1)
                y_end_list.append(-1)
                xg_list.append(events[name]["statsbomb_xg"])
            if "related_events" in events.keys():
                related.append(events["related_events"])
            else: 
                related.append("None")
            
    
    events_df = pd.DataFrame({"ids": ids,
                             "eventname": names,
                             "x": x_list,
                             "y" : y_list,
                             "xend" : x_end_list,
                             "yend" : y_end_list,
                             "statsbombxg" : xg_list,
                             "related events": related})
    
    return events_df.set_index("ids")