#/bin/sh -
find . -regex '.*\.c\|.*\.cpp\|.*\.h\|.*\.hpp\|.*\.py' > cscope.files
cscope -b -i cscope.files -f cscope.out


