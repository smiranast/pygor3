#!/usr/bin/env python3
import pygor3 as p3
import argparse

def generate_event_delta_Kronecker(event_nickname, event_id):
    def tmp_funct(bs:p3.IgorScenario):
        if bs[event_nickname] == event_id:
            return 1
        else:
            return 0
    return tmp_funct

def get_pairwise_prob(mdl, event_nickname1, event_nickname2):
    # create an xarray matrix with event_nickname1 and event_nickname2
    # da = xr.
    da = mdl.get_zero_xarray_from_list([event_nickname1, event_nickname2])

    def tmp_funct(bs:p3.IgorScenario):
        ev_dict_ids = {event_nickname1: bs['id_'+event_nickname1], event_nickname2: bs['id_'+event_nickname2]}
        da.loc[ev_dict_ids] = 1
        return da

    return tmp_funct


def calc_average(db:p3.IgorSqliteDB, observable_function):
    for sigma in db.fetch_IgorIndexedSeq_indexes():
        print(sigma, len(db.fetch_IgorIndexedSeq_indexes()))

# from  optparse import OptionParser
def main():
    #parser = OptionParser()
    #parser.add_option("-s", "--species", dest="species", help='Igor species')
    #parser.add_option("-c", "--chain", dest="chain", help='Igor chain')
    #parser.add_option("-b", "--batch", dest="batch", help='Batchname to identify run. If not set random name is generated')
    #parser.add_option("-o", "--output", dest="output", help='filename of csv file to export data')

    parser = argparse.ArgumentParser()
    igor_models = parser.add_argument_group('IGoR default models')

    # Use IGoR default model
    igor_models.add_argument("-s", "--species", dest="species", help='Igor species', default="human")
    igor_models.add_argument("-c", "--chain", dest="chain", help='Igor chain', default="tcr_beta")  # , type=str, choices=['TRB', 'TRA'])

    parser.add_argument("-D", "--database", dest="database", help="Igor database created with database script.", default="Ajam.db")
    parser.add_argument("--event_pair", dest="event_pair", help="Events nickname", nargs=2, default=['v_choice', 'j_choice'])

    igor_models = parser.add_argument_group('IGoR envent_pairdefault models')

    args = parser.parse_args()

    print(args)
    print(args.event_pair)
    str_event_nickname1 = args.event_pair[0]
    str_event_nickname2 = args.event_pair[1]

    # Create an IgorModel
    mdl = p3.IgorModel.load_default(args.species, args.chain)
    db = p3.IgorSqliteDB.create_db(args.database)
    fff = get_pairwise_prob(mdl, str_event_nickname1, str_event_nickname2)
    average = db.calc_IgorBestScenarios_average_of(fff)
    print(average)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10,15))
    average.plot(ax=ax)

    str_title = "$P($" + str_event_nickname1 + ", " + str_event_nickname2+"$)$"
    #ax.set_title(str_title)
    ax.set_ylabel(str_event_nickname1.replace("_", " "))
    ax.set_xlabel(str_event_nickname2.replace("_", " "))

    # plot sutilties
    import numpy as np
    v_genlabel = np.vectorize(p3.genLabel )

    XX = average[str_event_nickname2].values
    lbl_XX = average['lbl__' + str_event_nickname2].values

    YY = average[str_event_nickname1].values
    lbl_YY = average['lbl__' + str_event_nickname1].values

    ax.set_xticks(XX)
    ax.set_xticklabels(v_genlabel(lbl_XX), rotation=90)

    ax.set_yticks(YY)
    ax.set_yticklabels(v_genlabel(lbl_YY))

    fig.savefig('figura.pdf')
    # return ax

    plt.show()

    return 0

if __name__ == "__main__":
    main()