#!/bin/bash

APP_PATH="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$APP_PATH/app.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "正在停止应用 (PID: $PID)..."
        kill $PID
        sleep 2
        
        # 检查进程是否仍在运行
        if ps -p $PID > /dev/null; then
            echo "应用未响应，强制终止..."
            kill -9 $PID
        fi
        
        echo "应用已停止"
    else
        echo "应用未运行"
    fi
    
    # 删除PID文件
    # rm "$PID_FILE"
else
    echo "找不到PID文件，应用可能未运行"
fi