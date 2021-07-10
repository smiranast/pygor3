#!/usr/bin/env python3
import pygor3 as p3

from  optparse import OptionParser
def main():
    parser = OptionParser()
    parser.add_option("-s", "--species", dest="species", help='Igor species')
    parser.add_option("-c", "--chain", dest="chain", help='Igor chain')
    parser.add_option("-b", "--batch", dest="batch", help='Batchname to identify run. If not set random name is generated')
    parser.add_option("-o", "--output", dest="output", help='filename of csv file to export data')

    (options, args) = parser.parse_args()

    if options.batch == None:
        print("batch is mandatory")
        exit()
    else:
        task = p3.IgorTask.load_from_batchname(str(options.batch))


    if options.species == None:
        print("species is mandatory")
        exit()
    else:
        task.igor_specie = str(options.species)

    if options.chain == None:
        print("species is mandatory")
        exit()
    else:
        task.igor_chain = str(options.chain)

    if options.output == None:
        print("output is mandatory")
        exit()
    else:
        output = options.output

    task.update_batch_filenames()
    task.load_IgorModel()

    strSepChar = ';'

    bs0 = p3.IgorBestScenariosVDJ()
    bsHeaderList = list(eval(str(bs0)).keys())
    strHeader = ";".join(bsHeaderList)
    fln_output_scenarios_names = task.igor_batchname + "_output_scenarios_names.csv"
    ofile = open(fln_output_scenarios_names, "w")
    ofile.write(strHeader + '\n')

    ii = 0
    chosen_V = 0
    chosen_D = 1
    chosen_J = 2
    # Keep the
    normalization_factor = 0
    with open(task.igor_fln_output_scenarios, "r") as ifile:
        inputHeader = ifile.readline()
        # Read line by line but make a group of the same seq_index
        # FIXME: read_seq_index_from_bs(ii)
        prev_seq_index = 99
        list_of_bs = list()
        for line in ifile.readlines():
            # print(line.split(strSepChar), len(line.split(strSepChar)) )
            line = line.replace("\n", "")
            bs = p3.IgorBestScenariosVDJ.load_FromLineBestScenario(line)
            bs.mdlParms = task.mdl.parms
            if bs.seq_index == prev_seq_index:
                list_of_bs.append(bs)
                normalization_factor = normalization_factor + bs.scenario_proba_cond_seq
                aaa = strSepChar.join(list(map(str, bs.to_dict_ntsequences().values())))
                ofile.write(aaa+"\n")
            else:
                # Normalize the probabilities
                if(bs.id_v_choice == chosen_V) :
                    # count this prob scenario.
                    chosen_V_prob
                normalization_factor = 0



    ofile.close()
    print("Exported scenarios in :", fln_output_scenarios_names)

if __name__ == "__main__":
    main()
