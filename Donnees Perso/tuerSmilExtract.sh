ps -a | grep SMILExtract | cut -f2 -d' ' > processes.tmp
 
for line in $(cat processes.tmp); 
do sudo kill -9 $line ; 
echo "Processus $line tué"
done
