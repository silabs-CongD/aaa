ls ~/zephyrproject/build/zephyr
echo 0000000
# ls ~/zephyrproject/build/zephyr/CMakeFiles/zephyr.dir
# echo 11111

ls ~/zephyrproject/build/CMakeFiles/app.dir/src
echo 2222
ls ~/zephyrproject/build/CMakeFiles/app.dir

echo 33333333333333
mkdir tmp
while read line; do cp -r $WORKSPACE/projects/applications/$line --parents ./tmp; \
done < $WORKSPACE/projects/changed_projects.txt

find tmp -type f \( -name "*.c" -o -name "*.h" -o -name "*.cpp" \) -exec cp -- "{}" ~/zephyrproject/build/CMakeFiles/app.dir/ \;

echo 444444444444
ls ~/zephyrproject/build/CMakeFiles/app.dir
