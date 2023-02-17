
defaultsettings = { "serversList" : [(5,5)],
                    "txnlen" : [4],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ #"READ_COMMITTED",
                                  "READ_ATOMIC_STAMP", 
                                  #"EIGER",
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_BLOOM"
                                  #,"LWLR",
                                  #"LWSR",
                                  #"LWNR"
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,3),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : "zipfian",
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }


test_port = {
    "serversList" : [(8,8)],
                    "txnlen" : [5],
                    "threads" : [32],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}

num_clients = {
    "serversList" : [(8,8)],
                    "txnlen" : [5],
                    "threads" : [2,4,8,16,32,64,128,256,512],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}


num_servers = {
    "serversList" : [(2,2),(4,4),(8,8),(16,16),(32,32)],
                    "txnlen" : [5],
                    "threads" : [32],
                    "numseconds" : 60,
                    "configs" : [
                                  "EIGER",
                                  "EIGER_PORT",
                                  "EIGER_PORT_PLUS"
                                ],
                    "readprop" : [.9],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
}


experiments = { 
                "port" : test_port,
                "num_clients" : num_clients,
                "num_servers" : num_servers,               
}