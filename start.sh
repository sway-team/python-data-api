#!/bin/bash

# 设置变量
# VENV_PATH="/home/dev/workspace/pyflaskenv"
APP_PATH="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$APP_PATH/logs"
LOG_FILE="$LOG_DIR/app_$(date +%Y%m%d_%H%M%S).log"

# 创建日志目录（如果不存在）
mkdir -p "$LOG_DIR"

# 确保虚拟环境存在
# if [ ! -d "$VENV_PATH" ]; then
#     echo "错误：找不到虚拟环境 $VENV_PATH"
#     exit 1
# fi

# 导出当前时间为环境变量（用于日志）
export START_TIME="$(date '+%Y-%m-%d %H:%M:%S')"

# 定义启动应用的函数
start_app() {
    echo "启动应用..."
    echo "开始时间: $START_TIME" > "$LOG_FILE"
    echo "--------------------------------------" >> "$LOG_FILE"

    # 启动应用并加唯一标识参数
    (
     cd "$APP_PATH" &&
     nohup gunicorn -w 2 -b 0.0.0.0:5070 app:app --log-level=debug --pid "$APP_PATH/app.pid" >> "$LOG_FILE" 2>&1 &
    )

    # 等待进程启动
    sleep 1

    APP_PID=$(cat "$APP_PATH/app.pid")
    echo "应用已在后台启动，PID: $APP_PID"
    echo "日志文件: $LOG_FILE"
}

# 检查应用是否已在运行
if [ -f "$APP_PATH/app.pid" ]; then
    OLD_PID=$(cat "$APP_PATH/app.pid")
    if ps -p $OLD_PID > /dev/null; then
        echo "应用已在运行中，PID: $OLD_PID"
        echo "如需重启，请先停止应用: ./stop.sh"
        exit 1
    else
        echo "应用之前的PID文件存在但进程不在运行，将启动新实例"
    fi
fi

# 启动应用
start_app

# 显示日志文件的最后几行
echo "--------------------------------------"
echo "日志输出:"
tail -n 10 "$LOG_FILE"
echo "--------------------------------------"
echo "应用正在后台运行，使用 'tail -f $LOG_FILE' 查看实时日志"