import csv
import os
import argparse
from datetime import datetime

staleness = [10,20,30,40,50,100,150,200,500,1000,3000]
staleness_string = []
for s in staleness:
    staleness_string.append(str(s))

def get_parameters(dir_name):
    parts = dir_name.split('-')

    # create a dictionary mapping column names to their respective values
    data = {'algorithm': parts[0],
            'threads': int(parts[2][7:]),
            'read_prop': float(parts[3][5:]),
            'value_size': int(parts[4][2:]),
            'txn_size': int(parts[5][3:]),
            'num_clients': int(parts[6][2:]),
            'num_servers': int(parts[7][2:]),
            'num_key': int(parts[8][2:]),
            'distribution': parts[-2][2:],
            'zipfian_constant': float(parts[-1][2:]),}
    return data

def get_freshness_ramp_fast(dir_name):
    final_results = {}
    tot = 0
    for stale in staleness:
        final_results[stale] = 0
    for g in os.listdir(dir_name):
        if(g.find("S") == -1):
            continue
        g = dir_name + '/' + g
        lastAp = {}
        lastFresh = {}
        key = ""
        s = g.split("/S")[1]
        for line in open(g + "/server-0.log"):
            if line.find("Freshness") == -1:
                continue
            lookoutKey = False
            lookout = False
            for word in line.split():
                if word == "key:":
                    lookoutKey = True
                    key = ""
                    continue
                elif lookoutKey:
                    key = word
                    lookoutKey = False
                if word == "=":
                    lookout = True
                elif lookout:
                    lookout = False
                    if lastAp.get(key) is None:
                        if(line.find("Round 2") != -1):
                            lastAp[key] = 2
                            lastFresh[key] = int(word)
                            for stale in staleness:
                                if(int(word) <= stale):
                                    if stale not in final_results:
                                        final_results[stale] = 0
                                    final_results[stale] += 1
                            tot += 1
                        else:
                            lastAp[key] = 1
                            lastFresh[key] = int(word)
                    else:
                        if lastAp[key] == 2:
                            if(line.find("Round 2") != -1):
                                lastFresh[key] = int(word)
                                for stale in staleness:
                                    if(int(word) <= stale):
                                        if stale not in final_results:
                                            final_results[stale] = 0
                                        final_results[stale] += 1
                                tot += 1
                            else:
                                lastAp[key] = 1
                                lastFresh[key] = int(word)
                        else:
                            if(line.find("Round 2") != -1):
                                lastAp[key] = 2
                                lastFresh[key] = int(word)
                                for stale in staleness:
                                    if(int(word) <= stale):
                                        if stale not in final_results:
                                            final_results[stale] = 0
                                        final_results[stale] += 1
                                tot += 1
                            else:
                                lastAp[key] = 1
                                lastFresh[key] = int(word)
                                tot += 1
                                for stale in staleness:
                                    if(int(word) <= stale):
                                        if stale not in final_results:
                                            final_results[stale] = 0
                                        final_results[stale] += 1
            for key in lastAp:
                if lastAp[key] == 1:
                    tot += 1
                    for stale in staleness:
                        if(lastFresh[key] <= stale):
                            if stale not in final_results:
                                final_results[stale] = 0
                            final_results[stale] += 1
    ret = []
    for s in staleness:
        ret.append(100*float(final_results[s] / tot))
    return ret

def get_freshness(dir_name, algo):
    if algo == "READ_ATOMIC_KEY_LIST" or algo == "FASTOPW":
        return get_freshness_ramp_fast(dir_name)
    ret = []
    final_results = {}
    tot = 0
    for stale in staleness:
        final_results[stale] = 0
    for g in os.listdir(dir_name):
        if g.find("S") == -1:
            continue
        g = dir_name + '/' + g
        s = g.split("/S")[1]
        for line in open(g + "/server-0.log"):
            if line.find("Freshness") == -1:
                continue
            if line.find("timestamp : -1 = ") != -1:
                continue
            lookout = False
            for word in line.split():
                if word == "=":
                    lookout = True
                elif lookout:
                    lookout = False
                    tot += 1
                    for stale in staleness:
                        if(int(word) <= stale):
                            final_results[stale] += 1
    for s in staleness:
        ret.append(100*float(final_results[s] / tot))
    return ret

def get_tp_and_latency(dir_name, num_clients):
    var = "AverageLatency(us),"   
    var99 = "99thPercentileLatency(ms),"
    var95 = "95thPercentileLatency(ms),"
    vartp = "Throughput(ops/sec),"
    final_results = 0
    fr_read = 0
    fr_write = 0
    fr_99 = 0
    fr_95 = 0
    tp_final = 0

    results = {}
    rr = {}
    rw = {}
    r99 = {}
    r95 = {}
    tp = {}
    for g in os.listdir(dir_name):
        if g.find("C") == -1:
            continue
        g = dir_name + '/' + g
        c = g.split("/C")[1]
        if results.get(c) is None:
            results[c] = 0
            rr[c] = 0
            rw[c] = 0
            r99[c] = 0
            r95[c] = 0
            tp[c] = 0
        lookout = False
        lookout_tp = False
        opr = 0
        opw = 0
        latr = 0
        latw = 0
        latr99 = 0
        latr95 = 0
        latw99 = 0
        latw95 = 0
        for line in open(g+"/run_out.log"):
            if line.find(vartp) != -1:
                for word in line.split():
                    if word == vartp:
                        lookout_tp = True
                    elif lookout_tp:
                        lookout_tp = False
                        tp[c] += float(word)
            if line.find("Operations,") != -1:
                for word in line.split():
                    if word == "Operations,":
                        lookout = True
                    elif lookout:
                        lookout = False
                        if line.find("[UPDATE-TXN]") != -1:
                            opw = float(word)
                        else:
                            opr = float(word)
            if line.find(var) != -1:
                for word in line.split():
                    if word == var:
                        lookout = True
                    elif lookout:
                        lookout = False
                        if line.find("[UPDATE-TXN]") != -1:
                            latw = float(word)
                        else:
                            latr = float(word)
            if line.find(var99) != -1:
                for word in line.split():
                    if word == var99:
                        lookout = True
                    elif lookout:
                        lookout = False
                        if line.find("[UPDATE-TXN]") != -1:
                            latw99 = float(word)
                        else:
                            latr99 = float(word)
            if line.find(var95) != -1:
                for word in line.split():
                    if word == var95:
                        lookout = True
                    elif lookout:
                        lookout = False
                        if line.find("[UPDATE-TXN]") != -1:
                            latw95 = float(word)
                        else:
                            latr95 = float(word)
        if opr + opw == 0:
            results[c] += 0
            rr[c] += 0
            rw[c] += 0
            r99[c] += 0
            r95[c] += 0
        else:
            if latr99 == 0:
                latr99 = latr*pow(10,-3)
            if latw99 == 0:
                latw99 = latw*pow(10,-3)
            if latr95 == 0:
                latr95 = latr*pow(10,-3)
            if latw95 == 0:
                latw95 = latw*pow(10,-3)
            results[c] += (opr*latr*pow(10,-3) + opw*latw*pow(10,-3))/(opr+opw)
            r99[c] += (opr*latr99 + opw*latw99)/(opr+opw)
            r95[c] += (opr*latr95 + opw*latw95)/(opr+opw)
            rr[c] += latr*pow(10,-3)
            rw[c] += latw*pow(10,-3)
    for c in results:
        final_results += results[c]
        fr_read += rr[c]
        fr_write += rw[c]
        fr_95 += r95[c]
        fr_99 += r99[c]
        tp_final += tp[c]
    return tp_final, final_results/num_clients, fr_read/num_clients, fr_write/num_clients, fr_99/num_clients, fr_95/num_clients
    
        
def extract_data(experiment_dir, result_file):
    with open(result_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['algorithm', 'threads', 'read_prop', 'value_size', 'txn_size', 'num_clients', 'num_servers', 'num_key', 'distribution', 'zipfian_constant', 'throughput', 'average_latency', 'read_latency', 'write_latency', '99th_latency', '95th_latency'])
        writer.writeheader()
    # iterate through the directories in the root directory
        results = []
        for dirname in os.listdir(experiment_dir):
            if dirname.find("IT0") == -1:
                continue
            data = get_parameters(dirname)
            data['throughput'], data['average_latency'], data['read_latency'], data['write_latency'], data['99th_latency'], data['95th_latency'] = get_tp_and_latency(experiment_dir + '/' + dirname, int(data["num_clients"]))
            results.append(data)
        sorted_list = sorted(results, key=lambda x: (x['algorithm'], x['threads'], x['read_prop'], x['value_size'], x['txn_size'], x['num_clients'], x['num_servers'], x['num_key'], x['distribution'], x['zipfian_constant'], x['throughput'], x['average_latency'], x['read_latency'], x['write_latency'], x['99th_latency'], x['95th_latency']))
        for data in sorted_list:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)

def extract_freshness(experiment_dir, result_file):
    with open(result_file, 'w') as f:
        names = ['algorithm', 'threads', 'read_prop', 'value_size', 'txn_size', 'num_clients', 'num_servers', 'num_key', 'distribution', 'zipfian_constant']
        for s in staleness_string:
            names.append(s)
        writer = csv.DictWriter(f, fieldnames=names)
        writer.writeheader()
    # iterate through the directories in the root directory
        results = []
        for dirname in os.listdir(experiment_dir):
            if dirname.find("IT0") == -1:
                continue
            data = get_parameters(dirname)
            ret = get_freshness(experiment_dir + '/' + dirname, data["algorithm"])
            for i in range(len(staleness_string)):
                data[staleness_string[i]] = ret[i]
            results.append(data)
        sorted_list = sorted(results, key=lambda x: (x['algorithm'], x['threads'], x['read_prop'], x['value_size'], x['txn_size'], x['num_clients'], x['num_servers'], x['num_key'], x['distribution'], x['zipfian_constant']))
        for data in sorted_list:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='Directory path')
    now = datetime.now()
    parser.add_argument('experiment', type=str, help='Experiment name', default="experiment")
    parser.add_argument('--freshness', action='store_true', help='Extract freshness data')

    args = parser.parse_args()
    file_name = args.experiment + "-" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    directory = '/home/ubuntu/results/'
    file_path = os.path.join(directory, file_name)
    if args.freshness:
        extract_freshness(args.directory, file_path)
    else:
        extract_data(args.directory, file_path)
    print("Results in " + file_path)