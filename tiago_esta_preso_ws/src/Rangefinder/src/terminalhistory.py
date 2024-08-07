        
 1248  terminator -u
 1249  cd /
 1250  cd /tiago_public_ws/
 1251  ls
 1252  cd ~
 1253  ls
 1254  cd docker_update/
 1255  ls
 1256  ./copy_maze.sh 
 1257  sudo ./copy_maze.sh 
 1258  sudo ./update_gpu.sh 
 1259  cd /tiago_public_ws/
 1260  source devel/setup.bash 
 1261  cd ^
 1262  cd ~
 1263  ls
 1264  mkdir tiago_esta_preso
 1265  rm -r
 1266  mkdir -p ~/tiago_esta_preso_ws/src
 1267  cd ~/tiago_esta_preso_ws/src/
 1268  catkin_init_workspace
 1269  cd ..
 1270  catkin.make
 1271  catkin_make
 1272  source devel/setup.bash 
 1273  cd src/
 1274  ls
 1275  nano divisao_das_tarefas.txt
 1276  catkin_create_pkg Rangefinder rospy roscpp std_msgs
 1277  ls
 1278  cd Rangefinder/
 1279  ls
 1280  cd src/
 1281  ls
 1282  touch rangefind.py
 1283  sudo chmod +x rangefind.py 
 1284  ls
 1285  ./rangefind.py 
 1286  history
