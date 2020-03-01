import pandas as pd
import matplotlib.pyplot as plt
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

#helper functions for plot_event, defined below
def plot_pass(events_df, eventid, axis):
    axis.arrow(events_df.loc[eventid]["x"],
               events_df.loc[eventid]["y"],
               dx = events_df.loc[eventid]["xend"] - events_df.loc[eventid]["x"],
               dy = events_df.loc[eventid]["yend"] - events_df.loc[eventid]["y"],
               head_width=2, head_length=2)
    
def plot_carry(events_df, eventid, axis):
    axis.plot([events_df.loc[eventid]["x"], events_df.loc[eventid]["xend"]], 
              [events_df.loc[eventid]["y"], events_df.loc[eventid]["yend"]],
              linestyle="--", color = "black")

def plot_shot(events_df, eventid, axis):
    axis.scatter(events_df.loc[eventid]["x"],
                 events_df.loc[eventid]["y"],
                 marker="X", s=200)
    
def plot_event(events_df, eventid, axis):
    """
    Plots event in statsbomb json based on type. Dataframe named "events_df" must be generated 
    from get_events_for_game function first.

    Arguments:
    ----------
    events_df (pandas.DataFrame)
        - dataframe where events are stored. Output of get_events_for_game function
    eventid (string)
        - statsbomb event id
    axis (matplotlib.axes._subplots.AxesSubplot)
        - matplotlib axis on which to plot event

    Returns:
    --------
    None
    """
    if eventid not in events_df.index:
        return
    event_type = events_df.loc[eventid]["eventname"]
    if event_type == "pass":
        plot_pass(events_df, eventid, axis=axis)
    elif event_type == "carry":
        plot_carry(events_df, eventid, axis=axis)
    elif event_type == "shot":
        plot_shot(events_df, eventid, axis=axis)