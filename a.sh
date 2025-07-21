ls ~/zephyrproject/build/zephyr
echo 0000000
# ls ~/zephyrproject/build/zephyr/CMakeFiles/zephyr.dir
# echo 11111

ls ~/zephyrproject/build/CMakeFiles/app.dir/src
echo 2222
ls ~/zephyrproject/build/CMakeFiles/app.dir

echo 33333333333333
ls changed_projects

find changed_projects -type f \( -name "*.c" -o -name "*.cpp" \) -exec cp -- "{}" ~/zephyrproject/build/CMakeFiles/app.dir/ \;

echo 444444444444
ls ~/zephyrproject/build/CMakeFiles/app.dir
