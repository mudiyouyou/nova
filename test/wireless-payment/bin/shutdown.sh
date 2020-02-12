# !/bin/sh
jps|grep wireless-payment|awk '{print $1}'|xargs kill -9