import os

#f decrypt_data(curr_key):
cmd = 'ls output_folder/*ssl > file.txt'
os.system(cmd)
filename = open('file.txt', 'r')
for full_fil in filename:
    fils = full_fil.strip('\n').split('/')
    fil = fils[len(fils) - 1]
    info = fil.split('_')
    print(info)
    destIP = info[1]
    srcIP = info[0]
    cmd = "tcpdump -r test.pcap -w tmp_folder/out_" + srcIP + '_' + destIP + ".pcap host " + srcIP
    os.system(cmd)
    cmd = "tshark -nxr tmp_folder/out_" + srcIP + '_' + destIP + ".pcap -o ssl.keylog_file:" + full_fil.strip('\n') + " > output_folder_decrypted/" + srcIP + '_' + destIP + "_decrypted.out"
    print ("----------" + cmd)
    os.system(cmd)
    cmd = "tshark -nxr tmp_folder/out_" + srcIP + '_' + destIP + ".pcap" + " > output_folder_decrypted/" + srcIP + '_' + destIP + ".out"
    print  (cmd)
    os.system(cmd)





