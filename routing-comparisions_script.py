import os
import matplotlib.pyplot as plot
import numpy as np

# installing/updating xmltodict module
os.system('sudo pip3 install xmltodict')

import json
import xmltodict


# Code for Generating the trace files and analyzing them


# Generating the trace files

path = '/root/ns-3-allinone/ns-3-dev/'
cur_dir = os.getcwd()
os.chdir(path)

build_cmd = "cp NSLAB-group8/group8-routing-comparisions.cc scratch/group8-routing-comparisions.cc && ./waf"
os.system(build_cmd)

nodes = 20
sinks = 9
protocols = {"AODV":2,"DSDV":3}

network_size = []

while nodes < 201:
    run_cmd = "./waf --run 'scratch/group8-routing-comparisions "
    for protocol in protocols:
        traceFileName = protocol + "_nodes_" +str(nodes)+ "_sinks_" +str(sinks)+ "_trace"
        args = "--nWifis="+str(nodes)+" --nSinks="+str(sinks)+" --protocol="+str(protocols[protocol])+" --CSVfileName="+traceFileName+"'"
        print(str(run_cmd + args))
        os.system(str(run_cmd + args))
       
               
        # moving the trace file to required directory
        move_path = cur_dir + "/Trace_files/"+protocol
        move_cmd = "mv "+ traceFileName +".flowmon "+move_path
        os.system(move_cmd)
        
    network_size.append(nodes)
    nodes *= 2
    sinks *= 2


   
# Analysis of the trace files


Avg_delay = {"AODV":[],"DSDV":[]}
Packet_delivery_ratio = {"AODV":[],"DSDV":[],"DSR":[]}
Throughput = {"AODV":[],"DSDV":[],"DSR":[]}
JitterSum = {"AODV":[],"DSDV":[],"DSR":[]}
for protocol in Avg_delay:
	os.chdir(cur_dir+"/Trace_files/"+protocol)
	for traceFile in os.listdir():
		xmlfile = open(traceFile)
		data = xmltodict.parse(xmlfile.read())
		xmlfile.close()

		delay ,sent_packets, recieved_packets, recieved_bytes, jitterSum = 0,0,0,0,0

		for flow in (data['FlowMonitor']['FlowStats']['Flow']):
			delay += float(flow['@delaySum'][:-2])
			sent_packets += int(flow['@txPackets'])
			recieved_packets += int(flow['@rxPackets'])
			recieved_bytes += int(flow['@rxBytes'])
			jitterSum += float(flow['@jitterSum'][:-2])
		Avg_delay[protocol].append(delay/len(data['FlowMonitor']['FlowStats']['Flow']))
		Packet_delivery_ratio[protocol].append(recieved_packets/sent_packets)
		Throughput[protocol].append((recieved_bytes*8)/(21.0*1024*1024))
		JitterSum[protocol].append(jitterSum)

# Since flowmonitor doesn't work with DSR protocol
# Getting the DSR results extracted.	
DSR_data = np.genfromtxt(cur_dir+'/Trace_files/DSR/DSR_results.csv', delimiter=' ')
Avg_delay['DSR'] = list(DSR_data[:,0])
Packet_delivery_ratio['DSR'] = list(DSR_data[:,1])
Throughput['DSR'] = list(DSR_data[:,2])
JitterSum['DSR'] = list(DSR_data[:,3])


# Plotting and saving the plots

plot.plot(network_size,Avg_delay["AODV"],c='r',marker="o")
plot.plot(network_size,Avg_delay["DSDV"],c='g',marker="o")
plot.plot(network_size,Avg_delay["DSR"],c='b',marker="o")
plot.legend(Avg_delay.keys())
plot.title("Network size VS Average Delay")
plot.xlabel("Network size")
plot.ylabel("Average Delay")
plot.savefig(cur_dir+'/graphs/Average_delay.png')
plot.show()

plot.plot(network_size,Packet_delivery_ratio["AODV"],c='r',marker="o")
plot.plot(network_size,Packet_delivery_ratio["DSDV"],c='g',marker="o")
plot.plot(network_size,Packet_delivery_ratio["DSR"],c='b',marker="o")
plot.legend(Avg_delay.keys())
plot.title("Network size VS Packet_delivery_ratio")
plot.xlabel("Network size")
plot.ylabel("Packet_delivery_ratio")
plot.savefig(cur_dir+'/graphs/Packet_delivery_ratio.png')
plot.show()

plot.plot(network_size,Throughput["AODV"],c='r',marker="o")
plot.plot(network_size,Throughput["DSDV"],c='g',marker="o")
plot.plot(network_size,Throughput["DSR"],c='b',marker="o")
plot.legend(Avg_delay.keys())
plot.title("Network size VS Throughput")
plot.xlabel("Network size")
plot.ylabel("Throughput")
plot.savefig(cur_dir+'/graphs/Throughput.png')
plot.show()


plot.plot(network_size,JitterSum["AODV"],c='r',marker="o")
plot.plot(network_size,JitterSum["DSDV"],c='g',marker="o")
plot.plot(network_size,JitterSum["DSR"],c='b',marker="o")
plot.legend(Avg_delay.keys())
plot.title("Network size VS JitterSum")
plot.xlabel("Network size")
plot.ylabel("JitterSum")
plot.savefig(cur_dir+'/graphs/JitterSum.png')
plot.show()


