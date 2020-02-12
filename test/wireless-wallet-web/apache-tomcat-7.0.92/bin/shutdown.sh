# !/bin/sh
jps|grep wireless-wallet-web|awk '{print $1}'|xargs kill -9