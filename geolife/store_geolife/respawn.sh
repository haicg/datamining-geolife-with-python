###souce file from http://blog.sina.com.cn/s/blog_4c451e0e0100giqg.html
# #! 不是注释符，而是指定脚本由哪个解释器来执行，
# #! 后面有一个空格，空格后面为解释器的全路径且必须正确。
#! /bin/bash
PRO_PATH=""
# testpro 为要守护的可执行程序，即保证它是一直运行的
PROGRAM="main.py"

# 此脚本一直不停的循环运行，while <条件> 与 do 放在一行上要在条件后加分号
# if、then、while、do等关键字或命令是作为一个新表达式的开头，
# 一个新表达式之前的表达式必须以换行符或分号(；)来结束
# 如果条件不是单个常量或变量而是表达式的话，则要用[]括起来
# while、until与for循环皆以do开始以done结束构成循环体
while true ; do
# 休息10秒以确保要看护的程序运行起来了，这个时间因实际情况而定
#    sleep 10
# 单引号''中的$符与\符没有了引用变量和转义的作用，但在双引号""中是可以的！
# 单引号中如果还有单引号，则输出时全部的单引号都将去掉，单引号括住的内容原样输出。
# 例：echo 'have 'test'' --> have test
# ps aux --> a 为显示其他用户启动的进程；
#                 u 为显示启动进程的用户名与时间；
#                 x 为显示系统属于自己的进程；
# ps aux | grep 可执行程序名 --> 在得到的当前启动的所有进程信息文本中，
#                                            过滤出包含有指定文本(即可执行程序名字)的信息文本行
#注：假设 ps aux | grep 可执行程序名 有输出结果，但输出不是一条信而是两条，
# 一个为查找到的包含有指定文本(即可执行程序名字)的信息文本行(以换行符0x10结尾的文本为一行)，
# 一个为 grep 可执行程序名 ，即把自己也输出来了，
# 所这条信息是我们不需要的，因为我们只想知指定名字的可执行程序是否启动了
# grep -v 指定文本 --> 输出不包含指定文本的那一行文本信息
# wc -l --> 输出文件中的行数(-l --> 输出换行符统计数)
# ps aux | grep $PROGRAM | grep -v grep | wc -l --> 如果有指定程序名的程序启动的话，结果大于壹
    PRO_NOW=`ps aux | grep $PROGRAM | grep -v grep | wc -l`

# 整数比较：-lt -> 小于，-le -> 小于等于，-gt -> 大于，-ge -> 大于等于，-eq ->等于，-ne -> 不等于
# if [条件] 与 then 放在一行上要在条件后加分号
# 如果当前指定程序启动的个数小于壹的话
    if [ $PRO_NOW -lt 1 ]; then
# 0 -> 标准输入，1 -> 标准输出，2 - > 标准错误信息输出
# /dev/null --> Linux的特殊文件，它就像无底洞，所有重定向到它的信息数据都会消失！
# 2 > /dev/null --> 重定向 stderr 到 /dev/null，1 >& 2 --> 重定向 stdout 到 stderr，
# 直接启动指定程序，且不显示任何输出
# 可执行程序后面加空格加&，表示要执行的程序为后台运行

		if [ -e "filepathList.txt" ]
		then
			echo "file exist"
			linenum=`wc -w filepathList.txt|awk -F " " '{print $1}'`
			i=2
			if [ $linenum -lt $i ]
			then
				echo "empty"
				break
			fi
		else
			echo "no exist"
		fi
       	python $PROGRAM 2>/dev/null 1>&2 &
		echo "not empty"
	# date >> ./tinfo.log --> 定向输出当前日期时间到文件，添加到文件尾端，如果没有文件，则创建这个文件 
			date >> ./tinfo.log
# echo "test start" >> ./tinfo.log --> 定向输出 test start 添加到文件尾端
		echo "test start" >> ./tinfo.log
		echo "restart"
# if 分支结构体结束
    fi


# 基本与上面的相同，就是多了一个 grep T，其结果为过滤出含 T 字符的信息行
# T --> 进程已停止，D --> 不可中断的深度睡眠，R --> 进程运行或就绪，S --> 可接收信号的睡眠，
# X --> 已完全死掉，Z --> 已完全终止
    PRO_STAT=`ps aux|grep $PROGRAM |grep T|grep -v grep|wc -l`

# 如果指定进程状态为已停止的信息大于零的话
    if [ $PRO_STAT -gt 0 ] ; then
# killall --> 用名字方式来杀死进程，-9 --> 即发给程序一个信号值为9的信号，即SIGKILL(非法硬件指令)
# 也可以不指定信号，默认为SIGTERM，即信号值为15
        killall -9 $PROGRAM
        sleep 2
		if [ -e "filepathList.txt" ]
		then
			linenum=`wc -w filepathList.txt|awk -F " " '{print $1}'`
			i=2
			if [ $linenum -lt $i ]
			then
				echo "empty"
				break
			fi
		fi

		python $PROGRAM 2>/dev/null 1>&2 &
		echo "not empty"
	# date >> ./tinfo.log --> 定向输出当前日期时间到文件，添加到文件尾端，如果没有文件，则创建这个文件 
			date >> ./tinfo.log
# echo "test start" >> ./tinfo.log --> 定向输出 test start 添加到文件尾端
		echo "test start" >> ./tinfo.log
		echo "restart"
    fi
# while、until与for循环皆以do开始以done结束构成循环体
done
# exit 用来结束脚本并返回状态值，0 - 为成功，非零值为错误码，取值范围为0 ~ 255。
exit 0
